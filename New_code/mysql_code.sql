DELIMITER //
CREATE PROCEDURE GetPreferences(IN person_fname VARCHAR(20))
BEGIN
    SELECT p.fname, pr.train, pr.bus
    FROM people p
    JOIN preference pr ON p.fname = pr.fname
    WHERE p.fname = person_fname;
END //
DELIMITER ;
