from threading import Thread, Condition
from time import sleep
from random import uniform

class GenericMember(Thread):
    def __init__(self, pid, gym):
        super().__init__(target=self.run)
        self.pid = pid
        self.condition = Condition()
        self.locker_number = -1
        self.attempts = 0
        self.eid = -1
        self.gym = gym
        self.list_of_excercises=[]

    def run(self):
        self.enter_gym()
        if self.locker_number != -1:
            sleep(uniform(2,3))
            self.execute_training_plan()
            sleep(uniform(3,4))
        self.exit_gym()

    def execute_training_plan(self):
        for ex in self.list_of_excercises:
            self.train(ex,1,10)

    def train(self, equipment, min_occupation_time, max_occupation_time):
        equipment.start_training(self)
        sleep(uniform(min_occupation_time,max_occupation_time))
        equipment.stop_training(self)

    def exit_gym(self):
        if self.locker_number != -1:
            self.gym.reception.release_locker(self)
            print(f"Wychodzę po treningu {self.pid}")
        else:
            print(f"Nie chce mi się czekać {self.pid}")

    def enter_gym(self):
        self.locker_number = self.gym.reception.ask_to_enter(self)


class CardioFreak(GenericMember):
    def __init__(self, pid, gym):
        super().__init__(pid, gym)
        self.list_of_excercises = [
            self.gym.bicycles,
            self.gym.ergometers,
            self.gym.threadmills,
            self.gym.elipticals
            ]

class CallisctenicsEnjoyer(GenericMember):
    def __init__(self, pid, gym):
        super().__init__(pid, gym)
        self.list_of_excercises = [
            self.gym.threadmills,
            self.gym.pullup_bars,
            self.gym.ergometers,
            self.gym.crunch_machines,
            ]