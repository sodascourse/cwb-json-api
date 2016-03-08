import os

from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    DEBUG = int(os.environ.get('DEBUG', '0')) != 0
    app.run(debug=DEBUG)
