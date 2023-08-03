DELIMITER //

DROP FUNCTION IF EXISTS team30_GetSalesAmountForSalesperson //

CREATE FUNCTION team30_GetSalesAmountForSalesperson(salesperson_name VARCHAR(100), sales_month INT, sales_year INT) 
RETURNS VARCHAR(200)
BEGIN
    DECLARE total_sales DECIMAL(10, 2);
    DECLARE message VARCHAR(200);

    SELECT SUM(total_price) INTO total_sales
    FROM team30_orders
    JOIN team30_employees ON team30_orders.worker_id = team30_employees.employee_id
    WHERE team30_employees.name = salesperson_name AND MONTH(team30_orders.order_date) = sales_month AND YEAR(team30_orders.order_date) = sales_year;

    SET message = CONCAT(salesperson_name, ' total sales amount in month ', sales_month, ' and year ', sales_year, ': $', total_sales);

    RETURN message;
END //

DELIMITER ;