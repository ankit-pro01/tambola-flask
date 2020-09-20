from flask import render_template, jsonify, request
from flask1 import app
from flask1 import mongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from werkzeug.security import generate_password_hash, check_password_hash 



@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/add')
def add():
    id = mongo.db.user.insert_one({'name': 'abc', 'email': 'abc@domain.com', 'pwd': '####'})
    resp = jsonify("user added successfully")
    resp.status_code = 200
    return resp


@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }

    resp = jsonify(message)
    resp.status_code = 404
    return resp 

    

