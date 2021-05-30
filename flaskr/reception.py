from resources import Locker
from threading import Condition
import time

class Reception():
    def __init__(self, locker_count):
        self.condition = Condition()
        self.female_lockers = [True for _ in range(locker_count//2)]
        self.male_lockers = [True for _ in range(locker_count//2)]
        self.time = time.time()

    def ask_to_enter(self, gym_member):
        if gym_member.sex == "f":
            return self.aquire_locker(gym_member,self.female_lockers)
        else:
            return self.aquire_locker(gym_member,self.male_lockers)

    def aquire_locker(self, gym_member, lockers):
        with self.condition:
            while not any(lockers):
                if gym_member.attempts > 10:
                    return -1
                gym_member.attempts += 1
                self.condition.wait(1)

            for i in range(len(lockers)):
                if lockers[i]:
                    lockers[i] = False
                    if gym_member.sex == "f":
                        print(f"[{time.time() - self.time}] Odebrałam szafkę z szatni {gym_member.sex}: {gym_member.pid}")
                    else:
                        print(f"[{time.time() - self.time}] Odebrałem szafkę z szatni {gym_member.sex}: {gym_member.pid}")

                    return i            

    def release_locker(self, gym_member):
        if gym_member.sex == "f":
            self.release(gym_member,self.female_lockers)
        else:
            self.release(gym_member,self.male_lockers)

    def release(self, gym_member, lockers):
        with self.condition:
            if gym_member.locker_number == None:
                print("Err")
            else:
                lockers[gym_member.locker_number] = True
                self.condition.notify_all()
            pass