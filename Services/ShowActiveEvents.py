from DataGateways.MySQLEventRepository import MySQLEventRepository

class ShowActiveEvents:
    def __init__(self):
        self.event_repository = MySQLEventRepository()

    def execute(self):
        return self.event_repository.show_active_events()