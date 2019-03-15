insert into jacket_history (EID,JID, history_date,In_Out) values
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

((select eid from employee where firstname='Noah' and lastname='Crichlow'),'Sunday', '07:00','22:00'),