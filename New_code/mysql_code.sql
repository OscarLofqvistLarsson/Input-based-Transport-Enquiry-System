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

CREATE FUNCTION check_or_create_ticket(person_location VARCHAR(255), person_destination VARCHAR(255), ticket_price INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE existing_ticket_id INT;

    -- Check if a ticket with the same details already exists
    SELECT ticketID INTO existing_ticket_id
    FROM ticket
    WHERE location = person_location AND destination = person_destination AND price = ticket_price
    LIMIT 1;

    -- If such a ticket exists, return its ticketID
    IF existing_ticket_id IS NOT NULL THEN
        RETURN existing_ticket_id;
    ELSE
        -- Otherwise, create a new ticket and return its ticketID
        INSERT INTO ticket (location, destination, price, people_ticket_id)
        VALUES (person_location, person_destination, ticket_price, NULL);

        RETURN LAST_INSERT_ID();
    END IF;
END //

DELIMITER ;