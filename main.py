from flask import Flask, request, redirect, render_template, session, url_for, jsonify,  send_from_directory, Response
from msal import ConfidentialClientApplication
from uuid import uuid4
import secrets
import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup


from models import User
from algorithm import predict_tag


load_dotenv()


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Get the valkues from the .env file
APPLICATION_ID = os.getenv('APPLICATION_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


AUTHORITY = 'https://login.microsoftonline.com/common'
SCOPES = ['User.Read', 'Mail.Read', 'Mail.Send', 'Mail.ReadWrite']
REDIRECT_URI = 'https://instant-inbox.herokuapp.com/callback'
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
    access_token = session.get('access_token')
    return render_template('inbox.html', title='Inbox', access_token=access_token)


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
            BASE_URL + f"messages?$filter=isRead eq false", headers=headers)

        # Check for errors in the messages response
        messages_response.raise_for_status()

        messages_data = messages_response.json().get('value', [])

        cleaned_messages = []

        for message in messages_data:
            html_content = message['body']['content']
            soup = BeautifulSoup(html_content, 'html.parser')

            # Remove all script and style elements
            for script in soup(['script', 'style']):
                script.extract()

            cleaned_text = soup.get_text()
            message['body']['content'] = cleaned_text

            # Add predicted tags and corresponding tag content to each message
            predicted_tag = predict_tag(cleaned_text)
            tag_content = User().get_tag_content(email_address, predicted_tag)
            message['predicted_tag'] = predicted_tag
            message['tag_content'] = tag_content

            cleaned_messages.append(message)

        return jsonify(email_address=email_address, messages=cleaned_messages)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(error=str(e)), 500


# Insert the user data into the database if it's not there
@app.route('/save-user-data', methods=['POST'])
def save_user_data():
    email_address = request.json['email_address']
    user_data = User().save_user_data(email_address)
    return jsonify(user_data)


# Update the content of the tags
@app.route('/update-tags', methods=['POST'])
def update_tags():
    email_address = request.json['email_address']
    module_change = request.json['module_change']
    travel_leave = request.json['travel_leave']
    sick_leave = request.json['sick_leave']

    result = User().update_tags(email_address, module_change, travel_leave, sick_leave)

    if result:
        return jsonify({'message': 'Tags updated successfully!'}), 200
    else:
        return Response(status=304)


def send_email(access_token, to_address, subject, content):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    body = {
        'message': {
            'subject': subject,
            'body': {
                'contentType': 'HTML',
                'content': content
            },
            'toRecipients': [
                {
                    'emailAddress': {
                        'address': to_address
                    }
                }
            ]
        }
    }
    response = requests.post(f'{BASE_URL}sendMail', headers=headers, json=body)
    response.raise_for_status()


@app.route('/send-response', methods=['POST'])
def send_response():
    try:
        to_address = request.json['to_address']
        tag_content = request.json['tag_content']
        subject = request.json['subject']

        send_email(session['access_token'], to_address, subject, tag_content)
        return jsonify({'message': 'Email sent successfully!'}), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify(error=str(e)), 500


@app.route('/.well-known/<path:path>')
def serve_well_known(path):
    return send_from_directory('.well-known', path)


if __name__ == '__main__':
    # set debug to True when in development mode
    app.run(debug=True)
