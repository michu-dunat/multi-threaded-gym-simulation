#!/usr/bin/env python

import threading
from time import sleep
from gym import Gym
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
#from threading import Lock
from members import GenericMember, GymChad, CallisctenicsEnjoyer, CardioFreak
from random import random, sample, randint
from random import uniform

gym = Gym()

class Host(threading.Thread):
    def __init__(self) -> None:
        super().__init__(target=self.invite_following_customers)
        self.MEMBERS = list()
        global gym
        self.gym = gym
        self.condition = threading.Condition()
        self.gym_member_id = 0

    def add_member(self, m):
        with self.condition:
            self.MEMBERS.append(m)
            self.MEMBERS[-1].start()
            
    def remove_member(self, m):
        with self.condition:
            self.MEMBERS.remove(m)
    
    def invite_following_customers(self):
        global gym
        sleep(20)
        while True:
            sleep(uniform(2,3))
            rnd = randint(0, 100)
            if rnd % 3 == 0:
                self.add_member(CallisctenicsEnjoyer(self.gym_member_id, gym, self))
                self.gym_member_id+=1
            elif rnd % 3 == 1:
                self.add_member(CardioFreak(self.gym_member_id,gym, self))
                self.gym_member_id+=1
            else:
                self.add_member(GymChad(self.gym_member_id,gym, self))
                self.gym_member_id+=1
    
    def gym_members_statuses_to_dict(self) -> dict:
        with self.condition:
            members =[{
                "status": m.status,
                "type": m.type,
            } for m in self.MEMBERS]
                
            
            resources = {
                "total_weight": gym.total_weights.avaliable_weight,
                "threadmills": gym.threadmills.array,
                "ergometers": gym.ergometers.array,
                "pullup_bars": gym.pullup_bars.array,
                "crunch_machines": gym.crunch_machines.array,
                "elipticals": gym.elipticals.array,
                "bicycles": gym.bicycles.array,
                "benchpresses": gym.benchpresses.array,
                "smith": gym.smith.array,
                "deadlift": gym.deadlift.array,
            }

            x = {
                "currentMembersCount": len(self.MEMBERS),
                "members": members,
                "resources": resources,
            }

            return x

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
socketio = SocketIO(app)
MEMBERS_LIMIT = 10
MEMBERS = list()
TRIGGER_END_EVENT = False
gym_member_id = 0

gym_host = Host()
gym_host.start()

@app.route('/')
def index():
    return render_template('index.html', context={'members': gym_host.MEMBERS})

@socketio.on('run')
def run():
    global MEMBERS_LIMIT, MEMBERS, TRIGGER_END_EVENT, gym_member_id, gym, gym_host
    for i in range(0, MEMBERS_LIMIT+5, 3):
        gym_host.add_member(CallisctenicsEnjoyer(i, gym, host=gym_host))
        gym_host.add_member(CardioFreak(i+1, gym, host=gym_host))
        gym_host.add_member(GymChad(i+2, gym, host=gym_host))
        gym_host.MEMBERS = sample(gym_host.MEMBERS, len(gym_host.MEMBERS))
        gym_host.gym_member_id = i+3
    socketio.run(app)
    
@socketio.on('connection')
def connected(json):
    print("Initialized connection")
    print(json)
    socketio.emit('updating', {
        "start":"gym",
        "gymMembers": len(gym_host.MEMBERS)
    })

@socketio.on("update_received")
def request_update():
    socketio.emit('request_update')

@socketio.on('request_update_gym')
def update_view():
    global gym_host
    socketio.emit("updating", gym_host.gym_members_statuses_to_dict())

if (__name__ == "__main__"):
    run()

