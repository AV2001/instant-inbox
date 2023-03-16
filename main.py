from flask import Flask, render_template
from models import User

app = Flask(__name__)


# Rendering the index.html
@app.route('/')
def home():
    return render_template('index.html', title='Home')


# Rendering the about.html
@app.route('/about/')
def about():
    return render_template('about.html', title='About')


@app.route('/create-account/', methods=['POST'])
def create_account():
    # Insert data from create account form to the database
    return User().create_account()


@app.route('/login/', methods=['POST'])
def login():
    # Check whether credentials entered in log in form match with those in the database
    return User().login()


if __name__ == '__main__':
    # set debug to True when in development mode
    app.run(debug=True)
