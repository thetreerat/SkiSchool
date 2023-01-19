copy (select e.firstname,
             e.lastname,
             t.title,
             c.cert_date,
             c.cert_current
      from certs as c
      inner join employee as e on c.eid=e.eid
      inner join cert_template as t on c.ct=t.ct
      order by e.lastname, e.firstname, t.title;) to '/Users/halc/source/SkiSchedule/Database_create/csv/last/emp_cert_list_l.csv' Delimiter ',' csv header;
