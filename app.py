from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db,db,Users,Movies
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
db.init_app(app)

with app.app_context():
    db_drop_and_create_all()


@app.route('/', methods=['GET'])
def firstview(): 

    return jsonify({ 
        'success': True, 
        'Hello' : "Welcome" 
        })



@app.route('/viewusers', methods=['GET'])
def viewusers(): 
    userslist = Users.query.all()
    users = []
    for user in userslist:
        users.append(user.format())
    return jsonify({ 
        'success': True, 
        'users': users 
        })

@app.route('/createuser/<name>/<email>/<gender>', methods=['POST'])
@requires_auth('post:users')
def createuser(payload,name, email, gender):
    try:
        new_user = Users(name=name, email=email, gender=gender)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'New user added successfully'
        })
    except:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred. Could not add new user.'
        })

@app.route('/updateuser/<id>/<name>', methods=['PATCH'])
@requires_auth('patch:users')
def updateuser(id, name):
    try:
        user = Users.query.filter_by(id=id).first()
        user.name = name
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'User updated successfully'
        })
    except:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred. Could not update user.'
        })

@app.route('/deleteuser/<id>', methods=['DELETE'])
@requires_auth('delete:users')
def deleteuser(id):
    try:
        user = Users.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        })
    except:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred. Could not delete user.'
        })

@app.route('/viewmovies', methods=['GET'])
def viewmovies(): 
    movieslist = Movies.query.all()
    movies = []
    for movie in movieslist:
        movies.append(movie.format())
    return jsonify({ 
        'success': True, 
        'movies': movies 
        })


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
    
@app.errorhandler(400)
def not_found(error):
    return jsonify({
        'success':False,
        'error':400,
        'message':'invalid information sent by the client '
    }),400

@app.errorhandler(405)
def not_found(error):
    return jsonify({
        'success':False,
        'error':405,
        'message':'Not Allowed response'
    }),405

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success':False,
        'error':404,
        'message':'resource not found'
    }),404

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    Receive the raised authorization error and propagates it as response
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


if __name__ == '__main__':
    app.run()