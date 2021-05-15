from random import uniform
from threading import Condition
from time import sleep


class LockContextManager():
    def __init__(self) -> None:
        pass

    def __enter__(self):
        print("entering")

    def __exit__(self, type, value, traceback):
        print("exiting")

class Locker:
    def __init__(self):
        self.owner = None
        self.condition = Condition()

    def release(self):
        with self.condition:
            self.owner = None
            self.condition.notify_all()

    def assign_or_wait(self, gym_member):
        with self.condition:
            if self.owner is not None:
                gym_member.condition.wait()
                return False
            else:
                self.owner = gym_member
                return True


class CardioEquipement:
    def __init__(self, eq_count, name):
        self.condition = Condition()
        self.array = [True for _ in range(eq_count)]
        self.name = name
    
    def __str__(self) -> str:
        return self.name

    def start_training(self, g):
        with self.condition:
            while not any(self.array):
                self.condition.wait()
        
            for eq in range(len(self.array)):
                if self.array[eq]:
                    print(f"{g.pid} Took {self}")
                    self.array[eq] = False 
                    return eq

    def stop_training(self, g):
        with self.condition:
            print(g.pid, f" Zwolnił {self}")
            self.array[g.eid] = True
            self.condition.notify_all()
            

class Threadmill(CardioEquipement):
    def __init__(self, eq_count):
        super().__init__(eq_count, "Threadmill")


class Ergometer(CardioEquipement):
    def __init__(self, eq_count):
        super().__init__(eq_count, "Ergometer")


class Benchpress:
    def __init__(self):
        pass


class Bicycle(CardioEquipement):
    def __init__(self, eq_count):
        super().__init__(eq_count, "Bicycle")

class CrunchMachine(CardioEquipement):
    def __init__(self, eq_count):
        super().__init__(eq_count, "Crunch Machine")


class Eliptical(CardioEquipement):
    def __init__(self, eq_count):
        super().__init__(eq_count, "Eliptical")


class Bar_position:
    def __init__(self):
        pass


class Excercise_position:
    def __init__(self):
        pass


class Fitness_room:
    def __init__(self):
        pass


class PullUpBar(CardioEquipement):
    def __init__(self, eq_count):
        super().__init__(eq_count, "Pull Up Bar")