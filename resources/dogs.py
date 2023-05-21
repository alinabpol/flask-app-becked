import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

dogs = Blueprint('dogs', 'dog')


from flask_login import login_required, current_user

@dogs.route('/', methods=['GET'])
def dogs_index():
    result = models.Dog.select()
    print('result of dog select query')
    print(result)

    dog_dicts = [model_to_dict(dog) for dog in result]
    
    return jsonify({
        'data': dog_dicts,
        'message': f"Successfully found {len(dog_dicts)} dogs",
        'status': 200
    }), 200

@dogs.route('/<id>', methods=['GET'])
def get_one_dog(id):
    dog = models.Dog.get_by_id(id)
    print(dog)
    return jsonify(
        data=model_to_dict(dog),
        message="Success!!!",
        status=200
    ), 200


@dogs.route('/', methods=['POST'])
@login_required
def create_dogs():
    payload = request.get_json() # this is like req.body express 
    print(payload)
    new_dog = models.Dog.create(name=payload['name'], age=payload['age'], breed=payload['breed'])
    print(new_dog) # just prints the ID -- check sqlite3 to see the data 

    dog_dict = model_to_dict(new_dog)
    return jsonify(
        data=dog_dict,
        message="Sucessfully created dog!",
        status=201
    ), 201


# DELETE / DESTROY 
# DELETE api/v1/dogs/<id>
@dogs.route('/<id>', methods=['DELETE'])
@login_required
def delete_dog(id):
    delete_query = models.Dog.delete().where(models.Dog.id == id)
    nums_of_rows_deleted = delete_query.execute()
    print(nums_of_rows_deleted)


    return jsonify(
        data={},
        message=f"Successfully deleted {nums_of_rows_deleted} dog with id {id}",
        status=200
    ), 200

# PUT UPDATE ROUTE 
# PUT api/v1/dogs/<id>
@dogs.route('/<id>', methods=['PUT'])
@login_required
def update_dog(id):
    payload = request.get_json()
    print(payload)

    
    models.Dog.update(**payload).where(models.Dog.id == id).execute() 


    return jsonify(
        data=model_to_dict(models.Dog.get_by_id(id)), # same as lines 107, 108 
        message="resource updated successfully",
        status=200
    ),200
