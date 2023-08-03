SELECT c.customer_id, c.name, c.phone, c.address
FROM team30_customers AS c
JOIN team30_orders AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.phone, c.address
HAVING COUNT(o.order_id) > 1;