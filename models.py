from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
import uuid
import pymongo

# Database
client = pymongo.MongoClient(
    'mongodb+srv://test:1234@cluster0.es4s8d0.mongodb.net/test')
db = client.users


class User:

    def create_account(self):

        # Create the user object
        user = {
            '_id': uuid.uuid4().hex,
            'first_name': request.get_json()['firstName'],
            'last_name': request.get_json()['lastName'],
            'email': request.get_json()['email'],
            'password': request.get_json()['password'],
            'confirm_password': request.get_json()['confirmPassword']
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        user['confirm_password'] = pbkdf2_sha256.encrypt(
            user['confirm_password'])

        # Check for existing email address
        if db.users.find_one({'email': user['email']}):
            return jsonify({'error': 'Email already exists'})

        # Inserting user in the database
        db.users.insert_one(user)

        return jsonify(user), 200
