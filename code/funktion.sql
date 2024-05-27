DELIMITER //

CREATE FUNCTION check_or_create_ticket(person_location VARCHAR(255), person_destination VARCHAR(255), ticket_price INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE existing_ticket_id INT;

    -- Kontrollera om en biljett med samma detaljer redan finns
    SELECT ticketID INTO existing_ticket_id
    FROM ticket
    WHERE location = person_location AND destination = person_destination AND price = ticket_price
    LIMIT 1;

    -- Om en sådan biljett finns, returnera dess ticketID
    IF existing_ticket_id IS NOT NULL THEN
        RETURN existing_ticket_id;
    ELSE
        -- Annars, skapa en ny biljett och returnera dess ticketID
        INSERT INTO ticket (location, destination, price)
        VALUES (person_location, person_destination, ticket_price);

        RETURN LAST_INSERT_ID();
    END IF;
END //

DELIMITER ;
