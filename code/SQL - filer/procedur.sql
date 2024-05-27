DELIMITER //
CREATE PROCEDURE CheckPersonName(IN person_name VARCHAR(255))
BEGIN
    SELECT threshold, funds FROM people WHERE fname = person_name;
END //
DELIMITER ;