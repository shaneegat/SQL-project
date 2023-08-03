CREATE TABLE team30_events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_date DATE NOT NULL UNIQUE,
    event_type VARCHAR(100) NOT NULL,
    num_guests INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    waiters_assigned INT NOT NULL,
    chefs_assigned INT NOT NULL
);