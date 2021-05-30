#!/usr/bin/env python

from gym import Gym
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
#from threading import Lock
from resources import Locker, LockContextManager
from members import GenericMember, GymChad, CallisctenicsEnjoyer, CardioFreak
from random import sample

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
socketio = SocketIO(app)
MEMBERS_LIMIT = 10
MEMBERS = list()

@app.route('/')
def index():
    return render_template('index.html', context={'members': MEMBERS})

@socketio.on('run')
def run():
    global MEMBERS_LIMIT, MEMBERS
    gym = Gym()
    for i in range(0, MEMBERS_LIMIT+5, 3):
        MEMBERS.append(CallisctenicsEnjoyer(i, gym))
        MEMBERS.append(CardioFreak(i+1, gym))
        MEMBERS.append(GymChad(i+2, gym))
        MEMBERS = sample(MEMBERS, len(MEMBERS))
    for m in MEMBERS:
        m.start()
    socketio.run(app)
    
@socketio.on('connection')
def connected(json):
    print("Initialized connection")
    global MEMBERS_LIMIT

if (__name__ == "__main__"):
    run()

