import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
user = Blueprint('users', 'user', url_prefix='/user')

@user.route('/register', methods=["POST"])
def register():

    payload = request.get_json()

    payload['email'] = payload['email'].lower()
    try:
        # Find if the user already exists?
        models.User.get(models.User.email == payload['email']) # model query finding by email
        return jsonify(data={}, status={"code": 401, "message": "A user with that name already exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password']) # bcrypt line for generating the hash
        user = models.User.create(**payload) # put the user in the database
                                            

        # starts user session
        login_user(user)

        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))
        # delete the password before we return it, because we don't need the client to be aware of it
        del user_dict['password']

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

# login route
@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print('payload:', payload)
    try:
        user = models.User.get(models.User.username == payload['username']) # Try to find the user by thier email
        user_dict = model_to_dict(user) # if you find the User model convert in to a dictionary so you can edit and jsonify it
        if(check_password_hash(user_dict['password'], payload['password'])): # use bcrypt to check password and see if input password matches
            del user_dict['password'] # delete the password since the client doesn't need it
            login_user(user) # set up the session
            print(user, ' this is user')
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"}) # respond to the client
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})

@user.route('/logout', methods=["GET"])
def logout():
    logout_user() # this line will need to be imported
    return jsonify(
        data={},
        status=200,
        message= 'successful logout'
    ), 200