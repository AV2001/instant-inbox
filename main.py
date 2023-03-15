from flask import Flask, render_template, request, jsonify
from models import User

app = Flask(__name__)

# Routes
@app.route('/')
def home():
    return render_template('index.html', title='Home')


# Rendering the about.html
@app.route('/about/')
def about():
    return render_template('about.html', title='About')


@app.route('/create-account/', methods=['POST'])
def create_account():
    # Method for inserting data from create account form to the database
    return User().create_account()


if __name__ == '__main__':
    # set debug to True when in development mode
    app.run(debug=True)
