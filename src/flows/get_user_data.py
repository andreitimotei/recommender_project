from recombee_api_client.api_client import *
from recombee_api_client.api_requests import *

from src.cold_start_recommender import display_recommendations
from src.flows.flow1 import add_user_to_recombee

DATABASE_ID = 'sisteme-de-recomandare-dev'
PRIVATE_TOKEN = 'mvIzr7ar031TCk8AEsuoyya20kH0AuTgz9kkb8fz3MVZ4IYrYhi9h3u14et0PAZ8'

# Initialize Recombee client
client = RecombeeClient(DATABASE_ID, PRIVATE_TOKEN, region=Region.EU_WEST)

if __name__ == "__main__":
    users = client.send(ListUsers(return_properties = True))
    print(users)