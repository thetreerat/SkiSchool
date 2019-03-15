insert into seasons (ss_date, se_date, season_name) values
  ('10/1/18', '5/1/19', '2018-2019 Season');
  
insert into employee_hired_season (said,eid,es_date,ee_date) values
    ((select said from seasons where season_name='2018-2019 Season'),
     (select EID from employee where firstname='Harold' and lastname='Clark'),
     '11/1/2018',
     NULL
    );
    
insert into DayOff (EID, DayOffStart,DayoffEnd, approved) values
 
    ((select eid from employee where firstname='Noah' and lastname='Crichlow'),
      '02/8/17 06:30',
      '02/17/17 18:00',
      (select eid from employee where firstname='Harold' and lastname='Clark')
    );

update shifts set ct=(select ct from cert_template where title = 'SB Lineup Sup')
where shift_name='SB Lineup Sup';

update shifts set ct=(select ct from cert_template where title = 'Park 1')
where shift_name='Park Night' or
      shift_name='Park Night/lineup' or
      shift_name='Park Open';
      
update shifts set ct=(select ct from cert_template where title = 'SB Instructor')
where shift_name like '%Snowboard';

update shifts set ct=(select ct from cert_template where title = 'Park Lead')
where shift_name like 'Park Night Lead';
