SELECT e.*
FROM team30_events AS e
WHERE e.num_guests / 10 > e.waiters_assigned AND e.num_guests / 15 > e.chefs_assigned;