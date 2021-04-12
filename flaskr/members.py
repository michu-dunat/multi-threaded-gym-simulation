from threading import Thread, Condition
from app import locker_lock
class GenericMember(Thread):
    def __init__(self, reception):
        super().__init__(target=self.execute_training_plan)
        self.condition = Condition()        
        self.receptionist = reception
        self.locker = None
        pass

    def execute_training_plan(self):
        pass

    def exit_gym():
        pass


    def enter_gym():
        free_locker = self.receptionist.ask()
        attempt = 0
        if(free_locker):
            self.locker = free_locker
            locker_lock.release()
        
        else:
            self.exit_gym()
        pass
