from DataGateways.MySQLEventRepository import MySQLEventRepository

class AssignStaffToEvent:
    def __init__(self):
        self.event_repository = MySQLEventRepository()

    def execute(self, order, worker):
        return self.event_repository.assign_staff_to_event(order, worker)