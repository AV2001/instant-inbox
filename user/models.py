from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
import uuid


class User:

    def create_account(self):

        print(request.form)

        # Create the user object
        user = {
            '_id': uuid.uuid4().hex,
            'first_name': request.form.get('first-name'),
            'last_name': request.form.get('last-name'),
            'email': request.form.get('create-account-email'),
            'password': request.form.get('create-account-password'),
            'confirm_password': request.form.get('create-account-confirm-password')
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        user['confirm_password'] = pbkdf2_sha256.encrypt(
            user['confirm_password'])

        return jsonify(user), 200
