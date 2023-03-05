from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    # set debug to True when in development mode
    app.run(debug=True)
