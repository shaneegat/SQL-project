USE dbCourseSt23;
DROP PROCEDURE IF EXISTS team30_ScheduleTeamForEvent;

DELIMITER //

CREATE PROCEDURE team30_ScheduleTeamForEvent(
    IN event_id_param INT,
    IN employ_id_param INT
)
BEGIN
    DECLARE event_date_val DATE;
    DECLARE num_guests_val INT;
    DECLARE num_chefs_val INT;
    DECLARE num_waiters_val INT;
    DECLARE employ_role_val VARCHAR(100);
    DECLARE employ_name_val VARCHAR(100);
    DECLARE employ_needed_chefs INT;
    DECLARE employ_needed_waiters INT;
    DECLARE result_message VARCHAR(200);
    
    SELECT event_date, num_guests, chefs_assigned, waiters_assigned
    INTO event_date_val, num_guests_val, num_chefs_val, num_waiters_val
    FROM team30_events
    WHERE event_id = event_id_param;
    
    SELECT role, name
    INTO employ_role_val, employ_name_val
    FROM team30_employees
    WHERE employee_id = employ_id_param;
    
    IF event_date_val <= CURDATE() THEN
        SET result_message = 'The event is not in the future.';
    ELSE
        IF employ_role_val = 'chef' THEN
            SET employ_needed_chefs = CEIL(num_guests_val / 10) - num_chefs_val;
            SET result_message = CONCAT(employ_name_val, ' has been added as a chef');
            IF employ_needed_chefs > 0 THEN
                SET result_message = CONCAT(result_message, ' and ', employ_needed_chefs - 1, ' more chef(s) needed.');
                UPDATE team30_events SET chefs_assigned = chefs_assigned + 1 WHERE event_id = event_id_param;
            ELSE
                SET result_message = CONCAT('No chef is needed.');
            END IF;
        ELSEIF employ_role_val = 'waiter' THEN
            SET employ_needed_waiters = CEIL(num_guests_val / 10) - num_waiters_val;
            SET result_message = CONCAT(employ_name_val, ' has been added as a waiter');
            IF employ_needed_waiters > 0 THEN
                SET result_message = CONCAT(result_message, ' and ', employ_needed_waiters - 1, ' more waiter(s) needed.');
                UPDATE team30_events SET waiters_assigned = waiters_assigned + 1 WHERE event_id = event_id_param;
            ELSE
                SET result_message = CONCAT('No waiter is needed.');
            END IF;
        ELSE
            SET result_message = CONCAT(employ_name_val, ' is not allowed to participate in events as a salesperson.');
        END IF;
    END IF;
    
    SELECT result_message AS message;
END;
//

DELIMITER ;