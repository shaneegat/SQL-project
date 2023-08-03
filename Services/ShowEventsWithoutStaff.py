from DataGateways.MySQLEventRepository import MySQLEventRepository

class ShowEventsWithoutStaff:
    def __init__(self):
        self.event_repository = MySQLEventRepository()

    def execute(self):
        return self.event_repository.show_events_without_staff()