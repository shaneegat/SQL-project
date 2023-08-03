from DataGateways.MySQLEventRepository import MySQLEventRepository

class SalesPersonIncome:
    def __init__(self):
        self.event_repository = MySQLEventRepository()

    def execute(self, worker_name, month, year):
        return self.event_repository.sales_person_income(worker_name, month, year)