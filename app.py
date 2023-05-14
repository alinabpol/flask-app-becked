from flask import Flask, jsonify, g

from resources.dogs import dogs
import models

from flask_cors import CORS

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.~
# This starts the website!
app = Flask(__name__)

CORS(dogs, origins=['http://localhost:3000'],
supports_credentials=True)



@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


app.register_blueprint(dogs, url_prefix='/api/v1/dogs')


# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'hi'

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)