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
CREATE FUNCTION CheckPreference(fname VARCHAR(20))
RETURNS BOOLEAN
BEGIN
    DECLARE pref_exists BOOLEAN;
    SELECT CASE WHEN COUNT(*) > 0 THEN TRUE ELSE FALSE END INTO pref_exists
    FROM preference
    WHERE fname = p_fname;
    RETURN pref_exists;
END //
DELIMITER ;

