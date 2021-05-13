from flask import Flask
#from threading import Lock
from resources import Locker
from members import GenericMember
from reception import Reception

app = Flask(__name__)

MEMBERS_LIMIT = 3
LOCKERS = [Locker() for i in range(MEMBERS_LIMIT)]
# locker_lock = Lock()


@app.route('/')
def index():
    return "Gym application"


def run():
    r = Reception(LOCKERS)
    members = [GenericMember(i, r) for i in range(MEMBERS_LIMIT+10)]
    for m in members:
        m.start()


if (__name__ == "__main__"):
    run()