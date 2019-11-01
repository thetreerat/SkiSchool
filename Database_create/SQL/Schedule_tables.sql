create database skischool;

\c skischool

-- create tables 
CREATE TABLE calendar
(
  cal_date date NOT NULL,
  year_of_date integer NOT NULL,
  month_of_year integer NOT NULL,
  day_of_month integer NOT NULL,
  day_of_week character(3) NOT NULL,
  CONSTRAINT calendar_pkey PRIMARY KEY (cal_date),
  CONSTRAINT calendar_check CHECK (year_of_date::double precision = date_part('year'::text, cal_date)),
  CONSTRAINT calendar_check1 CHECK (month_of_year::double precision = date_part('month'::text, cal_date)),
  CONSTRAINT calendar_check2 CHECK (day_of_month::double precision = date_part('day'::text, cal_date)),
  CONSTRAINT calendar_check3 CHECK (day_of_week::text = 
CASE
    WHEN date_part('dow'::text, cal_date) = 0::double precision THEN 'Sun'::text
    WHEN date_part('dow'::text, cal_date) = 1::double precision THEN 'Mon'::text
    WHEN date_part('dow'::text, cal_date) = 2::double precision THEN 'Tue'::text
    WHEN date_part('dow'::text, cal_date) = 3::double precision THEN 'Wed'::text
    WHEN date_part('dow'::text, cal_date) = 4::double precision THEN 'Thu'::text
    WHEN date_part('dow'::text, cal_date) = 5::double precision THEN 'Fri'::text
    WHEN date_part('dow'::text, cal_date) = 6::double precision THEN 'Sat'::text
    ELSE NULL::text
END)
)
WITH (
  OIDS=FALSE
);

create table certmin
    ( CMID serial primary key,
      CT integer not null,
      CT_Min_Equal integer not null
    )
;

Create table certs
    ( CID serial primary key,
      EID integer not null,
      CT integer not null,
      cert_date date,
      cert_current integer default 1
    )
;

Create table Cert_Template
    (  CT serial primary key,
       Title character varying(50),
       Org character varying(30)
       
    )
;

create table DayOff
    ( DOID serial primary key,
      EID integer not null,
      DayOffStart timestamp,
      DayoffEnd timestamp,
      approved integer default 0,
      SaID integer default 1
    )
;    

create table employee
     (  EID serial primary key,
        LastName character varying(30),
        FirstName character varying(30),
        suffix varchar(5),
        NickName character varying(30),
        DOB date,
        Phone_cell character varying(11),
        Phone_cell_publish Boolean,
        Phone_2_text character varying(20),
        Phone_2 character varying(11),
        Phone_3_text character varying(20),
        Phone_3 character varying(11),
        Email character varying(50),
        Email_SMS character varying(50),
        payroll_id character varying(15) unique,
        PSIA_ID character varying(15),
        AASI_ID character varying(15)
    )
;

create table employee_availability 
    (   EAID serial primary key,
        EID integer,
        DOW character varying(10),
        Start_Time time,
        End_Time time,
        SaID integer default 1,
        foreign key (eid) references employee (EID) on delete restrict,
        foreign key (said) references seasons (said) on delete restrict
    )
;

create table employee_returning_templates
    (  rt serial primary key,
       return_title varchar(20)
    );
    
create table employee_seasons
    ( ESID serial primary key,
      SaID integer,
      eid integer,
      season_start_date date,
      season_end_date date,
      employee_returning integer,
      foreign key (SaID) references seasons (SaID) on delete restrict,
      foreign key (eid) references employee (EID) on delete restrict,
      foreign key (returning) references employee_returning_templates (rt) on delete restrict
    );
    
create table menu_roles
    (MRID serial primary Key,
     Role varchar(30)
    );

create table menu_items
    (MIID serial primary key,
     MRID integer,
     display_text varchar(20),
     help_text varchar(150),
     menu_command varchar(150),
     foreign key (MRID) REFERENCES menu_roles (MRID) on delete restrict
    );
     
create table private_lesson
    (PID serial primary key,
     sid integer,
     s_firstname varchar(30),
     s_lastname varchar(30),
     s_skill_level varchar(6),
     s_age integer,
     lesson_length float,
     c_firstname varchar(30),
     c_lastname varchar(30),
     c_phone varchar(10),
     lesson_type varchar(1),
     lesson_disapline varchar(4),
     s2_firstname varchar(30),
     s2_lastname varchar(30),
     checked_in boolean,
     payed boolean,
     Notes text,
     foreign key (sid) REFERENCES shifts (sid) on delete restrict,
     foreign key (assigned_eid) references employee (eid) on delete restrict
    );

create table publish
    (PuID serial primary key,
     page_name varchar(50),
     publish_date date,
     publish_rev integer default 0,
     update_date date,
     page_gen_date date,
    );
    
create table seasons
    ( SaID serial primary key,
      ss_date date,
      se_date date,
      season_name character varying(25)
    );
    
create table shifts 
	( SID serial primary key,
	  shift_name varchar(50),
      start_time time,
      end_time time,
      Shift_Date date,
      EID integer,
      no_show boolean default False,
      student_level varchar(25),
      student_count integer,
      worked_time NUMERIC(6, 2),
      ct integer default 1,
      cancelled boolean default False,
      publish integer default 0,
      SaID integer default 1,
      html_class varchar(20) defalut 'standard'
    )
;
        
create table shift_templates
	( StID serial primary key,
      Shift_Name character varying(45),
      start_time time, 
      End_Time time,
      DOW character varying(25),
      cert_required integer default 1,
      SaID integer default 1,
      number_needed integer
    )
;

-- create views            
create view employee_cert_list as
    select e.lastname,
           e.firstname,
           c.ct,
           ct.title
    from employee as e
    inner join certs as c on e.EID=c.eid
    inner join cert_template as ct on c.ct=ct.ct
;

create view dayoff_requests as
    select dt.doid,
           e.firstname,
           e.lastname,
           dt.dayoffstart,
           dt.dayoffend,
           dt.approved
    from dayoff as dt
    inner join employee as e on e.EID=dt.eid
;

create view dayoff_requests_approved as
    select dt.doid,
           e.firstname,
           e.lastname,
           dt.dayoffstart,
           dt.dayoffend,
           dt.approved,
           e2.firstname||' '||e2.lastname as approver
    from dayoff as dt
    inner join employee as e on e.EID=dt.eid
    inner join employee as e2 on dt.approved=e2.eid;

create view employee_certs as
    select c.eid,e.firstname||' '||e.lastname as Name, c.ct, ct.title from certs as c
        inner join employee as e on c.eid=e.eid
        inner join cert_template as ct on c.ct=ct.ct
    order by e.lastname,e.firstname,ct.title;

create view employee_missing_certs as
    select eid,firstname,lastname
    from employee
    where eid not in (select eid from certs) and
          eid not in (select eid from employee where lastname='Jacket')
    order by lastname,firstname;

create view employee_avail as
   select  e.eid,
           e.firstname,
           e.lastname,
           ea.dow,
           ea.Start_Time,
           ea.End_Time
   from employee as e
   inner join employee_availability as ea on e.eid=ea.eid
   order by e.lastname, e.firstname, ea.dow, ea.start_time, ea.end_time;

create view open_shfits as
     select s.sid,
       s.shift_name,
       s.start_time,
       s.end_time,
       to_char(s.shift_date, 'day') as DOW,
       s.shift_date,
       s.eid,
       c.title as "Min Cert"
    from shifts as s
    inner join cert_template as c on c.ct=s.ct
    where s.eid is null
    order by DOW, s.shift_name;

create view assigned_shifts as
    select s.sid,
       s.shift_name,
       to_char(s.shift_date, 'day') as DOW,
       s.start_time,
       s.end_time,
       s.shift_date,
       e.firstname,
       e.lastname
    from shifts as s
    inner join employee as e on s.eid=e.eid
    where s.eid is not null
    order by s.shift_date, e.lastname, e.firstname, s.start_time, s.end_time;

create view cert_min as
    select t.title as title,
           cm.title as min_equal_title,
           m.ct,
           m.ct_min_equal
    from certmin as m
    inner join cert_template as t on m.ct=t.ct
    inner join cert_template as cm on m.ct_min_equal=cm.ct
    order by t.title,cm.title;


create view export_emp_aval as
    select e.firstname,
           e.lastname,
           a.dow,
           a.start_time,
           a.end_time
    from employee_availability as a
    inner join employee as e on e.eid=a.eid
    order by e.lastname,
             e.firstname,
             a.dow,
             a.start_time,
             a.end_time;
    
create view shift_count as
    select e.lastname ||', '||e.firstname as name,
           count(s.eid) as shift_count,
           sum(extract(epoch from (s.end_time-s.start_time)) / 3600) as scheduled_hours,
           sum(s.worked_time) as worked_hours
    from shifts as s
    inner join employee as e on s.eid=e.eid
    where s.shift_date between '03/11/19' and '03/18/19'
    group by name
    order by name;
    
create view list_shift_templates as
    select t.stid,
           t.shift_name,
           t.start_time,
           t.end_time,
           t.dow,
           ct.title,
           t.number_needed
    from shift_templates as t
    inner join cert_template as ct on t.cert_required=ct.ct
    order by dow,shift_name,start_time,end_time;

-- create index

CREATE INDEX calendar_day_of_month
  ON calendar
  USING btree
  (day_of_month);
  
CREATE INDEX calendar_day_of_week
  ON calendar
  USING btree
  (day_of_week);

CREATE INDEX calendar_month_of_year
  ON calendar
  USING btree
  (month_of_year);
  
CREATE INDEX calendar_year_of_date
  ON calendar
  USING btree
  (year_of_date);