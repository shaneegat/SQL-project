
from DataGateways.MySQLEventRepository import MySQLEventRepository

class CreateCustomer:
    def __init__(self):
        self.event_repository = MySQLEventRepository()

    def execute(self, name, phone, address):
        return self.event_repository.create_customer(name, phone, address)