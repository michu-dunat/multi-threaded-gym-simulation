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
        pass

    def run(self):
        self.enter_gym()
        if self.locker_number != -1:
            self.execute_training_plan()
        self.exit_gym()

    def execute_training_plan(self):
        sleep(uniform(1,2))
        self.gym.threadmills.start_training(self)
        sleep(uniform(4,10))
        self.gym.threadmills.stop_training(self)
        sleep(uniform(1,2))

    def exit_gym(self):
        if self.locker_number != -1:
            self.gym.reception.release_locker(self)
            print(f"Wychodzę po treningu {self.pid}")
        else:
            print(f"Nie chce mi się czekać {self.pid}")

    def enter_gym(self):
        self.locker_number = self.gym.reception.ask_to_enter(self)
