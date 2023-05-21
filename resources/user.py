import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
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


