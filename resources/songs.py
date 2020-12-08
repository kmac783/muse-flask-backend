import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

song = Blueprint('songs', 'song')

##GET ROUTE
@song.route('/', methods=["GET"])
def get_all_songs():
    try:
        song = [model_to_dict(song) for song in models.Song.select()]
        print(song)
        return jsonify(data=song, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

##SHOW ROUTE
@song.route('/<id>', methods=["GET"])
def get_one_song(id):
    print(id, 'reserved word?')
    song = models.Song.get_by_id(id)
    print(song.__dict__)
    return jsonify(data=model_to_dict(song),
                   status={
                       "code": 200,
                       "message": "Success"
                   })


##POST ROUTE
@song.route('/', methods=["POST"])
def create_song():
    # see request payload anagolous to req.body in express
    payload = request.get_json()
    print(type(payload), 'payload')
    song = models.Song.create(**payload)
    # see the object
    print(song.__dict__)
    # Look at all the methods
    print(dir(song))
    # Change the model to a dict
    print(model_to_dict(song), 'model to dict')
    song_dict = model_to_dict(song)
    return jsonify(data=song_dict, status={"code": 201, "message": "Success"})

##UPDATE ROUTE
@song.route('/<id>', methods=["PUT"])
def update_song(id):
    payload = request.get_json()
    query = models.Song.update(**payload).where(models.Song.id == id)
    query.execute()
    return jsonify(data=model_to_dict(models.Song.get_by_id(id)),
                   status={
                       "code": 200,
                       "message": "resource updated successfully"
                   })

##DELETE ROUTE
@song.route('/<id>', methods=["Delete"])
def delete_song(id):
    query = models.Song.delete().where(models.Song.id == id)
    query.execute()
    return jsonify(data='resource successfully deleted',
                   status={
                       "code": 200,
                       "message": "resource deleted successfully"
                   })