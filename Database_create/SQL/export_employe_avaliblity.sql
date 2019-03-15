copy (select ea.eid,
    e.lastname,
    e.firstname,
    ea.dow,
    ea.start_time,
    ea.end_time,
    ea.said
from employee_availability as ea
inner join employee as e on ea.eid=e.eid
order by e.lastname, e.firstname) to '/Users/halc/source/SkiSchedule/Database_create/emp_a.csv' Delimiter ',' csv header;