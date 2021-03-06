from threading import Thread, Condition
from time import sleep
from datetime import datetime
from random import randint, uniform, sample

class GenericMember(Thread):
    def __init__(self, pid, gym, dw, gm_type, host):
        super().__init__(target=self.run)
        self.pid = pid
        self.condition = Condition()
        self.locker_number = -1
        self.attempts = 0
        self.eid = -1
        self.desired_weight = dw
        self.gym = gym
        self.list_of_excercises=[]
        self.type = gm_type
        self.host = host
        self.status = "Entering gym"
        self.total_sleep = 0
        self.remaining_sleep = 0
        self.is_remaiming_time_set = False

        if randint(0,1) == 0:
            self.sex = "m"
        else: 
            self.sex = "f"

    def gsleep(self, sleeping_period):
        self.total_sleep = round(sleeping_period,2)
        self.remaining_sleep = round(sleeping_period,2)
        while not self.remaining_sleep <= 0:
            if self.remaining_sleep > 0.2:
                sleep(0.2)
                self.remaining_sleep -= 0.2
                self.remaining_sleep = round(self.remaining_sleep,2)
            else:
                sleep(self.remaining_sleep)
                self.remaining_sleep -= self.remaining_sleep
                self.total_sleep = 0

    def run(self):
        self.enter_gym()
        if self.locker_number != -1:
            self.gsleep(uniform(2,3))
            self.execute_training_plan()
            self.gsleep(uniform(3,4))
        self.exit_gym()

    def execute_training_plan(self):
        for ex in self.list_of_excercises:
            self.train(ex,8,10)

    def train(self, equipment, min_occupation_time, max_occupation_time):
        equipment.start_training(self)
        self.gsleep(uniform(min_occupation_time,max_occupation_time))
        equipment.stop_training(self)

    def exit_gym(self):
        if self.locker_number != -1:
            self.gym.reception.release_locker(self)
            print(f"[{datetime.now()}] {self}: Wychodz?? po treningu")
            self.status = "Leaving after training"
            self.gsleep(5)
        else:
            print(f"[{datetime.now()}] {self}: Nie chce mi si?? czeka??")
            self.status = "I got bored waiting for locker... quitting"
            self.gsleep(5)
        self.host.remove_member(self)

    def enter_gym(self):
        self.locker_number = self.gym.reception.ask_to_enter(self)

    def __str__(self):
        return f"Member {self.type} {self.pid}"


class CardioFreak(GenericMember):
    def __init__(self, pid, gym, host):
        super().__init__(pid, gym, randint(40,70), "CardioFreak", host=host)
        l = [
            self.gym.bicycles,
            self.gym.ergometers,
            self.gym.threadmills,
            self.gym.elipticals,
            self.gym.deadlift
        ]
        self.list_of_excercises = sample(l, len(l))

class CallisctenicsEnjoyer(GenericMember):
    def __init__(self, pid, gym, host):
        super().__init__(pid, gym, randint(85,100), "CallistenicsEnj", host=host)
        l = [
            self.gym.threadmills,
            self.gym.pullup_bars,
            self.gym.ergometers,
            self.gym.benchpresses,
            self.gym.crunch_machines,
        ]
        self.list_of_excercises = sample(l, len(l))

class GymChad(GenericMember):
    def __init__(self, pid, gym, host):
        super().__init__(pid, gym, randint(100,200), "GymChad", host=host)
        l = [
            self.gym.pullup_bars,
            self.gym.crunch_machines,
            self.gym.benchpresses,
            self.gym.deadlift,
            self.gym.smith
        ]
        self.list_of_excercises = sample(l, len(l))