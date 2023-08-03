from DataGateways.MySQLEventRepository import MySQLEventRepository

class GiveDiscount:
    def __init__(self):
        self.event_repository = MySQLEventRepository()

    def execute(self, event_id, percentages):
        return self.event_repository.give_discount(event_id, percentages)