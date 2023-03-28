from flask import Flask, request, redirect, render_template, session, url_for, jsonify, send_from_directory
from msal import ConfidentialClientApplication
from uuid import uuid4
import secrets
import requests
from dotenv import load_dotenv
import os


from models import User


load_dotenv()


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Get the valkues from the .env file
APPLICATION_ID = os.getenv('APPLICATION_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


AUTHORITY = 'https://login.microsoftonline.com/common'
SCOPES = ['User.Read', 'Mail.ReadBasic']
REDIRECT_URI = 'http://localhost:5000/callback'
BASE_URL = 'https://graph.microsoft.com/v1.0/me/'


# Renders index.html
@app.route('/')
def home():
    return render_template('index.html', title='Home')


# Renders about.html
@app.route('/about/')
def about():
    return render_template('about.html', title='About')


# Renders inbox.html
@app.route('/inbox')
def inbox():
    return render_template('inbox.html', title='Inbox')


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
        return 'Please try again.', 400
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
    return redirect(url_for('inbox'))


# Uses access token to query the Microsoft Graph API and get the logged in user's email address
@app.route('/fetch-emails')
def fetch_emails():
    try:
        headers = {
            'Authorization': f'Bearer {session["access_token"]}',
            'Content-Type': 'application/json'
        }
        response = requests.get(
            'https://graph.microsoft.com/v1.0/me', headers=headers)

        # Check for errors in the response
        response.raise_for_status()

        data = response.json()
        email_address = data.get('mail') or data.get('userPrincipalName')

        # Get user's inbox messages
        messages_response = requests.get(
            BASE_URL + 'messages', headers=headers)

        # Check for errors in the messages response
        messages_response.raise_for_status()

        messages_data = messages_response.json().get('value', [])

        return jsonify(email_address=email_address, messages=messages_data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(error=str(e)), 500


@app.route('/.well-known/<path:path>')
def serve_well_known(path):
    return send_from_directory('.well-known', path)


if __name__ == '__main__':
    # set debug to True when in development mode
    app.run(debug=True)
