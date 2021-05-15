from reception import Reception
from resources import Threadmill, Ergometer, PullUpBar, Eliptical, Bicycle, CrunchMachine

LOCKER_COUNT = 10

class Gym:
    def __init__(self) -> None:
        global LOCKER_COUNT
        self.reception = Reception(LOCKER_COUNT)
        self.threadmills = Threadmill(2)
        self.ergometers = Ergometer(2)
        self.pullup_bars = PullUpBar(2)
        self.crunch_machines = CrunchMachine(2)
        self.elipticals = Eliptical(2)
        self.bicycles = Bicycle(2)