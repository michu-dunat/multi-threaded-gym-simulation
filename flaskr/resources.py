from random import uniform
from threading import Condition
from time import sleep
from datetime import datetime


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
                    self.take_info(g)
                    #print(f"[{datetime.now()}]{g} took {self}")
                    self.array[eq] = False 
                    return eq

    def stop_training(self, g):
        with self.condition:
            #print(g.pid, f" Zwolnił {self}")
            self.release_info(g)
            self.array[g.eid] = True
            self.condition.notify_all()

    def take_info(self, g):
        print(f"[{datetime.now()}] {g} took {self}")

    def release_info(self, g):
        print(f"[{datetime.now()}] {g} released {self}")


class Threadmill(CardioEquipement):
    def __init__(self, eq_count):
        super().__init__(eq_count, "Threadmill")


class Ergometer(CardioEquipement):
    def __init__(self, eq_count):
        super().__init__(eq_count, "Ergometer")



class FreeWeightEx:
    def __init__(self, eq_count, name, all_plates):
        self.condition = Condition()
        self.array = [True for _ in range(eq_count)]
        self.name = name
        self.weight = all_plates
    
    def __str__(self) -> str:
        return self.name

    def start_training(self, g):
        with self.condition:
            while not any(self.array):
                self.condition.wait()
                print(f"[{datetime.now()}] {g} waiting for {self}")
                g.status = f"Waiting for {self}"
            for eq in range(len(self.array)):
                if self.array[eq]:
                    #print(f"{g.pid} Took {self}")
                    self.array[eq] = False
                    break
        with self.weight.condition:
            while not self.weight.avaliable_weight - g.desired_weight > 0:
                print(f"[{datetime.now()}] {g} could not start lifting on {self}, missing plates, AVALIABLE: {self.weight.avaliable_weight} -> WANTED TO TAKE: {g.desired_weight}")
                g.status = f"Waiting on plates for {self}"
                self.weight.condition.wait()
            self.weight.avaliable_weight -= g.desired_weight
        self.take_info(g)
        return eq

    def stop_training(self, g):
        with self.weight.condition:
            self.weight.avaliable_weight += g.desired_weight
            self.release_info(g)
            self.weight.condition.notify_all()

        with self.condition:
            self.array[g.eid] = True
            self.condition.notify_all()

    def take_info(self, g):
        print(f"[{datetime.now()}] {g} took {self}, currently avaliable weight: {self.weight.avaliable_weight}")
        g.status = f"Works out on {self}"
    def release_info(self, g):
        print(f"[{datetime.now()}] {g} released {self}, currently avaliable weight: {self.weight.avaliable_weight}")
        g.status = f"Stopped working out on {self}"


class Benchpress(FreeWeightEx):
    def __init__(self, eq_count, all_plates):
        super().__init__(eq_count, "Benchpress", all_plates)


class Weight:
    def __init__(self, total_weight) -> None:
        self.avaliable_weight = total_weight
        self.condition = Condition()


class Bicycle(CardioEquipement):
    def __init__(self, eq_count):
        super().__init__(eq_count, "Bicycle")


class CrunchMachine(CardioEquipement):
    def __init__(self, eq_count):
        super().__init__(eq_count, "Crunch Machine")


class Eliptical(CardioEquipement):
    def __init__(self, eq_count):
        super().__init__(eq_count, "Eliptical")


class Deadlift(FreeWeightEx):
    def __init__(self, eq_count, all_plates):
        super().__init__(eq_count, "Deadlift", all_plates)


class Smith_machine(FreeWeightEx):
    def __init__(self, eq_count, all_plates):
        super().__init__(eq_count, "Smith", all_plates)


class Fitness_room:
    def __init__(self):
        pass


class PullUpBar(CardioEquipement):
    def __init__(self, eq_count):
        super().__init__(eq_count, "Pull Up Bar")