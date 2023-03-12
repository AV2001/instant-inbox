from flask import Flask, render_template, request, jsonify
from models import User

app = Flask(__name__)

# Routes
@app.route('/')
def home():
    return render_template('index.html', title='Home')


@app.route('/about/')
def about():
    return render_template('about.html', title='About')


@app.route('/create-account/', methods=['POST'])
def create_account():
    return User().create_account()


if __name__ == '__main__':
    # set debug to True when in development mode
    app.run(debug=True)
