SELECT e.*, c.name AS customer_name, c.phone AS customer_phone, c.address AS customer_address
FROM team30_events AS e
JOIN team30_orders AS o ON e.event_id = o.event_id
JOIN team30_customers AS c ON o.customer_id = c.customer_id
WHERE e.event_date > NOW();