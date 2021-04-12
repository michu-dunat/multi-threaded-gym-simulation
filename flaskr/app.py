from flask import Flask
from threading import Lock
from resources import Locker

app = Flask(__name__)

MEMBERS_LIMIT = 10
LOCKERS = [Locker() for i in range(MEMBERS_LIMIT)]
locker_lock = Lock()


@app.route('/')
def index():
    return "Gym application"


def run():
    pass

if (__name__ == "__main__"):
    run()