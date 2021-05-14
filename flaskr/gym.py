from reception import Reception
from resources import Threadmill, Ergometer

LOCKER_COUNT = 10

class Gym:
    def __init__(self) -> None:
        global LOCKER_COUNT
        self.reception = Reception(LOCKER_COUNT)
        self.threadmills = Threadmill(2)
        self.ergometers = Ergometer(2)