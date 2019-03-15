insert into employee_availability (EID,DOW,Start_Time,End_Time) values
    ((select eid from employee where firstname='James' and lastname='Vennette'),
      'Friday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='James' and lastname='Vennette'),
      'Saturday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='James' and lastname='Vennette'),
      'Monday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='James' and lastname='Vennette'),
      'Tuesday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='James' and lastname='Vennette'),
      'Thursday',
      '07:00',
      '22:00'
    ),    
    ((select eid from employee where firstname='Harold' and lastname='Clark'),
      'Monday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Harold' and lastname='Clark'),
      'Tuesday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Harold' and lastname='Clark'),
      'Wednesday',
      '07:00',
      '22:00'),
    ((select eid from employee where firstname='Harold' and lastname='Clark'),
      'Thursday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Harold' and lastname='Clark'),
      'Friday',
      '05:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Harold' and lastname='Clark'),
      'Saturday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Harold' and lastname='Clark'),
      'Sunday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Chris' and lastname='Bills'),
      'Monday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Chris' and lastname='Bills'),
      'Wednesday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Chris' and lastname='Bills'),
      'Thursday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Chris' and lastname='Bills'),
      'Friday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Chris' and lastname='Bills'),
      'Saturday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Chris' and lastname='Bills'),
      'Sunday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Tyler' and lastname='Austin'),
      'Saturday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Tyler' and lastname='Austin'),
      'Sunday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Zach' and lastname='Shultz'),
      'Saturday',
      '07:00',
      '22:00'
    ),
    ((select eid from employee where firstname='Zach' and lastname='Shultz'),
      'Sunday',
      '07:00',
      '10:00'
    ),
    ((select eid from employee where firstname='Guy' and lastname='Boor'),
      'Saturday',
      '07:00',
      '22:00'),
    ((select eid from employee where firstname='Guy' and lastname='Boor'),
      'Sunday',
      '07:00',
      '22:00'),
    ((select eid from employee where firstname='Guy' and lastname='Boor'),
      'Friday',
      '05:00',
      '22:00'
    );
    
    
insert into certmin (CT,CT_Min_Equal) values
    ((select ct from cert_template where title='SB Instructor'),(select ct from cert_template where title='AASI Level 1')),
    ((select ct from cert_template where title='SB Instructor'),(select ct from cert_template where title='AASI Level 2')),
    ((select ct from cert_template where title='SB Instructor'),(select ct from cert_template where title='AASI Level 3')),
    ((select ct from cert_template where title='SB Instructor'),(select ct from cert_template where title='Level 1 SB')),
    ((select ct from cert_template where title='SB Instructor'),(select ct from cert_template where title='Level 2 SB')),
    ((select ct from cert_template where title='SB Instructor'),(select ct from cert_template where title='Level 3 SB')),
    ((select ct from cert_template where title='SB Instructor'),(select ct from cert_template where title='SB Lineup Sup')),
    ((select ct from cert_template where title='Level 1 SB'),(select ct from cert_template where title='AASI Level 1')),
    ((select ct from cert_template where title='Level 1 SB'),(select ct from cert_template where title='AASI Level 2')),
    ((select ct from cert_template where title='Level 1 SB'),(select ct from cert_template where title='AASI Level 3')),
    ((select ct from cert_template where title='Level 1 SB'),(select ct from cert_template where title='Level 2 SB')),
    ((select ct from cert_template where title='Level 1 SB'),(select ct from cert_template where title='Level 2 SB')),
    ((select ct from cert_template where title='Level 1 SB'),(select ct from cert_template where title='SB Lineup Sup')),
    ((select ct from cert_template where title='Level 2 SB'),(select ct from cert_template where title='AASI Level 2')),
    ((select ct from cert_template where title='Level 2 SB'),(select ct from cert_template where title='AASI Level 3')),
    ((select ct from cert_template where title='Level 2 SB'),(select ct from cert_template where title='Level 3 SB')),
    ((select ct from cert_template where title='Level 3 SB'),(select ct from cert_template where title='AASI Level 3')),
    ((select ct from cert_template where title='AASI Level 1'),(select ct from cert_template where title='AASI Level 2')),
    ((select ct from cert_template where title='AASI Level 1'),(select ct from cert_template where title='AASI Level 3')),
    ((select ct from cert_template where title='AASI Level 2'),(select ct from cert_template where title='AASI Level 3')),
    ((select ct from cert_template where title='Park 1'),(select ct from cert_template where title='Park Lead')),
    ((select ct from cert_template where title='Park 1'),(select ct from cert_template where title='Park Sup')),
    ((select ct from cert_template where title='Park 1'),(select ct from cert_template where title='Park Manager')),
    ((select ct from cert_template where title='Frestyle Level 1'),(select ct from cert_template where title='Frestyle Level 2')),
    ((select ct from cert_template where title='Level 1 Park SB'),(select ct from cert_template where title='Frestyle Level 1')),
    ((select ct from cert_template where title='Level 1 Park SB'),(select ct from cert_template where title='Frestyle Level 2')),
    ((select ct from cert_template where title='Level 1 Park SB'),(select ct from cert_template where title='Level 2 Park SB')),
    ((select ct from cert_template where title='Level 2 Park SB'),(select ct from cert_template where title='Frestyle Level 2')),
    ((select ct from cert_template where title='SB Instructor'),(select ct from cert_template where title='SB Instructor')),
    ((select ct from cert_template where title='SB Lineup Sup'),(select ct from cert_template where title='SB Lineup Sup'))
    ;

insert into certs (EID, CT) values
    ((select eid from employee where firstname='Tommy' and lastname='Morsch'),
     (select ct from cert_template where title='AASI Level 3')
    ),
    ((select eid from employee where firstname='Harold' and lastname='Clark'),
     (select ct from cert_template where title='AASI Level 1')
    ),
    ((select eid from employee where firstname='Harold' and lastname='Clark'),
     (select ct from cert_template where title='SB Lineup Sup')
    ),
    ((select eid from employee where firstname='Harold' and lastname='Clark'),
     (select ct from cert_template where title='Park Manager')
    ),
    ((select eid from employee where firstname='Guy' and lastname='Boor'),
     (select ct from cert_template where title='AASI Level 3')
    ),
    ((select eid from employee where firstname='Lee' and lastname='Dame'),
     (select ct from cert_template where title='AASI Level 2')
    ),
    ((select eid from employee where firstname='Tommy' and lastname='Morsch'),
     (select ct from cert_template where title='Frestyle Level 2')
    ),
    ((select eid from employee where firstname='Tommy' and lastname='Morsch'),
     (select ct from cert_template where title='Frestyle Level 2')
    ),
    ((select eid from employee where firstname='Matt' and lastname='Hall'),
     (select ct from cert_template where title='Frestyle Level 1')
    ),
    ((select eid from employee where firstname='Matt' and lastname='Hall'),
     (select ct from cert_template where title='AASI Level 1')
    ),
    ((select eid from employee where firstname='Joshua' and lastname='Pike'),
     (select ct from cert_template where title='SB Instructor')
    ),
    ((select eid from employee where firstname='Joshua' and lastname='Pike'),
     (select ct from cert_template where title='Park Lead')
    ),
    ((select eid from employee where firstname='Luke' and lastname='Sheets'),
     (select ct from cert_template where title='Park 1')
    ),
    ((select eid from employee where firstname='Jesse' and lastname='Sheets'),
     (select ct from cert_template where title='Park 1')
    ),
    ((select eid from employee where firstname='Chris' and lastname='Bills'),
     (select ct from cert_template where title='Park 1')
    ),
    ((select eid from employee where firstname='Chris' and lastname='Bills'),
     (select ct from cert_template where title='Ski Instructor')
    ),
    ((select eid from employee where firstname='Luke' and lastname='Sheets'),
     (select ct from cert_template where title='SB Instructor')
    ),
    ((select eid from employee where firstname='Jesse' and lastname='Sheets'),
     (select ct from cert_template where title='SB Instructor')
    ),
    ((select eid from employee where firstname='Cody' and lastname='Wolschlegal'),
     (select ct from cert_template where title='SB Instructor')
    ),
    ((select eid from employee where firstname='Andrew' and lastname='Walsh'),
     (select ct from cert_template where title='SB Instructor')
    ),
    ((select eid from employee where firstname='James' and lastname='Vennette'),
     (select ct from cert_template where title='AASI Level 1')
    ),
    ((select eid from employee where firstname='Devon' and lastname='Spychalski'),
     (select ct from cert_template where title='SB Instructor')
    ),
    ((select eid from employee where firstname='Jacob' and lastname='Slocuk'),
     (select ct from cert_template where title='SB Instructor')
    ),
    ((select eid from employee where firstname='Zach' and lastname='Shultz'),
     (select ct from cert_template where title='AASI Level 1')
    ),
    ((select eid from employee where firstname='Joseph' and lastname='Scardilla'),
     (select ct from cert_template where title='SB Instructor')
    ),
    ((select eid from employee where firstname='Noah' and lastname='Crichlow'),
     (select ct from cert_template where title='SB Instructor')
    )
    ;