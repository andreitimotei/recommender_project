from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import SearchItems, GetUserValues, GetItemValues

DATABASE_ID = 'sisteme-de-recomandare-dev'
PRIVATE_TOKEN = 'mvIzr7ar031TCk8AEsuoyya20kH0AuTgz9kkb8fz3MVZ4IYrYhi9h3u14et0PAZ8'

# Initialize Recombee client
client = RecombeeClient(DATABASE_ID, PRIVATE_TOKEN, region=Region.EU_WEST)

# Function to retrieve item details by ID
def get_item_details(item_id):
    try:
        response = client.send(GetItemValues(item_id))
        return response
    except Exception as e:
        print(f"Failed to retrieve details for item {item_id}: {e}")
        return None

def display_recommendations(user_id, recommended_item_ids):
    print(f"\nRecommendations for User '{user_id}':")
    for item_id in recommended_item_ids:
        details = get_item_details(item_id)
        if details:
            print(f"Item ID: {item_id}")
            for key, value in details.items():
                print(f"  {key}: {value}")
            print("-")
        else:
            print(f"Item ID: {item_id} - Details not available")

# Function to recommend books based on preferred categories
def recommend_books_by_category(user_id, count=5):
    try:
        # Step 1: Retrieve user properties
        user_data = client.send(GetUserValues(user_id))
        preferred_categories = user_data.get('preferred_categories', [])

        if not preferred_categories:
            print(f"No preferred categories found for user: {user_id}")
            return []

        print(f"User '{user_id}' preferred categories: {preferred_categories}")

        # Step 2: Build filter string
        categories_filter = " or ".join([f"\"{category}\" in 'category'" for category in preferred_categories])
        print(f"Filter string: {categories_filter}")

        # Step 3: Search for items matching the filter
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

        print(search_results)

        # Step 4: Retrieve details and display results
        recommended_item_ids = [item['id'] for item in search_results['recomms']]
        display_recommendations(user_id, recommended_item_ids)
        return recommended_item_ids

    except Exception as e:
        print(f"Error generating category-based recommendations for user '{user_id}': {e}")
        return []

# Example usage
if __name__ == "__main__":
    # Recommend books for a user based on categories
    user_id = 'user_5'  # Replace with the user ID
    print("Generating category-based recommendations...\n")
    recommend_books_by_category(user_id)
