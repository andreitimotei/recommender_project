import hashlib
from datetime import datetime

import recombee_api_client
from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *
import pandas as pd

# Configuration
DATABASE_ID = 'sisteme-de-recomandare-dev'
PRIVATE_TOKEN = 'mvIzr7ar031TCk8AEsuoyya20kH0AuTgz9kkb8fz3MVZ4IYrYhi9h3u14et0PAZ8'
PROCESSED_DATA_PATH = "../data/processed/BooksDataset_cleaned.csv"
LIMIT_ROWS = 5000

# Initialize Recombee client
client = RecombeeClient(DATABASE_ID, PRIVATE_TOKEN)


# Define Item Properties in Recombee
def define_item_properties():
    properties = [
        ('title', 'string'),
        ('authors', 'string'),
        ('description', 'string'),
        ('category', 'set'),
        ('publisher', 'string'),
        ('publish_date', 'timestamp'),
        ('price', 'double')
    ]
    for prop, prop_type in properties:
        try:
            client.send(AddItemProperty(prop, prop_type))
            print(f"Successfully added property: {prop} ({prop_type})")
        except Exception as e:
            print(f"Failed to add property {prop}: {e}")


# Function to generate a unique hash for the Title
def generate_item_id(title):
    return hashlib.md5(title.encode('utf-8')).hexdigest()

# Clean and parse categories
def parse_categories(category_str):
    if pd.isnull(category_str):
        return []  # Return an empty list if no categories exist
    # Split by commas and strip spaces
    categories = [cat.strip() for cat in category_str.split(',')]
    # Remove stray characters
    return [cat.replace("']", "").replace("[", "").replace("'", "").strip() for cat in categories if cat]

# Function to add users to Recombee
def add_users_to_recombee(users):
    for user in users:
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


# Upload items to Recombee
def upload_items_to_recombee(df):



    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, '%A, %B %d, %Y').isoformat()
        except (ValueError, TypeError):
            return None  # Return None if date is invalid

    df['itemId'] = df['Title'].apply(generate_item_id)
    df['Category'] = df['Category'].apply(parse_categories)
    df['Publish Date'] = df['Publish Date'].apply(parse_date)

    for _, row in df.iterrows():
        try:
            # Add the item to Recombee
            client.send(AddItem(row['itemId']))

            # Set item properties
            client.send(SetItemValues(
                row['itemId'],  # Item ID
                {
                    'title': row['Title'],
                    'authors': row['Authors'],
                    'description': row['Description'],
                    'category': row['Category'],
                    'publisher': row['Publisher'],
                    'publish_date': row['Publish Date'].isoformat() if pd.notnull(row['Publish Date']) else None,
                    'price': row['Price']
                },
                cascade_create=True
            ))
        except Exception as e:
            print(f"Failed to upload item {row['Title']}: {e}")





# Example usage
if __name__ == "__main__":
    # client.send(ResetDatabase())

    # Define user properties
    client.send(AddUserProperty('preferred_categories', 'set'))
    client.send(AddUserProperty('age', 'int'))
    client.send(AddUserProperty('location', 'string'))

    users = [
        {"user_id": "user_1", "preferred_categories": ["Fiction", "Self-help"], "age": 25, "location": "USA"},
        {"user_id": "user_2", "preferred_categories": ["Cooking", "Health & Fitness"], "age": 30, "location": "Canada"},
        {"user_id": "user_3", "preferred_categories": ["Biography & Autobiography"], "age": 40, "location": "UK"},
        {"user_id": "user_4", "preferred_categories": ["History", "Poetry"], "age": 35, "location": "Australia"},
        {"user_id": "user_5", "preferred_categories": ["General"], "age": 28, "location": "India"}
    ]

    # Add the users
    add_users_to_recombee(users)

    # Upload items to Recombee
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df = df.dropna(subset=['Title', 'Authors', 'Description'])

    df = df.head(LIMIT_ROWS)

    define_item_properties()

    upload_items_to_recombee(df)

