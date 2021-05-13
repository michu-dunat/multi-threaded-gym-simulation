from threading import Thread, Condition
from time import sleep

class GenericMember(Thread):
    def __init__(self, pid, reception):
        super().__init__(target=self.execute_training_plan)
        self.pid = pid
        self.condition = Condition()
        self.receptionist = reception
        self.locker = None
        pass

    def execute_training_plan(self):
        self.enter_gym()
        pass


    def exit_gym(self):
        print(f"Wychodzę {self.pid}")


    def enter_gym(self):
        print(f"Wchodzę, {self.pid}")
        self.locker = self.receptionist.ask_to_enter()
        attempt = 0
        if(self.locker):
            print(f"Wziąłem szafkę {self.pid}")

            self.locker.take()
            sleep(5)
            self.locker.release()
            self.exit_gym()
        else:
            self.exit_gym()
        pass
