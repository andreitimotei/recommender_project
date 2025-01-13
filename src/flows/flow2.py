from recombee_api_client.api_client import *
from recombee_api_client.api_requests import *

from src.cold_start_recommender import display_recommendations
from src.flows.flow1 import add_user_to_recombee

DATABASE_ID = 'sisteme-de-recomandare-dev'
PRIVATE_TOKEN = 'mvIzr7ar031TCk8AEsuoyya20kH0AuTgz9kkb8fz3MVZ4IYrYhi9h3u14et0PAZ8'

# Initialize Recombee client
client = RecombeeClient(DATABASE_ID, PRIVATE_TOKEN, region=Region.EU_WEST)

if __name__ == "__main__":
    user = {"user_id": "user_12", "preferred_categories": ['General'], "age": 30, "location": "Romania"}

    add_user_to_recombee(user)

    client.send(AddPurchase(user_id='user_12', item_id='55b7d5134c8c24692cb8fc1d2fba377f', cascade_create=True))

    recommendations = client.send(RecommendItemsToItem('55b7d5134c8c24692cb8fc1d2fba377f', 'user_12', count=5, scenario = 'content-based'))

    recommended_item_ids = [item['id'] for item in recommendations['recomms']]
    display_recommendations('user_12', recommended_item_ids)
