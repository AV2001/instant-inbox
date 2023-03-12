from flask import Flask, render_template
from user.models import User

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', title='Home')


@app.route('/about/')
def about():
    return render_template('about.html', title='About')


@app.route('/user/create-account', methods=['POST'])
def create_account():
    return User().create_account()


if __name__ == '__main__':
    # set debug to True when in development mode
    app.run(debug=True)
