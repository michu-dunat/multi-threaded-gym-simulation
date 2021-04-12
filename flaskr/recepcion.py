from resources import Locker
from app import LOCKERS, locker_lock

class Reception():
    def __init__(self):
        pass

    def ask_to_enter(self):
        locker_lock.acquire()
        for x in LOCKERS:
            if x.status == "free":
                return x
        else:
            return False

rec = Reception()

print(rec.ask_to_enter())