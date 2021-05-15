from gym import Gym
from flask import Flask
#from threading import Lock
from resources import Locker, LockContextManager
from members import GenericMember, CallisctenicsEnjoyer, CardioFreak

app = Flask(__name__)

MEMBERS_LIMIT = 4

@app.route('/')
def index():
    return "Gym application"

def run():
    global MEMBERS_LIMIT
    gym = Gym()
    members = [CardioFreak(i, gym)  for i in range(MEMBERS_LIMIT//2)]
    for i in range(MEMBERS_LIMIT//2, MEMBERS_LIMIT+5):
        members.append(CallisctenicsEnjoyer(i, gym))
    for m in members:
        m.start()


if (__name__ == "__main__"):
    run()
