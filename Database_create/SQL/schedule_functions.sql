-- create functions

create function add_employee(p_firstname varchar(50),
                             p_lastname varchar(50)) returns varchar(50) as $$
declare
    p_eid integer;
    p_result varchar(50);
begin
    select into p_eid eid from employee where firstname=p_firstname and lastname=p_lastname;
    if p_eid is not null then
        p_result:= p_firstname||' has eid '||p_eid;
        
    else
        insert into employee (firstname, lastname) values (p_firstname,p_lastname);
        select into p_eid eid from employee where firstname=p_firstname and lastname=p_lastname;
        p_result:= 'employee added to database as eid: '||p_eid;
    end if;
    return p_result;
end; $$
language plpgsql;

create function add_employee(p_firstname varchar(50),
                             p_lastname varchar(50),
                             p_phone_cell varchar(11),
                             p_phone_cell_publish Boolean,
                             p_email varchar(50),
                             p_dob date) returns varchar(50) as $$
declare
    p_eid integer;
    p_result varchar(50);
begin
    select into p_eid eid from employee where firstname=p_firstname and lastname=p_lastname;
    if p_eid is not null then
        p_result:= p_firstname||' has eid '||p_eid;        
    else
        insert into employee (firstname,
                              lastname,
                              phone_cell,
                              phone_cell_publish,
                              email,
                              dob) values
                             (p_firstname,
                              p_lastname,
                              p_phone_cell,
                              p_phone_cell_publish,
                              p_email,
                              p_dob);
        p_result:= p_firstname||' added!';
    end if;
    return p_result;
end; $$
language plpgsql;


create function add_employee(p_firstname varchar(50),
                             p_lastname varchar(50),
                             p_phone_cell varchar(11),
                             p_phone_cell_publish Boolean,
                             p_email varchar(50),
                             p_dob date,
                             p_start_date date) returns varchar(80) as $$
declare
    p_eid integer;
    p_result varchar(80);
    p_start_result varchar(80);
begin
    select into p_eid eid from employee where firstname=p_firstname and lastname=p_lastname;
    if p_eid is not null then
        p_start_result := add_employee_start(p_eid,p_start_date);
        p_result:= p_firstname||' in database phone and email not update, start date added';        
    else
        insert into employee (firstname,
                              lastname,
                              phone_cell,
                              phone_cell_publish,
                              email,
                              dob) values
                             (p_firstname,
                              p_lastname,
                              p_phone_cell,
                              p_phone_cell_publish,
                              p_email,
                              p_dob);
        p_start_result := add_emloyee_start(p_firstname,p_lastname, p_start_date);
        p_result:= p_firstname||' added!';
    end if;
    return p_result;
end; $$
language plpgsql;

create function add_employee_aval(p_firstname varchar(50),
                                   p_lastname varchar(50),
                                   p_dow varchar(25),
                                   p_start_time time,
                                   p_end_time time) returns integer as $$
declare
    P_EID integer;
    p_eaid integer;    
begin
  select into P_EID EID from employee where firstname=p_firstname and lastname=p_lastname;
  if P_EID is not null then
    select into p_eaid eaid
    from employee_availability
    where eid=p_eid and
          start_time=p_start_time and
          end_time=p_end_time and
          dow=p_dow;
    if p_eaid is null then
        insert into employee_availability (eid,dow,start_time,end_time) values
            (P_EID,p_dow,cast(p_start_time as time),cast(p_end_time as time));
    end if;
  end if;
  return P_EID;
end; $$
LANGUAGE plpgsql;

create or replace function add_cert_min(p_title varchar(50),
                                        p_title_min_equal varchar(50)) returns varchar(25) as $$
declare
    p_ct integer;
    p_ct_min_equal integer;
begin
  select into p_ct ct from cert_template where title=p_title;
  select into p_ct_min_equal ct from cert_template where title=p_title_min_equal;
  if p_ct is not null and p_ct_min_equal is not null then
    insert into certmin (ct,ct_min_equal) values
      ((p_ct),(p_ct_min_equal));
  end if;
  return p_ct||', '||p_ct_min_equal;
end; $$
LANGUAGE plpgsql;

create or replace function add_employee_cert(p_eid integer,
                                             p_ct integer) returns varchar(150) as $$
declare
    P_Name varchar(91);
    p_title varchar(50);
    p_CID integer;
    p_result varchar(150);
begin
    select into P_Name firstname||' '||lastname from employee where eid=p_eid;
    select into p_title title from cert_template where ct=p_ct;
    select into p_CID CID from certs where eid=p_eid and ct=p_ct;
    if P_Name is not null and p_title is not null and p_CID is null then
        insert into certs (eid, ct) values (p_eid, p_ct);
        p_result := P_Name||', '||p_title;
    elsif p_CID is not null then
        p_result := 'Error: '||P_Name||' has '||p_title||' in the database alreay';
    elsif P_Name is null then
        p_result := 'Error: EID: '||p_eid||' not in the database!';
    elsif p_title is null then
        p_result := 'Error: CT:'||p_ct||' in not in the database!'
    else
        p_result := P_Name||', '||p_title;
    end if;
    return p_result;
end; $$
LANGUAGE plpgsql;

-- end of add_employee_cert(p_eid, p_ct)

create or replace function add_employee_cert(p_firstname varchar(50),
                                             p_lastname varchar(50),
                                             p_ct integer) returns varchar(30) as $$
declare
    P_EID integer;
    t_ct integer;
    p_result varchar(30);
begin
    select into P_EID EID from employee where firstname=p_firstname and lastname=p_lastname;
    if P_EID is not null then
        select into t_ct ct from certs where eid=P_EID  and ct=p_ct;
        if t_ct is null then
            insert into certs (eid,ct) values (P_EID,p_ct);
            p_result:=P_EID;
        else
            p_result:=P_EID||', '||p_ct||' All ready in!';
        end if;
    else
        p_result:=p_firstname||' '||p_lastname||' not an employee!';
    end if;
    return p_result;
end; $$
LANGUAGE plpgsql;

-- end of add_employee_cert(p_firstname, p_lastname, p_ct)

create function add_employee_dayoff(p_eid integer,
                                    p_start timestamp,
                                    p_end timestamp) returns varchar(150) as $$
declare
    p_result varchar(150);
    p_doid integer;
    p_name varchar(51);
begin
    select into p_name firstname||' '||lastname from employee where eid=p_eid;
    if p_name is not null then 
        insert into dayoff (eid,dayoffstart,dayoffend) values (p_eid,p_start,p_end);
        select into p_doid doid from dayoff where eid=p_eid and dayoffstart=p_start and dayoffend=p_end;
        p_result := 'doid: '||p_doid||' inserted for '||p_name;
    else
        p_result := 'Error: employee ID: '||p_eid||' not valid!';
    end if; 
    return p_result;
end; $$
language plpgsql;

-- end of add_employee_dateoff

create function add_employee_end(p_eid integer,
                                p_end_date date) returns varchar(80) as $$
declare
    p_SaID integer;
    p_result varchar(80);
    p_esid integer;
    d_end_date date;
begin
    select into p_SaID said from seasons where ss_date = (select max(ss_date) from seasons);
    if p_SaID is not null then
        select into p_esid esid from employee_seasons where said=p_SaID and eid=p_eid;
        select into d_end_date season_end_date from employee_seasons where esid=p_esid;
        if p_esid is not null and d_end_date is null then
            update employee_seasons set season_end_date=p_end_date where esid=p_esid;
            p_result := 'Added season end date: '||p_end_date||' for record esid='||p_esid;
        else
            if d_end_date is not null then
                p_result := 'Error: employee has end date of '||d_end_date||' already!';
            else
                p_result := 'Error: no season record for eid= '||p_eid;
            end if;
        end if;
    else
        p_result := 'Error: no seasons in database!';
    end if;
    return p_result;
end; $$
LANGUAGE plpgsql;

create function add_employee_start(p_eid integer,
                                  p_start_date date
                                  ) returns varchar(80) as $$
declare
    p_SaID integer;
    p_result varchar(80);
    p_esid integer;
begin
    select into p_SaID said from seasons where ss_date = (select max(ss_date) from seasons);
    select into p_esid esid from employee_seasons where said=p_SaID and eid=p_eid;
    if p_SaID is not null and p_esid is null then
        insert into employee_seasons (eid, SaID, season_start_date) values (p_eid,p_SaID,p_start_date);
        p_result := 'start date: '||p_start_date||' added!';
    else
        if p_esid is not null then
            p_result := 'Error: '||p_eid||' already has start date for season.';
        else
            p_result := 'Error: no seasons in database!';
        end if;
    end if;
    return p_result;
end; $$
LANGUAGE plpgsql;
create or replace function add_employee_shift(p_firstname varchar(50),
                                   p_lastname varchar(50),
                                   p_sid integer) returns integer as $$
declare
    P_EID integer;
begin
  select into P_EID EID from employee where firstname=p_firstname and lastname=p_lastname;
  update shifts set eid=P_EID where sid=p_sid;
  return P_EID;
end; $$
LANGUAGE plpgsql;

-- end of add_employee_end --

create or replace function add_employee_shift(p_eid integer,
                                              p_sid integer) returns integer as $$
begin
  update shifts set eid=p_eid where sid=p_sid;
  return P_EID;
end; $$
LANGUAGE plpgsql;

-- end of add_employee_shfit(p_eid,p_sid)

create function add_employee_start(p_firstname varchar(50),
                                  p_lastname varchar(50),
                                  p_start_date date
                                  ) returns varchar(80) as $$
declare
    p_eid integer;
    p_SaID integer;
    p_result varchar(80);
begin
    select into p_Said said from seasons where ss_date = (select max(ss_date) from seasons);
    select into p_eid eid from employee where firstname=p_firstname and lastname=p_lastname;
    if p_eid is not null then
        if p_SaID is not null then
            insert into employee_seasons (eid, SaID, season_start_date) values (p_eid,p_SaID,p_start_date);
            p_result := p_firstname||' '||p_lastname||' start date: '||p_start_date||' added!';
        else
            p_result := 'Error: no seasons in database!';
        end if;
    else
        p_result := 'Error: '||p_firstname||' '||p_lastname||' not an employee!';
    end if;

    return p_result;
end; $$
LANGUAGE plpgsql;



create function add_employee_start(p_firstname varchar(50),
                                   p_lastname varchar(50),
                                   p_season_name varchar(25),
                                   p_start_date date
                                   ) returns varchar(80) as $$
declare
    p_eid integer;
    p_SaID integer;
    p_result varchar(80) := 'hi';
begin
    select into p_eid eid select from employee where firstname=p_firstname and lastname=p_lastname;
    if p_eid is not null then
        select into p_SaID SaID from seasons where season_name=p_season_name;
        if p_SaID is not null then
            insert into employee_seasons (eid, SaID, season_start_date) values (p_eid,p_SaID,p_start_date);
            p_result := p_fristname||' '||p_lastname||' start date: '||p_start_date||' added!'
        else
            p_result := 'Error: '||p_season_name||' not in database!';
        end if;
    else
        p_result := 'Error: '||p_firstname||' '||p_lastname||' not an employee!';
    end if;
    return p_result;
end; $$
LANGUAGE plpgsql;

-- end of add_employee_start()

 create or replace function add_emp_cert_title(p_firstname varchar(50),
                                   p_lastname varchar(50),
                                   p_cert_title varchar(50)) returns varchar(25) as $$
declare
    P_EID integer;
    P_CT integer;
begin
  select into P_EID EID from employee where firstname=p_firstname and lastname=p_lastname;
  select into P_CT ct from cert_template where title=p_cert_title;
  if P_EID is not null and P_CT is not null then
    insert into certs (eid,ct) values (P_EID,(P_CT));
  end if;
  return P_EID||', '||P_CT;
end; $$
LANGUAGE plpgsql;

-- end of add_emp_cert_title(p_firstname,p_lastname,p_season_name, p_start_date)                                   

create function add_shift(p_shift_name varchar(50),
                          p_start_time time,
                          p_end_time time,
                          p_shift_date date,
                          p_ct_title varchar(50)) returns varchar(150) as $$
declare
    p_ct integer;
    p_sid integer;
begin
    select into p_ct ct
    from cert_template
    where title = p_ct_title;

    insert into shifts (shift_name,
                        start_time,
                        end_time,
                        shift_date,
                        ct)
    values (p_shift_name,
            p_start_time,
            p_end_time,
            p_shift_date,
            p_ct);

    select into p_sid max(sid)
    from shifts
    where shift_name=p_shift_name and
          start_time=p_start_time and
          end_time=p_end_time and
          shift_date=p_shift_date;
    return p_sid;
end; $$
LANGUAGE plpgsql;

-- end add_shift(p_shift_name, etc)
                                   
create function add_private(p_s_firstname varchar(25),
                            p_s_lastname varchar(25),
                            p_c_firstname varchar(25),
                            p_c_lastname varchar(25),
                            p_c_phone varchar(10),
                            p_date date,
                            p_time time,
                            p_end_time time,
                            p_lesson_length float,
                            p_lesson_type varchar(1),
                            p_s_skill_level varchar(6),
                            p_discipline varchar(4),
                            p_eid integer
                            ) returns varchar(150) as $$
declare
    p_shift_name varchar(50);
    p_ct integer;
    --p_end_time time;
    p_sid integer;
    p_result varchar(150);
begin
    p_shift_name := 'Private - '||p_s_firstname||' '||p_s_lastname||' '||p_lesson_type||' '||p_discipline;
    if p_discipline = 'Ski' then
        p_ct := 3;
    elsif p_discipline = 'SB' then
        p_ct := 2;
    else
        p_ct := 1;
    end if;
    
    --select into p_end_time (p_time + interval to_char(p_lesson_length, '9.9')||' hour');
    insert into shifts (shift_name, start_time, end_time, shift_date, eid, ct) values (p_shift_name, p_time, p_end_time,p_date, p_eid, p_ct);
    select into p_sid sid from shifts where shift_name=p_shift_name and start_time=p_time and end_time=p_end_time and shift_date=p_date;
    insert into private_lesson (sid,
                                s_firstname,
                                s_lastname,
                                s_skill_level,
                                c_firstname,
                                c_lastname,
                                c_phone,
                                lesson_type,
                                lesson_disapline,
                                assigned_eid
                                )
                        values (p_sid,
                                p_s_firstname,
                                p_s_lastname,
                                p_s_skill_level,
                                p_c_firstname,
                                p_c_lastname,
                                p_c_phone,
                                p_lesson_type,
                                p_discipline,
                                p_eid
                                );
    select into p_result pid from private_lesson where sid=p_sid;                            
    return p_result;
end; $$
LANGUAGE plpgsql;

-- end of add_private()

create function add_shift_class_size(p_sid integer,
                                     p_student_count integer,
                                     p_student_level varchar(30),
                                     p_worked_time float) returns varchar(80) as $$
declare
    p_eid integer;
    p_name varchar(50);
    p_result varchar(80);
begin
    select into p_eid eid from shifts where sid=p_sid;
    if p_eid is not null then
        select into p_name firstname||' '||lastname from employee where eid=p_eid;
        update shifts set student_level=p_student_level,student_count=p_student_count, worked_time=p_worked_time where sid=p_sid;
        p_result := p_name||' had '||p_student_count||' at level '||p_student_level||' and worked '||p_worked_time;
    else
        p_result := 'Error: Shift has no instructor assigned not updated!';
    end if;
    return p_result;
end; $$
LANGUAGE plpgsql;

create function add_shift_template(p_shift_name varchar(50),
                                   p_start_time time,
                                   p_end_time time,
                                   p_dow varchar(25),
                                   p_cert_required varchar(50),
                                   p_number_needed integer) returns integer as $$
declare
    p_ct integer;
begin
    select into p_ct ct from cert_template where title=p_cert_required;
    if p_ct is not null then
        insert into shift_templates (shift_name,start_time,end_time,dow,cert_required,number_needed) values
                                    (p_shift_name,p_start_time,p_end_time,p_dow,p_ct,p_number_needed);
    end if;
    return p_ct;
end; $$
LANGUAGE plpgsql;



create function copy_shift_template(p_stid integer,
                                    p_date date,
                                    p_nn integer) returns varchar(50) as $$
declare
    p_name varchar(50);
    p_start time;
    p_end time;
    nn_counter integer := 0;
    p_ct integer;
begin
    select into p_name TRIM(shift_name) from shift_templates where stid=p_stid;
    select into p_start start_time from shift_templates where stid=p_stid;
    select into p_end end_time from shift_templates where stid=p_stid;
    select into p_ct cert_required from shift_templates where stid=p_stid;
    while nn_counter < p_nn loop
        nn_counter := nn_counter + 1;
        insert into shifts (shift_name,start_time, end_time, shift_date,ct) values
            (p_name,p_start,p_end,p_date,p_ct);
    end loop;
    return p_name;
end; $$
LANGUAGE plpgsql;

create function copy_shift_template(p_stid integer,
                                    p_date date) returns varchar(50) as $$
declare
    p_name varchar(50);
    p_start time;
    p_end time;
    p_nn integer;
    nn_counter integer := 0;
    p_ct integer;
begin
    select into p_name TRIM(shift_name) from shift_templates where stid=p_stid;
    select into p_start start_time from shift_templates where stid=p_stid;
    select into p_end end_time from shift_templates where stid=p_stid;
    select into p_nn number_needed from shift_templates where stid=p_stid;
    select into p_ct cert_required from shift_templates where stid=p_stid;
    while nn_counter < p_nn loop
        nn_counter := nn_counter + 1;
        insert into shifts (shift_name, start_time, end_time, shift_date,ct) values
           (p_name,p_start,p_end,p_date,p_ct);
    end loop;
    return p_name;
end; $$
LANGUAGE plpgsql;


create function copy_shift_template_day(p_shift_date date) returns varchar(130)  as $$
declare
    p_dow varchar(15);
    p_count integer := 0;
    r_count integer := 0;
    myquery text;
    temprow record;
    
begin
    select into p_dow BTRIM(to_char(cast(p_shift_date as date), 'day'), ' ');
    myquery := 'select shift_name, start_time,end_time,cert_required,number_needed from shift_templates where dow=$1';
     for temprow in
            execute myquery using p_dow
        loop
            p_count:=0;
            while p_count < temprow.number_needed loop
                r_count:=r_count + 1;
                p_count:= p_count + 1;
                insert into shifts (shift_name,
                                    start_time,
                                    end_time,
                                    ct,
                                    shift_date)
                values             (temprow.shift_name,
                                    temprow.start_time,
                                    temprow.end_time,
                                    temprow.cert_required,
                                    p_shift_date);
            end loop;
        end loop;    
    return 'result: '|| p_dow||' '||r_count;
end; $$
language plpgsql;

create function copy_shift_template_next_week() returns date  as $$
declare
    p_mon date;
    p_tue date;
    p_wed date;
    p_thu date;
    p_fri date;
    p_sat date;
    p_sun date;
    temprow record;
    
begin
    select into p_mon max(cal_date) + 7  
    from calendar
    where day_of_week = 'Mon' and
          cal_date <= current_date;
    
    select into p_sun max(cal_date) + 14 
    from calendar        
    where day_of_week = 'Sun' and
          cal_date <= current_date;
    
    for temprow in
            select shift_name, start_time,end_time,cert_required from shift_templates where dow='monday'
        loop
            insert into shifts (shift_name,
                                start_time,
                                end_time,
                                ct,
                                shift_date)
            values             (temprow.shift_name,
                                temprow.start_time,
                                temprow.end_time,
                                temprow.cert_required,
                                p_mon);
        end loop;
    return p_sun;
end; $$
language plpgsql;

create function change_shift_count(p_stid integer,
                                   new_needed_count integer) returns varchar(50) as $$
declare
    p_title varchar(50);
    p_nn integer;
    myquery varchar(80):= 'update shift_templates set number_needed = $1 where stid = $2';
begin
    select into p_title shift_name from shift_templates where stid=p_stid;
    select into p_nn number_needed from shift_templates where stid=p_stid;
    execute myquery using new_needed_count,p_stid;
    return p_title||' - '||p_nn||'->'||new_needed_count;
end; $$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION insert_range_into_calendar(from_date date, to_date date)
  RETURNS void AS
$BODY$

DECLARE
    this_date date := from_date;
BEGIN

    while (this_date <= to_date) LOOP
        INSERT INTO calendar (cal_date, year_of_date, month_of_year, day_of_month, day_of_week)
        VALUES (this_date, extract(year from this_date), extract(month from this_date), extract(day from this_date),
        case when extract(dow from this_date) = 0 then 'Sun'
             when extract(dow from this_date) = 1 then 'Mon'
             when extract(dow from this_date) = 2 then 'Tue'
             when extract(dow from this_date) = 3 then 'Wed'
             when extract(dow from this_date) = 4 then 'Thu'
             when extract(dow from this_date) = 5 then 'Fri'
             when extract(dow from this_date) = 6 then 'Sat'
        end);
        this_date = this_date + interval '1 day';
    end loop;       

END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;


create or replace function list_availble(p_sid integer)
    returns table (empID integer,
                   first_name varchar(50),
                   last_name varchar(50)
                  ) as $$
declare
    p_start_time time;
    p_end_time time;
    p_shift_date date;
    p_dow varchar(15);
    
begin
 select into p_start_time start_time from shifts where sid=p_sid;
 select into p_end_time end_time from shifts where sid=p_sid;
 select into p_dow RTRIM(to_char(shift_date, 'day')) from shifts where sid=p_sid;
 select into p_shift_date shift_date from shifts where sid=p_sid;
 return query select a.eid,e.firstname,e.lastname from employee_availability as a
inner join employee as e on a.eid=e.eid
where a.start_time <= (p_start_time)
      and a.end_time >= (p_end_time)
      and a.dow = (p_dow)
      and a.eid not in (select eid from shifts
                   where start_time<=p_start_time
                   and end_time>=p_end_time
                   and eid is not null
                   and shift_date=p_shift_date)
      and a.eid in (select eid from certs
                    where ct in (select ct_min_equal
                                 from certmin
                                 where ct=(select ct
                                           from shifts
                                           where sid=p_sid)
                                )
                   )
order by e.lastname, e.firstname;
    
end; $$
LANGUAGE plpgsql;

create function list_shift(p_shift_date date)
    returns table (firstname varchar(50),
                   lastname varchar(50),
                   shift_name varchar(50),
                   start_time time,
                   end_time time,
                   html_class varchar(20)) as $$
declare
    p_result varchar(150);
begin
    return query select e.firstname,
                        e.lastname,
                        s.shift_name,
                        s.start_time,
                        s.end_time,
                        c.html_class
                        
                 from shifts as s
                 inner join employee as e on s.eid=e.eid
                 inner join cert_template as c on c.ct=s.ct
                 where s.shift_date=p_shift_date
                 order by e.lastname,e.firstname,s.start_time,s.end_time;
                
end; $$
LANGUAGE plpgsql;