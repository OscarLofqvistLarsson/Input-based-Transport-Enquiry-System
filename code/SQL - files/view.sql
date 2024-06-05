CREATE VIEW person_ticket_info AS
SELECT 
    p1.fname AS person_name,
    p1.funds AS remaining_funds,
    t.location AS ticket_start,
    t.destination AS ticket_destination,
    t.price AS ticket_price
FROM 
    people p1
JOIN 
    ticket t ON p1.people_ticket_id = t.ticketID
JOIN 
    (SELECT fname, min(funds) AS latest_funds FROM people GROUP BY fname) p2 ON p1.fname = p2.fname;
