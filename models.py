from flask import jsonify, request
import pymongo
from dotenv.main import load_dotenv
import os

load_dotenv()

# Get the connection string for the database from.env file
MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')

# Database
client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)


# Give name for the database
db = client.instantInbox


class User:
    def save_user_data(self, email_address):
        user_data = {
            'email_address': email_address,
            'module_change': '',
            'travel_leave': '',
            'sick_leave': ''
        }

        # Check if user exists
        existing_user = db.users.find_one({'email_address': email_address})
        if existing_user:
            user_data = existing_user
            user_data.pop('_id', None)
        else:
            # Insert new user with empty tags
            db.users.insert_one(user_data)
            user_data.pop('_id', None)

        return user_data

    def update_tags(self, email_address, module_change, travel_leave, sick_leave):
        result = db.users.update_one(
            {'email_address': email_address},
            {'$set': {
                'module_change': module_change,
                'travel_leave': travel_leave,
                'sick_leave': sick_leave
            }}
        )

        return result.modified_count > 0
