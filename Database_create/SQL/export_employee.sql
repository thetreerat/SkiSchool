copy (select firstname,
             lastname + ' ' + suffix as lastname,
             phone_cell, phone_cell_publish,
             email. 
             dob
    
from employee 
order by lastname, firstname) to '/Users/halc/source/SkiSchedule/Database_create/emp_a_l.csv' Delimiter ',' csv header;
