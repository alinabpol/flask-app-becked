import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user', url_prefix='/user')
def register():
    payload = request.get_json()

    payload['email'] = payload['email'].lower()
    try:
        #find if user already exists?
        models.user.get(models.user.email == payload['email'])
        return jsonify(data={}, status={"code": 401, "message": "USER WITH THAT NAME ALREADY EXISTS!"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.user.create(**payload)

        login_user(user)

        user_dict = model_to_dict(user)

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print('payload:', payload)
    try:
        user = models.user.get(models.user.email == payload['email']) 
        user_dict = model_to_dict(user) 
        if(check_password_hash(user_dict['password'], payload['password'])): 
            del user_dict['password'] 
            login_user(user) 
            print(user, ' this is user')
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"}) 
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    
# at the botton of the file
@user.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return jsonify(
        data={},
        status=200,
        message= 'successful logout'
    ), 200