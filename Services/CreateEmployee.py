
from DataGateways.MySQLEventRepository import MySQLEventRepository

class CreateEmployee:
    def __init__(self):
        self.event_repository = MySQLEventRepository()

    def execute(self, name, role, phone, address):
        return self.event_repository.create_employee(name, role, phone, address)