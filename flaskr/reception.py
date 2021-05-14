from resources import Locker
from threading import Condition
import time

class Reception():
    def __init__(self, locker_count):
        self.condition = Condition()
        self.lockers = [True for _ in range(locker_count)]
        self.time = time.time()

    def ask_to_enter(self, gym_member):
        with self.condition:
            while not any(self.lockers):
                if gym_member.attempts > 10:
                    return -1
                gym_member.attempts += 1
                self.condition.wait(1)

            for i in range(len(self.lockers)):
                if self.lockers[i]:
                    self.lockers[i] = False
                    print(f"[{time.time() - self.time}] Odebrałem szafkę: {gym_member.pid}")
                    return i            

    def release_locker(self, gym_member):
        with self.condition:
            if gym_member.locker_number == None:
                print("Err")
            else:
                self.lockers[gym_member.locker_number] = True
                self.condition.notify_all()
            pass