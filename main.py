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


if __name__ == '__main__':
    # set debug to True when in development mode
    app.run(debug=True)
