from random import uniform
from threading import Condition
from time import sleep
from datetime import datetime


class CardioEquipement:
    def __init__(self, eq_count, name):
        self.condition = Condition()
        self.array = [True for _ in range(eq_count)]
        self.name = name
        self.taken_by = ["None" for _ in range(eq_count)]
    
    def __str__(self) -> str:
        return self.name

    def start_training(self, g):
        with self.condition:
            while not any(self.array):
                self.condition.wait()
                g.status = f"Waiting for {self}"
        
            for eq in range(len(self.array)):
                if self.array[eq]:
                    self.take_info(g)
                    #print(f"[{datetime.now()}]{g} took {self}")
                    self.array[eq] = False
                    self.taken_by[eq] = g.pid
                    g.eid = eq
                    return eq

    def stop_training(self, g):
        with self.condition:
            #print(g.pid, f" Zwolnił {self}")
            self.release_info(g)
            self.array[g.eid] = True
            self.taken_by[g.eid] = "None"
            self.condition.notify_all()

    def generate_string(self):
        string_info = "Taken by: ["
        for i in self.taken_by:
            string_info+=f"{i},"
        string_info+="]"
        return string_info

    def take_info(self, g):
        g.status = f"Works out on {self}"
        print(f"[{datetime.now()}] {g} took {self}")

    def release_info(self, g):
        g.status = f"Stopped working out on {self}"
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
        self.taken_by = ["None" for _ in range(eq_count)]
    
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
                    self.taken_by[eq] = g.pid
                    self.array[eq] = False
                    g.eid = eq
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
            self.taken_by[g.eid] = "None"
            self.condition.notify_all()
    
    def generate_string(self):
        string_info = "Taken by: ["
        for i in self.taken_by:
            string_info+=(f"{i},")
        string_info+="]"
        return string_info

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
        self.total = total_weight
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