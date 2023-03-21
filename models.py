from flask import jsonify, request
import uuid
import pymongo
from dotenv.main import load_dotenv
import os

load_dotenv()

MONGODB_CONNECTION_STRING = os.environ['MONGODB_CONNECTION_STRING']


# Database
client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)


# Give name for the database
db = client.instantInbox


class User:
    def create_account(self):

        # Create the user object
        user = {
            '_id': uuid.uuid4().hex,
            'firstName': request.get_json()['firstName'],
            'lastName': request.get_json()['lastName'],
            'email': request.get_json()['email'],
            'password': request.get_json()['password'],
            'confirmPassword': request.get_json()['confirmPassword']
        }

        # Check for existing email address
        if db.users.find_one({'email': user['email']}):
            return jsonify({'message': 'Email already exists'})

        # Inserting user in the database
        db.users.insert_one(user)

        # Return user with status code set to 200
        return jsonify(user), 200

    def login(self):

        user = {
            'email': request.get_json()['email'],
            'password': request.get_json()['password']
        }

        retrieved_user = db.users.find_one({'password': user['password']})

        # Check whether email address and password match
        if retrieved_user:
            return jsonify(retrieved_user), 200

        return jsonify({'message': 'Your email/password is wrong!'})
