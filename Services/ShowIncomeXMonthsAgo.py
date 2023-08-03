from DataGateways.MySQLEventRepository import MySQLEventRepository

class ShowIncomeXMonthsAgo:
    def __init__(self):
        self.event_repository = MySQLEventRepository()

    def execute(self, months):
        return self.event_repository.show_income_x_months_ago(months)
    
    