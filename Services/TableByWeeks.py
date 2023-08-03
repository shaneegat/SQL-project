from DataGateways.MySQLEventRepository import MySQLEventRepository

class TableByWeeks:
    def __init__(self):
        self.event_repository = MySQLEventRepository()

    def execute(self, weeks):
        return self.event_repository.get_table_by_weeks(weeks)