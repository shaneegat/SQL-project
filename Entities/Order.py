class Order:
    def __init__(self, customer, event, salesperson, order_date):
        self.customer = customer
        self.salesperson = salesperson
        self.event = event
        self.order_date = order_date