SELECT YEAR(order_date) AS year, MONTH(order_date) AS month, SUM(total_price) AS income, COUNT(order_id) AS total_orders
FROM team30_orders
WHERE order_date >= DATE_SUB(NOW(), INTERVAL X MONTH)
GROUP BY year, month;