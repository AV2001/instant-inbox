from flask import jsonify, request
import uuid
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
            'email': email_address,
            'module_change': '',
            'travel_leave': '',
            'sick_leave': ''
        }

        # Check if user exists
        existing_user = db.users.find_one({'email': email_address})
        if existing_user:
            user_data = existing_user
        else:
            # Insert new user with empty tags
            db.users.insert_one(user_data)

        return user_data
