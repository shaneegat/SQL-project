import arrow
from flask import Flask, render_template, request, redirect
from Services.AssignStaffToEvent import AssignStaffToEvent
from Services.CreateCustomer import CreateCustomer
from Services.CreateEmployee import CreateEmployee
from Services.CreateEvent import CreateEvent
from Services.GiveDiscount import GiveDiscount
from Services.SalesPersonIncome import SalesPersonIncome
from Services.ShowActiveEvents import ShowActiveEvents
from Services.ShowEventsWithoutStaff import ShowEventsWithoutStaff
from Services.ShowIncomeXMonthsAgo import ShowIncomeXMonthsAgo
from Services.ShowReturningCustomers import ShowReturningCustomers
from Services.TableByWeeks import TableByWeeks
from Utils.paginate import paginate_data

app = Flask(__name__)

table_data = None

@app.route('/')
def index():
    return render_template('Templates/index.html')

@app.route('/create_event')
def create_event_press():
    if request.method != 'GET':
        return redirect('/')

    event_date_str = request.args.get('event_date', "")
    try:
        event_date = arrow.get(event_date_str).replace(tzinfo='local')
        current_date = arrow.now().replace(tzinfo='local')

        if event_date <= current_date:
            return render_template('index.html', eventCreateError="Date should be in the future")
        
        event_type = request.args.get('event_type', "")
        num_guests = int(request.args.get('num_guests', 0))
        waiters_assigned = int(request.args.get('num_waiters', 0))
        chefs_assigned = int(request.args.get('num_chefs', 0))
        create_event = CreateEvent()
        new_event_id, new_order_id, status = create_event.execute(event_date_str, event_type, num_guests, waiters_assigned, chefs_assigned)

        if status:
            message = f"New event_id: {new_event_id} and order_id: {new_order_id}"
            return render_template('index.html', eventCreateError=message)
        
        message = f"Failed: {new_event_id}"
        return render_template('index.html', eventCreateError=message)

    except ValueError:
        return render_template('index.html')

@app.route('/create_employee')
def create_employee_press():
    if request.method != 'GET':
        return redirect('/')

    name = request.args.get('name', "")
    role = request.args.get('role', "")
    phone = request.args.get('phone', "")
    address = request.args.get('address', "")

    create_employee = CreateEmployee()
    new_employee_id, status = create_employee.execute(name, role, phone, address)
    if status:
        message = f"New employee_id: {new_employee_id}"
        return render_template('index.html', employeeCreateError=message)
        
    message = f"Failed: {new_employee_id}"
    return render_template('index.html', employeeCreateError=message)

@app.route('/create_customer')
def create_customer_press():
    if request.method != 'GET':
        return redirect('/')

    name = request.args.get('name', "")
    phone = request.args.get('phone', "")
    address = request.args.get('address', "")

    create_customer = CreateCustomer()
    new_customer_id, status = create_customer.execute(name, phone, address)
    if status:
        message = f"New customer_id: {new_customer_id}"
        return render_template('index.html', customerCreateError=message)
        
    message = f"Failed: {new_customer_id}"
    return render_template('index.html', customerCreateError=message)

@app.route('/show_events_by_weeks')
def show_events_by_weeks_press():
    global table_data
    if request.method != 'GET':
        return redirect('/')

    weeks = int(request.args.get('weeks', 1))
    page = int(request.args.get('page', 1))

    if table_data is None:
        get_table_by_weeks = TableByWeeks()
        table_data = get_table_by_weeks.execute(weeks)

    current_page_data, total_pages, page = paginate_data(page, table_data)

    return render_template('events.html', data=current_page_data, total_pages=total_pages, current_page=page)

@app.route('/show_active_events')
def show_active_events_press():
    show_active_events = ShowActiveEvents()
    table_data = show_active_events.execute()
    current_page_data, total_pages, page = paginate_data(int(request.args.get('page', 1)), table_data)

    return render_template('events_with_customer.html', data=current_page_data, total_pages=total_pages, current_page=page)

@app.route('/show_events_without_staff')
def show_events_without_staff_press():
    show_events_without_staff = ShowEventsWithoutStaff()
    table_data = show_events_without_staff.execute()
    current_page_data, total_pages, page = paginate_data(int(request.args.get('page', 1)), table_data)

    return render_template('events.html', data=current_page_data, total_pages=total_pages, current_page=page)

@app.route('/show_returning_customers')
def show_returning_customers_press():
    show_returning_customers = ShowReturningCustomers()
    table_data = show_returning_customers.execute()
    current_page_data, total_pages, page = paginate_data(int(request.args.get('page', 1)), table_data)

    return render_template('customers.html', data=current_page_data, total_pages=total_pages, current_page=page)

@app.route('/show_income_x_months_ago')
def show_income_x_months_ago_press():
    if request.method != 'GET':
        return redirect('/')

    show_income_x_months_ago = ShowIncomeXMonthsAgo()
    months = int(request.args.get('months', 1))
    income = show_income_x_months_ago.execute(months)

    return render_template('index.html', income=income)

@app.route('/assign_staff_to_event')
def assign_staff_to_event_press():
    if request.method != 'GET':
        return redirect('/')
    
    order_number = int(request.args.get('order_number', 1))
    employee_number = int(request.args.get('employee_number', 1))
    assign_staff_to_event = AssignStaffToEvent()
    message = assign_staff_to_event.execute(order_number, employee_number)

    return render_template('index.html', assignStaffToEventPress=message)

@app.route('/give_discount')
def give_discount_press():
    if request.method != 'GET':
        return redirect('/')
    
    event_id = int(request.args.get('event_id', 1))
    discount = int(request.args.get('discount', 1))
    
    give_discount = GiveDiscount()
    message = give_discount.execute(event_id, discount)

    return render_template('index.html', giveDiscount=message)

@app.route('/sales_person_income')
def sales_person_income_press():
    if request.method != 'GET':
        return redirect('/')
    
    sales_person_name = request.args.get('sales_person_name', 1)
    month = int(request.args.get('month', 1))
    year = int(request.args.get('year', 1))
    sales_person_income = SalesPersonIncome()
    message = sales_person_income.execute(sales_person_name, month, year)

    return render_template('index.html', salesPersonIncome=message)

if __name__ == '__main__':
    app.run()
