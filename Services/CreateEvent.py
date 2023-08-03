
from DataGateways.MySQLEventRepository import MySQLEventRepository

class CreateEvent:
    def __init__(self):
        self.event_repository = MySQLEventRepository()

    def execute(self, event_date, event_type, num_guests, waiters_assigned, chefs_assigned):
        total_price = num_guests * 50
        return self.event_repository.create_event(event_date, event_type, num_guests, total_price, waiters_assigned, chefs_assigned, 1)