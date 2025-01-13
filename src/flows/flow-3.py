from recombee_api_client.api_client import *
from recombee_api_client.api_requests import *

from src.cold_start_recommender import display_recommendations
from src.data_upload import add_users_to_recombee
from src.flows.flow1 import add_user_to_recombee

DATABASE_ID = 'sisteme-de-recomandare-dev'
PRIVATE_TOKEN = 'mvIzr7ar031TCk8AEsuoyya20kH0AuTgz9kkb8fz3MVZ4IYrYhi9h3u14et0PAZ8'

# Initialize Recombee client
client = RecombeeClient(DATABASE_ID, PRIVATE_TOKEN, region=Region.EU_WEST)

users = [
        {"user_id": "user_20", "preferred_categories": ["Fiction", "Self-help"], "age": 25, "location": "USA"},
        {"user_id": "user_21", "preferred_categories": ["Cooking", "Health & Fitness"], "age": 30, "location": "Canada"},
        {"user_id": "user_22", "preferred_categories": ["Biography & Autobiography"], "age": 40, "location": "UK"},
        {"user_id": "user_23", "preferred_categories": ["History", "Poetry"], "age": 35, "location": "Australia"},
        {"user_id": "user_24", "preferred_categories": ["General"], "age": 28, "location": "India"}
    ]





def add_interactions():
    # Add the users
    add_users_to_recombee(users)

    # user_21
    client.send(AddPurchase(user_id='user_21', item_id='0004dfa44c1ba26c97268166800589a5', cascade_create=True))
    client.send(AddPurchase(user_id='user_21', item_id='000ef363628614103bffd854ab629625', cascade_create=True))
    client.send(AddPurchase(user_id='user_21', item_id='0017bb6683cc968ebaeb3bf4e4e213d9', cascade_create=True))
    client.send(AddPurchase(user_id='user_21', item_id='002df4a92277b737d0f720ad03741f36', cascade_create=True))
    client.send(AddPurchase(user_id='user_21', item_id='00404a068497500ab205b1839af48085', cascade_create=True))
    client.send(AddPurchase(user_id='user_21', item_id='00459de4a4d740335eca77b83515f15e', cascade_create=True))
    client.send(AddPurchase(user_id='user_21', item_id='00517cf0a35043635e5b88fa7038b298', cascade_create=True))

    # user_22
    client.send(AddPurchase(user_id='user_22', item_id='0004dfa44c1ba26c97268166800589a5', cascade_create=True))
    client.send(AddPurchase(user_id='user_22', item_id='000ef363628614103bffd854ab629625', cascade_create=True))
    client.send(AddPurchase(user_id='user_22', item_id='0017bb6683cc968ebaeb3bf4e4e213d9', cascade_create=True))
    client.send(AddPurchase(user_id='user_22', item_id='002df4a92277b737d0f720ad03741f36', cascade_create=True))
    client.send(AddPurchase(user_id='user_22', item_id='00404a068497500ab205b1839af48085', cascade_create=True))
    client.send(AddPurchase(user_id='user_22', item_id='00459de4a4d740335eca77b83515f15e', cascade_create=True))
    client.send(AddPurchase(user_id='user_22', item_id='00517cf0a35043635e5b88fa7038b298', cascade_create=True))

    # user_23
    client.send(AddPurchase(user_id='user_23', item_id='0004dfa44c1ba26c97268166800589a5', cascade_create=True))
    client.send(AddPurchase(user_id='user_23', item_id='000ef363628614103bffd854ab629625', cascade_create=True))
    client.send(AddPurchase(user_id='user_23', item_id='0017bb6683cc968ebaeb3bf4e4e213d9', cascade_create=True))
    client.send(AddPurchase(user_id='user_23', item_id='002df4a92277b737d0f720ad03741f36', cascade_create=True))
    client.send(AddPurchase(user_id='user_23', item_id='00404a068497500ab205b1839af48085', cascade_create=True))
    client.send(AddPurchase(user_id='user_23', item_id='00459de4a4d740335eca77b83515f15e', cascade_create=True))
    client.send(AddPurchase(user_id='user_23', item_id='00517cf0a35043635e5b88fa7038b298', cascade_create=True))

    # user_24
    client.send(AddPurchase(user_id='user_24', item_id='0004dfa44c1ba26c97268166800589a5', cascade_create=True))
    client.send(AddPurchase(user_id='user_24', item_id='000ef363628614103bffd854ab629625', cascade_create=True))
    client.send(AddPurchase(user_id='user_24', item_id='0017bb6683cc968ebaeb3bf4e4e213d9', cascade_create=True))
    client.send(AddPurchase(user_id='user_24', item_id='002df4a92277b737d0f720ad03741f36', cascade_create=True))
    client.send(AddPurchase(user_id='user_24', item_id='00404a068497500ab205b1839af48085', cascade_create=True))
    client.send(AddPurchase(user_id='user_24', item_id='00459de4a4d740335eca77b83515f15e', cascade_create=True))
    client.send(AddPurchase(user_id='user_24', item_id='00517cf0a35043635e5b88fa7038b298', cascade_create=True))





if __name__ == "__main__":
    add_interactions()

    # user_20
    client.send(AddPurchase(user_id='user_20', item_id='0004dfa44c1ba26c97268166800589a5', cascade_create=True))
    client.send(AddPurchase(user_id='user_20', item_id='000ef363628614103bffd854ab629625', cascade_create=True))

    recommendations = client.send(RecommendItemsToUser('user_20', count = 5, scenario='collaborative'))

    recommended_item_ids = [item['id'] for item in recommendations['recomms']]
    display_recommendations('user_20', recommended_item_ids)
