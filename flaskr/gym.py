from reception import Reception
from resources import Threadmill, Benchpress, Ergometer, PullUpBar, Eliptical, Bicycle, CrunchMachine, Weight, Deadlift, Smith_machine

LOCKER_COUNT = 10

class Gym:
    def __init__(self) -> None:
        global LOCKER_COUNT
        self.reception = Reception(LOCKER_COUNT)

        self.total_weights = Weight(500)        
        self.threadmills = Threadmill(2)
        self.ergometers = Ergometer(2)
        self.pullup_bars = PullUpBar(2)
        self.crunch_machines = CrunchMachine(2)
        self.elipticals = Eliptical(2)
        self.bicycles = Bicycle(2)
        self.benchpresses = Benchpress(3, self.total_weights)
        self.smith = Smith_machine(2, self.total_weights)
        self.deadlift = Deadlift(2, self.total_weights)