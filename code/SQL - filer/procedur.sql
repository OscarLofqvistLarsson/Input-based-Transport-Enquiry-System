DELIMITER //

CREATE PROCEDURE check_name(IN person_name VARCHAR(255), OUT person_threshold VARCHAR(255), OUT person_funds INT)
BEGIN
    SELECT threshold, funds
    INTO person_threshold, person_funds
    FROM people
    WHERE fname = person_name
    LIMIT 1;  -- Ensure only one row is returned
END //

DELIMITER ;
