from flask import Flask, request, redirect, render_template, session, url_for, jsonify, send_from_directory
from msal import ConfidentialClientApplication
from uuid import uuid4
import secrets
import requests
from dotenv.main import load_dotenv
import os


from models import User


load_dotenv()


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Get the valkues from the .env file
APPLICATION_ID = os.environ.get('APPLICATION_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

AUTHORITY = 'https://login.microsoftonline.com/common'
SCOPES = ['User.Read', 'Mail.Read']
REDIRECT_URI = 'https://instant-inbox.herokuapp.com/callback'
BASE_URL = 'https://graph.microsoft.com/v1.0/me/'


# Rendering the index.html
@app.route('/')
def home():
    return render_template('index.html', title='Home')


# Rendering the about.html
@app.route('/about/')
def about():
    return render_template('about.html', title='About')


# Outlook authentication
@app.route('/login/')
def login():
    session['state'] = str(uuid4())
    msal_app = ConfidentialClientApplication(
        client_id=APPLICATION_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY
    )

    authorization_url = msal_app.get_authorization_request_url(
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        state=session['state']
    )

    return redirect(authorization_url)


# Handles the callback from Azure Active Directory
@app.route('/callback')
def callback():
    if request.args.get('state') != session.get('state'):
        return 'State Mismatch', 400

    msal_app = ConfidentialClientApplication(
        client_id=APPLICATION_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY
    )

    token_response = msal_app.acquire_token_by_authorization_code(
        request.args['code'],
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    # Stores the access token in the session
    session['access_token'] = token_response['access_token']
    return redirect(url_for('me'))


# Uses access token to query the Microsoft Graph API and get the logged in user's email address
@app.route('/me')
def me():
    headers = {
        'Authorization': f'Bearer {session["access_token"]}',
        'Content-Type': 'application/json'
    }
    response = requests.get(
        'https://graph.microsoft.com/v1.0/me', headers=headers)
    data = response.json()
    email_address = data['mail']

    # Get user's inbox messages
    messages_response = requests.get(
        BASE_URL + 'messages', headers=headers)
    messages_data = messages_response.json()

    # Return email address and inbox messages as JSON
    return jsonify({
        'email_address': email_address,
        'inbox_messages': messages_data['value']
    })


@app.route('//.well-known/<path:path>')
def serve_well_known(path):
    return send_from_directory('.well-known', path)


if __name__ == '__main__':
    # set debug to True when in development mode
    app.run(debug=True)
