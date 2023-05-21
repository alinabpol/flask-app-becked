from flask import Flask, jsonify, g

from resources.dogs import dogs
import models

from flask_cors import CORS
from flask_login import LoginManager, current_user

DEBUG = True
PORT = 8000

# Login manager
login_manager = LoginManager()

# Initialize an instance of the Flask class.~
# This starts the website!
app = Flask(__name__)

app.secret_key = "LJAKLJLKJJLJKLSDJLKJASD" # Need this to encode the session
login_manager.init_app(app) # set up the sessions on the app

@login_manager.user_loader # decorator function, that will load the user object whenever we access the session, we can get the user
# by importing current_user from the flask_login
def load_user(userid):
    try:
        return models.user.get(models.user.id == userid)
    except models.DoesNotExist:
        return None

CORS(dogs, origins=['http://localhost:3000'],
supports_credentials=True)

CORS(app)

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