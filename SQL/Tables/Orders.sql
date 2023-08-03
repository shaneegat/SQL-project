CREATE TABLE team30_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    worker_id INT NOT NULL,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES team30_events (event_id),
    FOREIGN KEY (worker_id) REFERENCES team30_employees (employee_id),
    FOREIGN KEY (customer_id) REFERENCES team30_customers (customer_id)
);