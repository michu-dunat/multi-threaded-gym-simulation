from threading import Lock, Condition


class Locker:
    def __init__(self):
        self.status = "free"
        self.condition = Condition()
        self.lock = Lock()            

    def take(self):
        with self.lock:
            self.status="taken"

    def release(self):
        with self.lock:
            self.status="free"

class Threadmill:
    def __init__(self):
        pass


class Ergometer:
    def __init__(self):
        pass


class Benchpress:
    def __init__(self):
        pass


class Bicycle:
    def __init__():
        pass


class Bar_position:
    def __init__(self):
        pass


class Excercise_position:
    def __init__(self):
        pass


class Equipement:
    def __init__(self):
        pass


class Fitness_room:
    def __init__(self):
        pass