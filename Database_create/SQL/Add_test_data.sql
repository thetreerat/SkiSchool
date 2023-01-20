insert into employee_seasons (said,eid,season_start_date, season_end_date) values
    ((select said from seasons where season_name='2018-2019 Season'),
     (select EID from employee where firstname='Harold' and lastname='Clark'),
     '11/1/2018',
     '03/31/2019'
    );

insert into employee_seasons (said,eid,season_start_date, season_end_date) values
    ((select said from seasons where season_name='2019-2020 Season'),
     (select EID from employee where firstname='Harold' and lastname='Clark'),
     '11/1/2019',
     '03/31/2020'
    );    

insert into employee_seasons (said,eid,season_start_date, season_end_date) values
    ((select said from seasons where season_name='2020-2021 Season'),
     (select EID from employee where firstname='Harold' and lastname='Clark'),
     '11/1/2020',
     '03/31/2021'
    );    

insert into employee_seasons (said,eid,season_start_date, season_end_date) values
    ((select said from seasons where season_name='2021-2022 Season'),
     (select EID from employee where firstname='Harold' and lastname='Clark'),
     '11/1/2021',
     '03/31/2022'
    );    
    



              
--insert into DayOff (EID, DayOffStart,DayoffEnd, approved, approving_user, approved_date) values
 
--    ((select eid from employee where firstname='Noah' and lastname='Crichlow'),
--      '02/8/17 06:30',
--      '02/17/17 18:00',
--      True,
--      (select eid from employee where firstname='Harold' and lastname='Clark'),
--      '01/10/17 15:21'
--    );

--update shifts set ct=(select ct from cert_template where title = 'SB Lineup Sup')
--where shift_name='SB Lineup Sup';

--update shifts set ct=(select ct from cert_template where title = 'Park 1')
--where shift_name='Park Night' or
--      shift_name='Park Night/lineup' or
--      shift_name='Park Open';
      
--update shifts set ct=(select ct from cert_template where title = 'SB Instructor')
--where shift_name like '%Snowboard';

--update shifts set ct=(select ct from cert_template where title = 'Park Lead')
--where shift_name like 'Park Night Lead';
