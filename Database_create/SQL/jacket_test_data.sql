/* insert into employee (FirstName, LastName) values
  ('Damaged','Jacket'),
  ('New','Jacket'),
  ('Unassinged','Jacket'),
  ('Missing', 'Jacket')
;
*/
insert into location (location_name, location_size)
values ('Admin Office','Office'),
       ('41','Standard'),
       ('42', 'Standard'),
       ('B10', 'Big Blue');

insert into jacket_condition_template (condition)
values ('New'),
       ('Like New'),
       ('Good'),
       ('Fair'),
       ('Damaged - Repairable'),
       ('Damaged - not Repairable');

insert into jacket (jacket_type,jacket_number, modifiy_date, jacket_size, EID) values
  ('Park','1', now() , 'XS', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','2',now(), 'XS', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','3',now(), 'XS', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','4',now(), 'S', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','5',now(), 'S', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','6',now(), 'S', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','7',now(), 'S', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','8',now(), 'S', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','9',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','10',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','11',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','12',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','13',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','14',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','15',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','16',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','17',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','18',now(), 'L', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','19',now(), 'L',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','20',now(), 'L',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','21',now(), 'L',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','22',now(), 'L',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','23',now(), 'XL',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','24',now(), 'XL',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park','25',now(), 'XL',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','1',now(), 'XS', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','2',now(), 'XS',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','3',now(), 'XS',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','4',now(), 'S',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','5',now(), 'S',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','6',now(), 'S',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','7',now(), 'S',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','8',now(), 'S',  (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','9',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','10',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','11',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','12',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','13',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','14',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','15',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','16',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','17',now(), 'M', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','18',now(), 'L', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','19',now(), 'L', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','20',now(), 'L', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','21',now(), 'L', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','22',now(), 'L', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','23',now(), 'XL', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','24',now(), 'XL', (select EID from employee where FirstName like 'New' and LastName like 'Jacket')),
  ('Park Liner','25',now(), 'XL', (select EID from employee where FirstName like 'New' and LastName like 'Jacket'))
;
insert into jacket_history (EID,JID, history_date,In_Out) values
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and jacket_number = '1'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='2'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='3'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='4'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='5'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='6'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='7'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='8'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='9'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='10'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='11'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='12'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='13'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='14'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='15'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='16'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='17'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='18'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='19'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='20'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='21'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='22'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='23'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='24'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Jacket'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='25'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='1'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='2'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='3'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='4'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='5'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='6'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='7'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='8'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='9'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='10'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='11'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='12'),
  now(),
  'In'
  ),
    ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='13'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='14'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='15'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='16'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='17'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='18'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='19'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='20'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='21'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='22'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='23'),
   now(),
   'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='24'),
  now(),
  'In'
  ),
  ((select EID from employee where FirstName like 'New' and LastName like 'Park Liner'),
   (select JID from jacket where jacket_type like 'Park' and Jacket_number='25'),
   now(),
   'In'
  )
;