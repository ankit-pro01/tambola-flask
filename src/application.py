
from flask import Flask

from flask import render_template, jsonify, request

from flask_socketio import SocketIO, send, emit, join_room, leave_room

from time import localtime, strftime
import random

import numpy as np

import os

# app = Flask(__name__,static_folder='../build', static_url_path='/')

app = Flask(__name__, static_url_path='', static_folder="build", template_folder="build")

socketIo = SocketIO(app, cors_allowed_origins="*")
        

ROOMS = []

KING = {}

NAMES = []

check_list = []


class Host():
    def __init__(self):
        pass
    def getList(self):
        return [i for i in range(0,100)]
        



@socketIo.on('join')
def on_join(data):
    print("inside room")
    print(data)
    room = data['room']
    name = data['name']

    print("joining room is : ", room)
    
    if room in ROOMS:
        if name not in NAMES:
            join_room(room)
            emit('join', { 'msg' : data['name'] + " has joined the room ", 'error' : ''}, room = data['room'])
        else:
            emit('join', { 'error' : 'please select different username'},)
    else:
        emit('join', { 'error' : room + ' room is not there, please create '},)





@socketIo.on('newRoom')
def on_newRoom(data):
    print("inside new room")
    print(data)
    room = data['room']
    name = data['name']
    
    ROOMS.append(room)
    KING[room] = data['name']
    print(KING)
    join_room(room)

    if name == KING[room]:
        king_flag = True
    else:
        king_flag = False

    print(king_flag)

    emit('join', { 'msg' : data['name'] + " has joined the room ", 'error' : ''}, room = data['room'])

    emit('king', {'king' : True, "room_id": room}, room = data['room'])



@socketIo.on('claim')
def on_claim(data):
    List2 = data['number_list']
    room = data['room']
    name = data['claimer']
    check =  all(item in check_list for item in List2)
    print(check_list)
    print(List2)
    print("room name is " + room)
    if check:
        print("yes")
        emit('claim', { 'msg' : "YES", 'claimer' : name}, room = room)
    else:
        print("Warning")
        emit('claim', { 'msg' : "NO", 'claimer' : name}, room = room)



def get_arr():
    return random.sample(range(1, 101), 18)



@socketIo.on("message")
def handleMessage(data):
    print("inside message")
    print(data)
    send({'msg' : data['msg'], 'username': data['name'], 'time_stamp': strftime("%b-%d %I:%M%p", localtime())}, room = data['room'])
    return None

@socketIo.on("chits")
def distribute_chits():
    chit = get_arr()
    print(chit)
    emit('chits',{'chit' : chit})
    return None
    

@socketIo.on("start")
def handleStart(data):
    print("starting..")
    print(data)
    host = Host()
    list1 = host.getList()
    random.shuffle(list1)
    check_list.append(list1[-1])
    
    print(check_list)
    #send({'username': 'host', 'msg' :list1.pop()}, room = data['room'])
    emit('start',{'username': 'host', 'msg' :list1.pop()}, room = data['room'])


@socketIo.on("playAgain")
def playAgain(data):
    print("playing again")
    check_list[:] = []
    emit("playAgain", {'msg': "playAgain"})
    

@app.route('/')
def hello():
    return app.send_static_file('index.html')



@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }

    resp = jsonify(message)
    resp.status_code = 404
    return resp 


if __name__ == '__main__':
    # socketIo.run(app)
    app.run()
