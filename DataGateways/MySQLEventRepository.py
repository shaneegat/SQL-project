import datetime

import arrow
from Utils.config import DB_CONFIG
import mysql.connector

class MySQLEventRepository:
    def __init__(self):
        self.connection = None
        self.connect()

    def __del__(self):
        self.close()

    def connect(self):
        if self.connection is None or not self.connection.is_connected():
            self.connection = mysql.connector.connect(
                host=DB_CONFIG['HOST'],
                user=DB_CONFIG['USER'],
                password=DB_CONFIG['PASSWORD'],
                database=DB_CONFIG['DATABASE']
            )

    def close(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()

    def create_order(self, event_id, saleperson_id, customer_id, order_date, total_price):
        try:
            self.connect()
            cursor = self.connection.cursor()

            query = "INSERT INTO team30_orders (event_id, worker_id, customer_id, order_date, total_price) VALUES (%s, %s, %s, %s, %s);"
            values = (event_id, saleperson_id, customer_id, order_date, total_price)
            cursor.execute(query, values)

            self.connection.commit()

            return cursor.lastrowid

        except mysql.connector.Error as error:
            print("Error creating order:", error)
            return None
        
    def create_event(self, event_date, event_type, num_guests, total_price, waiters_assigned, chefs_assigned, customer_id):
        try:
            cursor = self.connection.cursor()
            check_event_query = "SELECT event_id FROM team30_events WHERE event_date = %s"
            cursor.execute(check_event_query, (event_date,))
            existing_event = cursor.fetchone()

            if existing_event:
                message = "event already exsist in this date"
                status = False
                return message, None , status
            insert_event_query = "INSERT INTO team30_events (event_date, event_type, num_guests, price, waiters_assigned, chefs_assigned) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_event_query, (event_date, event_type, num_guests, total_price, waiters_assigned, chefs_assigned))
            self.connection.commit()

            new_event_id = cursor.lastrowid
            current_date = arrow.now().replace(tzinfo='local')
            current_date_str = current_date.format('YYYY-MM-DD')

            new_order_id = self.create_order(new_event_id, 3, customer_id, current_date_str, total_price)

            return new_event_id, new_order_id, True
        except mysql.connector.Error as err:
            print("Error inserting event into the database:", err)

    def create_employee(self, name, role, phone, address):
        try:
            cursor = self.connection.cursor()

            check_employee_query = "SELECT employee_id FROM team30_employees WHERE name = %s"
            cursor.execute(check_employee_query, (name,))
            existing_employee = cursor.fetchone()

            if existing_employee:
                return "Employee with the same name already exists.", False

            insert_employee_query = "INSERT INTO team30_employees (name, role, phone, address) VALUES (%s, %s, %s, %s)"
            values = (name, role, phone, address)
            cursor.execute(insert_employee_query, values)

            self.connection.commit()

            new_employee_id = cursor.lastrowid
            return new_employee_id, True

        except mysql.connector.Error as err:
            return "Error inserting employee into the database:", False

    def create_customer(self, name, phone, address):
        try:
            cursor = self.connection.cursor()

            check_customer_query = "SELECT customer_id FROM team30_customers WHERE name = %s"
            cursor.execute(check_customer_query, (name,))
            existing_customer = cursor.fetchone()

            if existing_customer:
                return "Customer with the same name already exists.", False

            query = "INSERT INTO team30_customers (name, phone, address) VALUES (%s, %s, %s);"
            values = (name, phone, address)
            cursor.execute(query, values)

            self.connection.commit()

            return cursor.lastrowid, True

        except mysql.connector.Error as error:
            return "Error inserting customer into the database:", False

    def show_income_x_months_ago(self, months):
        try:
            self.connect()
            cursor = self.connection.cursor()

            query = f"SELECT SUM(total_price) AS income FROM team30_orders WHERE order_date >= DATE_SUB(NOW(), INTERVAL {months} MONTH);"
            cursor.execute(query)

            total_income = cursor.fetchone()[0]

            return total_income

        except mysql.connector.Error as error:
            print("Error fetching event table from the database:", error)
            return 0

    def get_table_by_weeks(self, weeks):
        try:
            self.connect()
            cursor = self.connection.cursor()

            query = f"SELECT * FROM team30_events WHERE event_date <= DATE(NOW()) AND event_date > DATE_SUB(NOW(), INTERVAL {weeks} WEEK);"
            cursor.execute(query)
            table_data = cursor.fetchall()

            return table_data

        except mysql.connector.Error as error:
            print("Error fetching event table from the database:", error)
            return []

    def show_active_events(self):
        try:
            self.connect()
            cursor = self.connection.cursor()

            query = f"SELECT e.*, c.name AS customer_name, c.phone AS customer_phone, c.address AS customer_address FROM team30_events AS e JOIN team30_orders AS o ON e.event_id = o.event_id JOIN team30_customers AS c ON o.customer_id = c.customer_id WHERE e.event_date > CURDATE();"
            cursor.execute(query)

            table_data = cursor.fetchall()

            return table_data

        except mysql.connector.Error as error:
            print("Error fetching event table from the database:", error)
            return []

    def show_events_without_staff(self):
        try:
            self.connect()
            cursor = self.connection.cursor()

            query = f"SELECT e.* FROM team30_events AS e WHERE e.num_guests / 10 > e.waiters_assigned AND e.num_guests / 15 > e.chefs_assigned;"
            cursor.execute(query)

            table_data = cursor.fetchall()

            return table_data

        except mysql.connector.Error as error:
            print("Error fetching event table from the database:", error)
            return []

    def show_returning_customers(self):
        try:
            self.connect()
            cursor = self.connection.cursor()

            query = f"SELECT c.customer_id, c.name, c.phone, c.address FROM team30_customers AS c JOIN team30_orders AS o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.name, c.phone, c.address HAVING COUNT(o.order_id) > 1;"
            cursor.execute(query)

            table_data = cursor.fetchall()

            return table_data

        except mysql.connector.Error as error:
            print("Error fetching event table from the database:", error)
            return []
        
    def give_discount(self, event_id, discount_percentage):
        try:
            self.connect()
            cursor = self.connection.cursor()

            cursor.callproc("team30_update_event_discount", (event_id, discount_percentage))

            result = next(cursor.stored_results())
            return result.fetchone()[0]

        except mysql.connector.Error as error:
            print("Error giving discount to event:", error)
            return "An error occurred while applying the discount."

    def assign_staff_to_event(self, event_id_param, employ_id_param):
        try:
            self.connect()
            cursor = self.connection.cursor()

            cursor.callproc('team30_ScheduleTeamForEvent', (event_id_param, employ_id_param))

            result = next(cursor.stored_results())
            message =  result.fetchone()[0]

            self.connection.commit()
            return message
        except mysql.connector.Error as error:
            print("Error calling team30_ScheduleTeamForEvent:", error)
            return "An error occurred while calling the stored procedure."

    def sales_person_income(self, salesperson_name, sales_month, sales_year):
        try:
            self.connect()
            cursor = self.connection.cursor()

            query = f"SELECT team30_GetSalesAmountForSalesperson('{salesperson_name}', {sales_month}, {sales_year});"

            cursor.execute(query)
            result = cursor.fetchone()[0]

            return result

        except mysql.connector.Error as error:
            print("Error fetching sales amount for salesperson:", error)
            return 0