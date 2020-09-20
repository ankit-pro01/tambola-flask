from flask import Flask
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, send, emit, join_room, leave_room


app = Flask(__name__, static_folder='../build', static_url_path='/')

socketIo = SocketIO(app, cors_allowed_origins="*")

app.debug = True
app.host = 'localhost'

app.config['SECRET_KEY'] = 'replaceable'
app.config['MONGO_URI'] = "mongodb+srv://ankit:ankit@cluster1.pydvi.mongodb.net/AwesomeData?retryWrites=true&w=majority"

mongo = PyMongo(app)

from flask1 import routes