from recombee_api_client.api_client import *
from recombee_api_client.api_requests import *

from src.cold_start_recommender import display_recommendations

DATABASE_ID = 'sisteme-de-recomandare-dev'
PRIVATE_TOKEN = 'mvIzr7ar031TCk8AEsuoyya20kH0AuTgz9kkb8fz3MVZ4IYrYhi9h3u14et0PAZ8'

# Initialize Recombee client
client = RecombeeClient(DATABASE_ID, PRIVATE_TOKEN, region=Region.EU_WEST)


def add_user_to_recombee(user):
    try:
        # Add the user
        client.send(AddUser(user['user_id']))

        # Set user properties
        client.send(SetUserValues(
            user['user_id'],
            {
                "preferred_categories": user['preferred_categories'],
                "age": user['age'],
                "location": user['location']
            },
            cascade_create=True
        ))
        print(f"Successfully added user {user['user_id']}")
    except Exception as e:
        print(f"Failed to add user {user['user_id']}: {e}")

def cold_start(user_id, count=5):
    user_data = client.send(GetUserValues(user_id))

    preferred_categories = user_data.get('preferred_categories', [])

    if not preferred_categories:
        print(f"No preferred categories found for user: {user_id}")
        return []

    categories_filter = " or ".join([f"\"{category}\" in 'category'" for category in preferred_categories])

    search_results = client.send(
        SearchItems(
            search_query=categories_filter,  # Empty query since we only filter
            user_id=user_id,
            count=count,
            filter=categories_filter,
            scenario='cold_start',
            cascade_create=True
        )
    )

    recommended_item_ids = [item['id'] for item in search_results['recomms']]
    display_recommendations(user_id, recommended_item_ids)


if __name__ == "__main__":
    user = {"user_id": "user_10", "preferred_categories": ["Science Fiction", "Fantasy"], "age": 24, "location": "Romania"}

    add_user_to_recombee(user)

    cold_start('user_10', 5)


