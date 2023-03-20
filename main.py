from flask import Flask, request, redirect, render_template, session, url_for
from msal import ConfidentialClientApplication
from uuid import uuid4
import secrets
import requests
from dotenv.main import load_dotenv
import os


from models import User


load_dotenv()

APPLICATION_ID = os.environ['APPLICATION_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

print(APPLICATION_ID)
print(CLIENT_SECRET)


app = Flask(__name__)


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


if __name__ == '__main__':
    # set debug to True when in development mode
    app.run(debug=True)
