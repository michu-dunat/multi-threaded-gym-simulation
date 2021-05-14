from gym import Gym
from flask import Flask
#from threading import Lock
from resources import Locker, LockContextManager
from members import GenericMember

app = Flask(__name__)

MEMBERS_LIMIT = 3

@app.route('/')
def index():
    return "Gym application"

def run():
    global MEMBERS_LIMIT
    gym = Gym()
    members = [GenericMember(i, gym) for i in range(MEMBERS_LIMIT+10)]
    for m in members:
        m.start()


if (__name__ == "__main__"):
    run()
