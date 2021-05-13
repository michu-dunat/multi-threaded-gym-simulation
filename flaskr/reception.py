from resources import Locker

class Reception():
    def __init__(self, LOCKERS):
        self.LOCKERS = LOCKERS
        pass

    def ask_to_enter(self):
        for x in self.LOCKERS:
            if x.status == "free":
                return x
        else:
            return False