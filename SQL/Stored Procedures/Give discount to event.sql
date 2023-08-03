USE dbCourseSt23;
DROP PROCEDURE IF EXISTS team30_update_event_discount;

DELIMITER //

CREATE PROCEDURE team30_update_event_discount(
    IN event_id_param INT,
    IN discount_percentage_param DECIMAL(5, 2)
)
BEGIN
    DECLARE event_price DECIMAL(10, 2);
    DECLARE discount_amount DECIMAL(10, 2);
    DECLARE original_price DECIMAL(10, 2);
    DECLARE new_price DECIMAL(10, 2);
    DECLARE message VARCHAR(200);

    SELECT price INTO event_price
    FROM team30_events
    WHERE event_id = event_id_param;

    SET discount_amount = event_price * (discount_percentage_param / 100);
    SET original_price = event_price;
    SET new_price = event_price - discount_amount;

    UPDATE team30_events
    SET price = new_price
    WHERE event_id = event_id_param;

    SET message = CONCAT('Original Price: $', original_price, ', New Price: $', new_price);

    SELECT message;
END //

DELIMITER ;
