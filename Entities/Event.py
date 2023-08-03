class Event:
    def __init__(self, event_date, event_type, num_guests):
        self.event_date = event_date
        self.event_type = event_type
        self.num_guests = num_guests
        self.price = 0
        self.price_per_guest = 0
        self.waiters_assigned = 0
        self.chefs_assigned = 0