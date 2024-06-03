DELIMITER //
CREATE PROCEDURE GetPreferences(IN person_fname VARCHAR(20))
BEGIN
    SELECT p.fname, pr.train, pr.bus
    FROM people p
    JOIN preference pr ON p.fname = pr.fname
    WHERE p.fname = person_fname;
END //
DELIMITER ;



DELIMITER //

CREATE PROCEDURE check_name(IN person_name VARCHAR(255), OUT person_funds INT)
BEGIN
    SELECT funds
    INTO person_funds
    FROM people
    WHERE fname = person_name
    LIMIT 1;  -- Ensure only one row is returned
END //

DELIMITER ;
