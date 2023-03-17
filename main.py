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


if __name__ == '__main__':
    # set debug to True when in development mode
    app.run(debug=True)
