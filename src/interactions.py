import random
from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import AddDetailView, AddPurchase, ListItems, AddBookmark, AddCartAddition, \
    AddRating

# Configuration
DATABASE_ID = 'sisteme-de-recomandare-dev'
PRIVATE_TOKEN = 'mvIzr7ar031TCk8AEsuoyya20kH0AuTgz9kkb8fz3MVZ4IYrYhi9h3u14et0PAZ8'
client = RecombeeClient(DATABASE_ID, PRIVATE_TOKEN)

# List of users
users = ['user_1', 'user_2', 'user_3', 'user_4', 'user_5']

# Load item IDs from the file
item_ids = client.send(ListItems())

print(len(item_ids))

# Function to send interactions for users
def send_interactions(users, item_ids, max_interactions=50):
    for user in users:
        print(f"Sending interactions for user: {user}")
        interactions_sent = 0

        # Randomly generate interactions for a user
        while interactions_sent < max_interactions:
            item_id = random.choice(item_ids)
            interaction_type = random.choice(["view", "purchase", "bookmark", "rating", "cart_addition"])

            try:
                if interaction_type == "view":
                    client.send(AddDetailView(user_id=user, item_id=item_id, cascade_create=True))
                    print(f"Added view interaction: User={user}, Item={item_id}")
                elif interaction_type == "purchase":
                    client.send(AddPurchase(user_id=user, item_id=item_id, cascade_create=True))
                    print(f"Added purchase interaction: User={user}, Item={item_id}")
                elif interaction_type == "bookmark":
                    client.send(AddBookmark(user_id=user, item_id=item_id, cascade_create=True))
                    print(f"Added bookmark interaction: User={user}, Item={item_id}")
                elif interaction_type == "cart_addition":
                    client.send(AddCartAddition(user_id=user, item_id=item_id, cascade_create=True))
                    print(f"Added cart addition interaction: User={user}, Item={item_id}")
                elif interaction_type == "rating":
                    rating_value = random.randint(1, 5)  # Random rating between 1 and 5
                    client.send(AddRating(user_id=user, item_id=item_id, rating=rating_value, cascade_create=True))
                    print(f"Added rating interaction: User={user}, Item={item_id}, Rating={rating_value}")

                interactions_sent += 1

            except Exception as e:
                print(f"Failed to send interaction for user={user}, item={item_id}: {e}")

if __name__ == "__main__":
    # Define max interactions per user
    MAX_INTERACTIONS = 50

    # Call the function to send interactions
    send_interactions(users, item_ids, max_interactions=MAX_INTERACTIONS)
