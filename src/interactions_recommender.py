import re

from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import *


DATABASE_ID = 'sisteme-de-recomandare-dev'
PRIVATE_TOKEN = 'mvIzr7ar031TCk8AEsuoyya20kH0AuTgz9kkb8fz3MVZ4IYrYhi9h3u14et0PAZ8'

# Initialize Recombee client
client = RecombeeClient(DATABASE_ID, PRIVATE_TOKEN, region=Region.EU_WEST)


def recommend_books(user_id, count):
    try:

        recommendations = client.send(RecommendItemsToUser(user_id, count, scenario = 'recommend_items_to_user'))

        return [rec['id'] for rec in recommendations['recomms']]
    except Exception as e:
        print(f"Error generating recommendations for user '{user_id}': {e}")
        return []

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


# Function to retrieve item details by ID
def get_item_details(item_id):
    try:
        response = client.send(GetItemValues(item_id))
        return response
    except Exception as e:
        print(f"Failed to retrieve details for item {item_id}: {e}")
        return None


if __name__ == "__main__":
    user_id = 'user_4'
    count = 5

    # Get and display recommendations
    recommendations = recommend_books(user_id, count)
    display_recommendations(user_id, recommendations)

    # after 20 interactions per user

    # user 1 Recommended books: ['1f0cb7cb2442f408dc8f9307feea98e2', '284ddd06e1545b871aa6b1ad1c621050', '3df58153ae3b6e66fde3456f3feabcc4', 'f9d229a6ed0e299d3cb0133f117426f8', '3b74c10ff26fd151981ff9650eebb53c']
    # user 2 Recommended books: ['1f0cb7cb2442f408dc8f9307feea98e2', '284ddd06e1545b871aa6b1ad1c621050', 'adbc8dddfa15d677a1cea7831f883114', '99a810e81e819f3f6b3dc2f21c3077ca', 'd0fb9a5f7010af0a7a6297141e95b294']
    # user 3 Recommended books: ['a606b3b02930b70dff78144b4f61a81f', '3b74c10ff26fd151981ff9650eebb53c', '284ddd06e1545b871aa6b1ad1c621050', 'adbc8dddfa15d677a1cea7831f883114', '1f0cb7cb2442f408dc8f9307feea98e2']
    # user 4 Recommended books: ['1f0cb7cb2442f408dc8f9307feea98e2', '284ddd06e1545b871aa6b1ad1c621050', '99a810e81e819f3f6b3dc2f21c3077ca', '8f9f9ff4f9246f13fdaf19c25875042c', 'd0fb9a5f7010af0a7a6297141e95b294']
    # user 5 Recommended books: ['1f0cb7cb2442f408dc8f9307feea98e2', '284ddd06e1545b871aa6b1ad1c621050', 'f9d229a6ed0e299d3cb0133f117426f8', '99a810e81e819f3f6b3dc2f21c3077ca', '127d006eb0d1af95bc1633569668d1fd']

    # after 50 more interactions per user
    # user 1 Recommended books: ['3569eac335a4d0a755920f3f3cd207c2', 'fe5d02315a9775ccfed31edca77e75e4', '5af66ac3c4cf54cd76a8d0e2b0d2adfa', 'eb1fce6a906f73ab6c234bfaefb50ef9', '284ddd06e1545b871aa6b1ad1c621050']
    # user 2 Recommended books: ['1f0cb7cb2442f408dc8f9307feea98e2', '63c94782aaca1f6e5697cd4cf9cf94b1', '284ddd06e1545b871aa6b1ad1c621050', '8504ddaf8bd13a9b562574a83edc8af0', 'e98250829d53b7765c8ed8f04c438ab1']
    # user 3 Recommended books: ['284ddd06e1545b871aa6b1ad1c621050', '1f0cb7cb2442f408dc8f9307feea98e2', 'd0fb9a5f7010af0a7a6297141e95b294', '63c94782aaca1f6e5697cd4cf9cf94b1', '99a810e81e819f3f6b3dc2f21c3077ca']
    # user 4 Recommended books: ['284ddd06e1545b871aa6b1ad1c621050', '1f0cb7cb2442f408dc8f9307feea98e2', '99a810e81e819f3f6b3dc2f21c3077ca', 'c60c46e2acfa6629f3cf8dcede9fd958', 'eb1fce6a906f73ab6c234bfaefb50ef9']
    # user 5 Recommended books: ['284ddd06e1545b871aa6b1ad1c621050', '1f0cb7cb2442f408dc8f9307feea98e2', 'f9d229a6ed0e299d3cb0133f117426f8', '790c926818658c8a88ae36aabf02b7e6', 'eb1fce6a906f73ab6c234bfaefb50ef9']