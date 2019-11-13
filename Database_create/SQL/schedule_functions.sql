-- create functions
create or replace function add_candidate(p_eid integer,
                                         discipline_title varchar) returns integer as $$
declare
    p_caid integer;
    p_ct integer;
begin
    select into p_ct ct from cert_template where title=discipline_title;
    insert into candidate(eid, discipline) values (p_eid, p_ct);
    select into p_caid max(caid) from candidate where eid=p_eid;
    return p_caid;
end; $$

language plpgsql;
-- end add_candidate

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
        p_start_result := self._eeid()(p_eid,p_start_date);
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
-- end of add_employee()

-- need to make a add_employee_aval with eid, dow, start_teim, end_time
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
        insert into employee_availability (eid,dow,start_time,end_time,dow_sort) values
            (P_EID,p_dow,cast(p_start_time as time),cast(p_end_time as time),(select get_DOW_sort(p_dow)));
    end if;
  end if;
  return P_EID;
end; $$
LANGUAGE plpgsql;
-- end of add_emplye_aval

create function add_employee_availabilty(p_eid integer,
                                         p_dow varchar(25),
                                         p_start_time time,
                                         p_end_time time) returns integer as $$
declare
    p_eaid integer;    
begin
    select into p_eaid eaid
    from employee_availability
    where eid=p_eid and
          start_time=p_start_time and
          end_time=p_end_time and
          dow=p_dow;
    if p_eaid is null then
        insert into employee_availability (eid,dow,start_time,end_time, dow_sort) values
            (P_EID,p_dow,cast(p_start_time as time),cast(p_end_time as time), (select get_DOW_sort(p_dow)));
        select into p_eaid eaid
        from employee_availability
        where eid=p_eid and
            start_time=p_start_time and
            end_time=p_end_time and
            dow=p_dow;

    end if;  
    return P_EAID;
end; $$
LANGUAGE plpgsql;
-- end of add_employee_availability()

create function get_DOW_sort(dow varchar(15))
    returns integer as $$
declare
    p_sort integer;
begin
    if dow='monday' then
        p_sort := 1;
    elsif dow = 'tuesday' then
        p_sort := 2;
    elsif dow = 'wednesday' then
        p_sort := 3;
    elsif dow = 'thursday' then
        p_sort := 4;
    elsif dow = 'friday' then
        p_sort := 5;
    elsif dow = 'saturday' then
        p_sort := 6; 
    elsif dow = 'sunday' then
        p_sort :=7;
    end if;
    return p_sort;
end; $$
LANGUAGE plpgsql;
--end of get_dow_sort()


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
create or replace function add_employee_cert(p_eid integer,
                                             p_ct integer,
                                             p_cert_current integer,
                                             p_cert_date date) returns varchar(150) as $$
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
        insert into certs (eid, ct, cert_current, cert_date) values (p_eid, p_ct, p_cert_current, p_cert_date);
        p_result := P_Name||', '||p_title;
    elsif p_CID is not null then
        p_result := 'Error: '||P_Name||' has '||p_title||' in the database alreay';
    elsif P_Name is null then
        p_result := 'Error: EID: '||p_eid||' not in the database!';
    elsif p_title is null then
        p_result := 'Error: CT:'||p_ct||' in not in the database!';
    else
        p_result := P_Name||', '||p_title;
    end if;
    return p_result;
end; $$
LANGUAGE plpgsql;

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
        if p_esid is not null then
            update employee_seasons set season_end_date=p_end_date where esid=p_esid;
            p_result := 'Added season end date: '||p_end_date||' for record esid='||p_esid;
        else
            p_result := 'Error: no season record for eid= '||p_eid;
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

-- end add_employee_start(p_eid, p_start_date)


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
create or replace function add_employee_start(p_eid integer,
                                              p_start_date date) returns integer as $$
declare
    p_said integer;
begin
    select into p_said said from get_current_season();
    if p_said is not null then
        insert into employee_seasons (eid, SaID, season_start_date)
                    values (p_eid,p_SaID,p_start_date);
    end if;
    return p_said
end; $$
LANGUAGE plpgsql;
-- end add_employee_start(eid)

create or replace function get_employee_default_start()
                  returns date as $$
declare
    best_date date;
    cdate date;
begin
    select into best_date ss_date_default from seasons where said=(select * from get_current_season());
    select into cdate current_date;
    if best_date < cdate then
        best_date = cdate;
    end if;
    return best_date;
end; $$
LANGUAGE plpgsql;


create function add_employee_start(p_firstname varchar(50),
                                  p_lastname varchar(50),
                                  p_start_date date
                                  ) returns varchar(80) as $$
declare
    p_eid integer;
    p_SaID integer;
    p_result varchar(80);
begin
    select into p_Said said from get_current_seasons();
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

-- end add_employee_start(fname, lname, start)

create function add_employee_start(p_firstname varchar(50),
                                   p_lastname varchar(50),
                                   p_season_name varchar(25),
                                   p_start_date date
                                   ) returns varchar(80) as $$
declare
    p_eid integer;
    p_SaID integer;
    p_esid integer;
    p_result varchar(80) := 'hi';
begin
    select into p_eid eid from employee where firstname=p_firstname and lastname=p_lastname;
    if p_eid is not null then
        select into p_SaID SaID from seasons where season_name=p_season_name;
        select into p_esid esid from employee_seasons where eid=p_eid and said=p_said;
        if p_SaID is not null then 
            if p_esid is null then
                insert into employee_seasons (eid, SaID, season_start_date) values (p_eid,p_SaID,p_start_date);
                p_result := p_fristname||' '||p_lastname||' start date: '||p_start_date||' added!';
            else
                p_result := 'Error: Employee already has start date.';
            end if;
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

create or replace function add_employee_extra_day(p_eid integer,
                                                  p_et integer,
                                                  p_priority integer)
    returns integer as $$
declare
    r_eeid integer;
begin
    insert into employee_extra_days (eid, et, priority)
        values (p_eid, p_et, p_priority);
    select into r_eeid eeid
        from employee-extra_days
        where eid=p_eid and
              et=p_et and
              priority=p_priority;
    return r_eeid;
end; $$
LANGUAGE plpgsql;
-- end add_employee_extra_day()

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

create or replace function add_emp_cert_title(p_firstname varchar(50),
                                   p_lastname varchar(50),
                                   p_cert_title varchar(50),
                                   p_cert_date date) returns varchar(25) as $$
declare
    P_EID integer;
    P_CT integer;
begin
  select into P_EID EID from employee where firstname=p_firstname and lastname=p_lastname;
  select into P_CT ct from cert_template where title=p_cert_title;
  if P_EID is not null and P_CT is not null then
    insert into certs (eid,ct,cert_date) values (P_EID,P_CT, p_cert_date);
  end if;
  return P_EID||', '||P_CT;
end; $$
LANGUAGE plpgsql;

-- end of add_emp_cert_title(p_firstname,p_lastname,p_season_name, p_start_date)
create or replace function add_extra_days(p_title varchar(40),
                                          p_extra_date date,
                                          p_points integer,
                                          p_ideal_max integer
                                          ) returns integer as $$
declare
    r_et integer;
begin 
    insert into extra_days_templates (title, extra_date, points, ideal_max)
           values (p_title, p_extra_date, p_points, p_ideal_max);
    select into r_et max(et)
           from extra_days_templates
           where title=p_title and
                 said=(select * from get_current_season());
    return r_et;
end; $$
LANGUAGE plpgsql;
-- end of add_extra_days()

create or replace function add_season(p_season_name varchar(50),
                                      p_ss_date date,
                                      p_se_date date) returns integer as $$
    declare
        p_said integer;        
    begin
        insert into seasons (season_name,
                             se_date,
                             ss_date)
        values (p_season_name,
                p_se_date,
                p_ss_date);
        
        select into p_said max(said) from seasons;
        return p_said;
end; $$
LANGUAGE plpgsql;    

-- end of add_season()
create or replace function add_shift(p_shift_name varchar(50),
                          p_start_time time,
                          p_end_time time,
                          p_shift_date date,
                          p_ct_title varchar(50),
                          p_html_class varchar) returns integer as $$
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
                            ct,
                            html_class)
        values (p_shift_name,
                p_start_time,
                p_end_time,
                p_shift_date,
                p_ct,
                p_html_class);

        select into p_sid max(sid)
        from shifts
        where shift_name=p_shift_name and
              start_time=p_start_time and
              end_time=p_end_time and
              shift_date=p_shift_date;
        return p_sid;
    
end; $$
LANGUAGE plpgsql;

-- end add_shift(p_shift_name, p_start_time, p_end_time, p_shift_date,p_ct_title, p_html_class)

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
create or replace function  add_shift_template(p_Shift_Name varchar(45),
                                   p_start_time time, 
                                   p_End_Time time,
                                   p_DOW varchar(25),
                                   p_cert_required integer ,
                                   p_SaID integer,
                                   p_number_needed integer
                                  ) returns integer as $$
declare
    p_stid integer;
begin
    insert into shift_templates (shift_name,
                                 start_time,
                                 end_time,
                                 dow,
                                 cert_required,
                                 said,
                                 number_needed)
        values (p_shift_name,
                p_start_time,
                p_end_time,
                p_dow,
                p_cert_required,
                p_said,
                p_number_needed);
    select into p_stid max(stid) from shift_templates where shift_name=p_shift_name;
    return p_stid;
end $$
LANGUAGE plpgsql;
-- end add_shift_template()

create function add_private(p_sid integer,
                            p_s_firstname varchar(30),
                            p_s_lastname varchar(30),
                            p_s_skill_level varchar(6),
                            p_lesson_length float,
                            p_c_firstname varchar(30),
                            p_c_lastname varchar(30),
                            p_c_phone varchar(10),
                            p_lesson_type varchar(1),
                            p_lesson_disapline varchar(4),
                            p_s2_firstname varchar(30),
                            p_s2_lastname varchar(30)) returns integer as $$
declare
    p_pid integer;
begin
    insert into private_lesson (sid,s_firstname,s_lastname,s_skill_level,
                                c_firstname, c_lastname, c_phone,
                                lesson_type, lesson_disapline, s2_firstname,
                                s2_lastname)
    values (p_sid,p_s_firstname,p_s_lastname,p_s_skill_level,
            p_c_firstname, p_c_lastname, p_c_phone,
            p_lesson_type, p_lesson_disapline, p_s2_firstname,
            p_s2_lastname);
    select into p_pid max(pid) from private_lesson where sid=p_sid;
    return p_pid;
end; $$
LANGUAGE plpgsql;

-- end add_private(p_pid,p_sid,p_s_firstname,p_s_lastname,p_s_skill_level,
--                 p_lesson_length, p_c_firstname,p_c_lastname,p_c_phone,
--                   p_lesson_type,p_lesson_disapline,p_s2_firstname, p_s2_lastname)
create or replace function add_private(p_s_firstname varchar(25),
                            p_s_lastname varchar(25),
                            p_s_age integer, 
                            p_c_firstname varchar(25),
                            p_c_lastname varchar(25),
                            p_c_phone varchar(10),
                            p_lesson_type varchar(1),
                            p_s_skill_level varchar(6),
                            p_discipline varchar(4),
                            p_sid integer) returns integer as $$
declare
    p_pid integer;
begin
    insert into private_lesson (sid,
                                s_firstname,
                                s_lastname,
                                s_age,
                                s_skill_level,
                                c_firstname,
                                c_lastname,
                                c_phone,
                                lesson_type,
                                lesson_disapline
                                )
                        values (p_sid,
                                p_s_firstname,
                                p_s_lastname,
                                p_s_age,
                                p_s_skill_level,
                                p_c_firstname,
                                p_c_lastname,
                                p_c_phone,
                                p_lesson_type,
                                p_discipline
                                );
    select into p_pid pid from private_lesson where sid=p_sid;                            
    return p_pid;
end; $$
LANGUAGE plpgsql;

-- end of add_private()    
                        
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
-- end of add_shift_template()


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


create or replace function copy_shift_template_day(p_shift_date date) returns varchar(130)  as $$
declare
    p_dow varchar(15);
    p_count integer := 0;
    r_count integer := 0;
    myquery text;
    temprow record;
    
begin
    select into p_dow BTRIM(to_char(cast(p_shift_date as date), 'day'), ' ');
    myquery := 'select shift_name,
                       start_time,
                       end_time,
                       cert_required,
                       number_needed
                from shift_templates
                where dow=$1 and
                      said=(select * from get_current_season())';
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

create function sorts(p_org varchar(30),
                           p_title varchar(50))
    returns table (r_ct integer,
                   r_title varchar(50),
                   r_org varchar(30)
                   ) as $$
begin
    if p_org = '' or p_org is Null then
        p_org := '%';
    end if;
    if p_title = ''or p_title is Null then
        p_title := '%';
    end if;
    return query select ct,
                        title,
                        org
    from cert_template 
    where title ilike p_title and
          org ilike p_org
    order by title, org;
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
-- end insert_into_calendar

create or replace function delete_shift_template(p_stid integer)
    returns integer as $$
begin
    update shift_templates set deleted = TRUE where stid=p_stid;
    return 1;
end; $$
LANGUAGE plpgsql;
-- end delete_shift_template(p_stid integer)

create or replace function get_cert(p_ct integer)
    returns table (ct integer,
                   title varchar(50),
                   org varchar(30),
                   html_class varchar(10)
                  ) as $$
begin
    return query select t.ct,
                        t.title,
                        t.org,
                        t.html_class
                 from cert_template as t
                 where t.ct=p_ct;
end; $$
LANGUAGE plpgsql;

-- end get_cert(p_ct integer)
create or replace function get_current_extra_days()
    returns table (et integer,
                   title varchar(40),
                   extra_date date,
                   points integer,
                   ideal_max integer,
                   booked bigint) as $$
begin
    return query select t.et, t.title, t.extra_date, t.points, t.ideal_max, count(e.et)
    from extra_days_templates as t
    left outer join employee_extra_days as e on e.et=t.et
    where t.said=(select * from get_current_season())
    group by t.et, t.title, t.extra_date, t.points, t.ideal_max
    order by t.extra_date;
    
end; $$
LANGUAGE plpgsql;

-- end get_current_extra_days()                   
create function get_current_season()
    returns integer as $$
declare
    p_said integer;
begin
    select into p_said said from seasons where ss_date = (select max(ss_date) from seasons);
    return p_said;
end;  $$
LANGUAGE plpgsql;

-- end of get_current_season()
create or replace function get_dow_avalibility(p_dow varchar(25))
    returns table (eaid integer,
                  eid integer,
                  dow varchar(25),
                  start_time time,
                  end_tiem time,
                  said integer,
                  dow_sort integer) as $$
begin
    return query select a.eaid,
                  a.eid,
                  a.dow,
                  a.start_time,
                  a.end_time,
                  a.said,
                  a.dow_sort
    from employee_availability as a
    where a.dow=p_dow and
          a.said=(select * from get_current_season());
end;  $$
LANGUAGE plpgsql;

-- end of get_dow_avalibility()

create function get_eid(p_firstname varchar(30),
                        p_lastname varchar(30)
                        )
    returns integer as $$
declare
    p_eid integer;
begin
    select into p_eid eid from employee where firstname=p_firstname and lastname=p_lastname;
    return p_eid;
end; $$
LANGUAGE plpgsql;

-- end of get_eid()

create function get_employee(p_eid integer)
    returns table (eid integer,
                   firstname varchar(30),
                   lastname varchar(30),
                   suffix varchar(5),
                   Nickname varchar(30),
                   DOB date,
                   phone_cell varchar(11),
                   Phone_cell_publish Boolean,
                   Phone_2_text character varying(20),
                   Phone_2 character varying(11),
                   Phone_3_text character varying(20),
                   Phone_3 character varying(11),
                   Email character varying(50),
                   Email_SMS character varying(50),
                   payroll_id character varying(15),
                   PSIA_ID character varying(15),
                   AASI_ID character varying(15),
                   sex varchar(6)
                   ) as $$
begin
    return query select e.eid,
                        e.firstname,
                        e.lastname,
                        e.suffix, 
                        e.nickname,
                        e.dob,
                        e.phone_cell,
                        e.phone_cell_publish,
                        e.phone_2_text,
                        e.phone_2,
                        e.phone_3_text,
                        e.phone_3,
                        e.email,
                        e.email_sms,
                        e.payroll_id,
                        e.psia_id,
                        e.aasi_id,
                        e.sex
                 from employee as e
                 where p_eid=e.eid;
end; $$
LANGUAGE plpgsql;
-- end onf get_employee()

create function get_employee(p_firstname varchar(30),
                             p_lastname varchar(30))
    returns table (eid integer,
                   firstname varchar(30),
                   lastname varchar(30),
                   suffix varchar(5),
                   Nickname varchar(30),
                   DOB date,
                   phone_cell varchar(11),
                   Phone_cell_publish Boolean,
                   Phone_2_text character varying(20),
                   Phone_2 character varying(11),
                   Phone_3_text character varying(20),
                   Phone_3 character varying(11),
                   Email character varying(50),
                   Email_SMS character varying(50),
                   payroll_id character varying(15),
                   PSIA_ID character varying(15),
                   AASI_ID character varying(15),
                   sex varchar(6)
                   ) as $$
begin
    if p_firstname is null  or p_firstname='' then
        p_firstname := '%';
    end if;
    if p_lastname is null or p_lastname='' then
        p_lastname  := '%';
    end if;
    return query select e.eid,
                        e.firstname,
                        e.lastname,
                        e.suffix, 
                        e.nickname,
                        e.dob,
                        e.phone_cell,
                        e.phone_cell_publish,
                        e.phone_2_text,
                        e.phone_2,
                        e.phone_3_text,
                        e.phone_3,
                        e.email,
                        e.email_sms,
                        e.payroll_id,
                        e.psia_id,
                        e.aasi_id,
                        e.sex
                 from employee as e
                 where e.lastname ilike p_lastname and 
                       e.firstname ilike p_firstname
                order by e.lastname, e.firstname;
end; $$
LANGUAGE plpgsql;
-- end onf get_employee()

create or replace function get_employee_availability(p_eid integer)
    returns table (r_eaid integer,
                   r_eid integer,
                   r_dow varchar(10),
                   r_start_time time,
                   r_end_time time,
                   r_said integer) as $$
begin
    return query select eaid,eid, dow, start_time, end_time, said
                 from employee_availability
                 where said = (select get_current_season()) and
                       eid = p_eid
                 order by dow_sort;
end; $$
LANGUAGE plpgsql;
-- end of get_employee_availability()

create function get_employee_cell(p_eid integer)
    returns varchar(11) as $$
declare
    p_cell varchar(11);
begin
    select into p_cell phone_cell from employee where eid=p_eid;
    return p_cell;
end; $$
LANGUAGE plpgsql;

-- end of get_employee_cell()

create function get_employee_certs(p_eid integer)
    returns table (cid integer,
                   ct integer,
                   title varchar(50),
                   org varchar(30),
                   cert_date date,
                   cert_current integer) as $$
begin
    return query select c.cid,
    c.ct,
    t.title,
    t.org,
    c.cert_date,
    c.cert_current
    from certs as c
    inner join cert_template as t on c.ct=t.ct
    where c.eid=p_eid
    order by c.cert_date;
end; $$
LANGUAGE plpgsql;

-- end of get_employee_certs()

create or replace function get_employee_extra_points(p_eid integer)
    returns bigint as $$
declare
    r_total bigint;
begin
    select into r_total sum(t.points) as total_points
        from employee_extra_days as e
        inner join extra_days_templates as t on t.et=e.et
        where eid=p_eid;
    return r_total;
end; $$
LANGUAGE plpgsql;
-- end get_employee_extra_points()

create function get_employee_season_dates(p_eid integer)
    returns table (eid integer,
                   start_date date,
                   end_date date,
                   employee_returning integer,
                   return_title VARCHAR(20)) as $$    
begin
    return query select s.eid,
                        s.season_start_date,
                        s.season_end_date,
                        s.employee_returning,
                        e.return_title
                 from employee_seasons as s
                 full join employee_returning_templates as e on s.employee_returning=e.rt
                 where s.eid=p_eid and s.said=get_current_season();
end; $$
LANGUAGE plpgsql;

-- end of get_employee_season_dates

create or replace function get_extra_day_booked(p_et integer)
    returns bigint as $$
declare
    r_total bigint;
begin
    select into r_total count(et) from employee_extra_days where et=p_et;
    return r_total;
end; $$
LANGUAGE plpgsql;
-- end of get_extra_day_booked(p_et)

create or replace function get_extra_days_template(p_et integer)
    returns table (et integer,
                   title varchar(40),
                   extra_date date,
                   points integer,
                   ideal_max integer,
                   booked bigint) as $$
begin
    return query select t.et, t.title, t.extra_date, t.points, t.ideal_max, get_extra_day_booked(p_et)
    from extra_days_templates as t
    where t.et=p_et;
    
end; $$
LANGUAGE plpgsql;
-- end get_extra_days_template(et integer)

create or replace function get_private (p_student_firstname varchar(45),
                             p_student_lastname varchar(45),
                             p_student_skill varchar(6),
                             p_contact_firstname varchar(45),
                             p_contact_lastname varchar(45),
                             p_contact_phone varchar(10),
                             p_instructor_firstname varchar(45),
                             p_instructor_lastname varchar(45),
                             p_start_date date,
                             p_end_date date,
                             p_disapline varchar(4),
                             p_type varchar(1),
                             p_age integer)
    returns table (pid integer,
                   sid integer,
                   s_firstname varchar(45),
                   s_lastname varchar(45),
                   s_skill_level varchar(6),
                   c_firstname varchar(45),
                   c_lastname varchar(45),
                   c_phone varchar(30),
                   lesson_type varchar(1),
                   lesson_disapline varchar(4),
                   assigned_eid integer,
                   s_age integer,
                   e_firstname varchar(45),
                   e_lastname varchar(45)) as $$
declare
    find_query text;
    where_clause text;
begin
    if p_instructor_firstname='' and p_instructor_lastname!='' then
        where_clause := 'p.assigned_eid in (select eid
                                            from employee
                                            where firstname=''%'' and
                                                  lastname= '''||p_instructor_lastname||''') ';
    elsif p_instructor_firstname!='' and p_instructor_lastname='' then
        where_clause := 'p.assigned_eid in (select eid
                                            from employee
                                            where firstname='''||p_instructor_firstname||''' and
                                                  lastname= ''%'') ';
    else 
        where_clause := 'p.assigned_eid in (select eid
                                             from employee
                                             where firstname=''%'' and
                                             lastname=''%'') ';
    end if;

    if p_student_firstname!='' then
        where_clause := where_clause||' p.s_firstname ilike '||p_student_firstname||' and';
    else:
        where_clasue := where_clause||' p.s_firstname ilike ''%'' and';
    end if;
    
    if p_student_lastname!='' then
        where_clause := where_clause||' p.s_lastname ilike '||p_student_lastname||' and';
    else:
        where_clause := where_clause||' p.s_lastname ilike ''%'' and';
    end if;
    
    if p_contact_lastname!='' then
        where_clause := where_clause||' p.c_lastname ilike '||p_contact_lastname||' and';
    else:
        where_clause := where_clause||' p.c_lastname ilike ''%'' and';
    end if;

    if p_contact_firstname!='' then
        where_clause := where_clause||' p.c_firstname ilike '||p_contact_firstname||' and';
    else:
        where_clause := where_clause||' p.c_firstname ilike ''%'' and';
    end if;
    
    if p_contact_phone!='' then
        where_clause := where_clause||' p.c_phone ilike '||p_contact_phone||' and';
    else:
        where_clause := where_clause||' p.c_phone ilike ''%'' and';
    end if;
    
    if p_student_skill!='' then
        where_clause := where_clause||' p.s_skill_level ilike'||p_student_skill||' and';
    else:
        where_clause := where_clause||' p.s_skill_level ilike''%'' and';
    end if;
    
    if p_start_date is not null and p_end_date is null then
        where_clause := where_clause|| 'date'
        
    find_query := 'select p.pid,
                    p.sid,
                    p.s_firstname,
                    p.s_lastname,
                    p.s_skill_level,
                    p.c_firstname,
                    p.c_lastname,
                    p.c_phone,
                    p.lesson_type,
                    p.lesson_disapline,
                    p.assigned_eid,
                    p.s_age,
                    e.firstname,
                    e.lastname
             from private_lesson as p
             join employee as e on e.eid=p.assigned_eid
             where '||where_clause||' order by p.pid';
    return query execute find_query ;            
end; $$
LANGUAGE plpgsql;
                             
-- end of get_private

create or replace function get_seasons()
    returns table (said integer,
                  ss_date date,
                  se_date date,
                  season_name character varying(25)
                 ) as $$
begin
    return query select s.said,
                        s.ss_date,
                        s.se_date,
                        s.season_name
                 from seasons as s
                 order by s.ss_date;
end; $$
LANGUAGE plpgsql;  
  
-- end of get_seasons

create or replace function get_seasons(p_said integer)
    returns table (said integer,
                  ss_date date,
                  se_date date,
                  season_name character varying(25)
                 ) as $$
begin
    return query select s.said,
                        s.ss_date,
                        s.se_date,
                        s.season_name
                 from seasons as s
                 where s.said=p_said
                 order by s.ss_date;
end; $$
LANGUAGE plpgsql;  
  
-- end of get_seasons (p_said)

create or replace function get_shift_template(p_stid integer)
    returns table (StID integer,
                   shift_name character varying(45),
                   start_time time, 
                   end_time time,
                   DOW character varying(25),
                   cert_required integer,
                   SaID integer,
                   number_needed integer) as $$
begin
    return query select s.stid,
                        s.shift_name,
                        s.start_time,
                        s.end_time,
                        s.dow,
                        s.cert_required,
                        s.said,
                        s.number_needed
                 from shift_templates as s
                 where s.stid=p_stid and
                       s.deleted = FALSE
                 order by s.dow, s.shift_name;
end $$
LANGUAGE plpgsql;
                   
-- end get_shift_template ()

create or replace function get_shift_templates(p_said integer, p_dow varchar(25))
    returns table (StID integer,
                   shift_name character varying(45),
                   start_time time, 
                   end_time time,
                   DOW character varying(25),
                   cert_required integer,
                   SaID integer,
                   number_needed integer) as $$
begin
    return query select s.stid,
                        s.shift_name,
                        s.start_time,
                        s.end_time,
                        s.dow,
                        s.cert_required,
                        s.said,
                        s.number_needed
                 from shift_templates as s
                 where s.said=p_said and
                       s.dow=p_dow and
                       s.deleted = FALSE
                 order by s.dow, s.shift_name;
end $$
LANGUAGE plpgsql;
-- end get_shift_templates (said, dow)

create or replace function get_current_shift_templates()
    returns table (StID integer,
                   shift_name character varying(45),
                   start_time time, 
                   end_time time,
                   DOW character varying(25),
                   cert_required integer,
                   SaID integer,
                   number_needed integer) as $$
begin

    return query select s.stid,
                        s.shift_name,
                        s.start_time,
                        s.end_time,
                        s.dow,
                        s.cert_required,
                        s.said,
                        s.number_needed
                 from shift_templates as s
                 where s.said=(select * from get_current_season()) and
                       s.deleted = FALSE
                 order by s.dow, s.shift_name;
end $$
LANGUAGE plpgsql;
                   
-- end get_current_shift_templates ()

create or replace function get_current_shift_templates(p_dow varchar(25))
    returns table (StID integer,
                   shift_name character varying(45),
                   start_time time, 
                   end_time time,
                   DOW character varying(25),
                   cert_required integer,
                   SaID integer,
                   number_needed integer) as $$
begin

    return query select s.stid,
                        s.shift_name,
                        s.start_time,
                        s.end_time,
                        s.dow,
                        s.cert_required,
                        s.said,
                        s.number_needed
                 from shift_templates as s
                 where s.said=(select * from get_current_season()) and
                       s.dow=p_dow and
                       s.deleted = FALSE
                 order by s.dow, s.shift_name;
end $$
LANGUAGE plpgsql;
-- end get_current_shift_templates(dow varchar(25))

create or replace function list_available(p_sid integer)
    returns table (empID integer,
                   first_name varchar(50),
                   last_name varchar(50),
                   suffix varchar(5),
                   nickname varchar(45),
                   dob date,
                   sex varchar(6)
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
 return query select a.eid,e.firstname,e.lastname, e.suffix, e.nickname, e.dob, e.sex from employee_availability as a
inner join employee as e on a.eid=e.eid
where a.start_time <= (p_start_time)
      and a.end_time >= (p_end_time)
      and a.dow = (p_dow)
      and a.said = (select * from get_current_season())
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

create or replace function list_current_employees()
    returns table (eid integer,
                  esid integer) as $$
begin
    return query select s.eid, s.esid
                 from employee_seasons as s
                 where s.said=(select * from get_current_season());
                 
end; $$
LANGUAGE plpgsql;

create function list_shifts_for_date(p_shift_date date)
    returns table (sid integer,
                   shift_name varchar(50),
                   shift_date date,
                   start_time time,
                   end_time time,
                   eid integer,
                   firstname varchar(30),
                   lastname varchar(30),
                   no_show boolean,
                   student_level varchar(25),
                   student_count integer,
                   worked_time numeric(6,2),
                   ct integer,
                   cancelled boolean,
                   html_class varchar(20)) as $$
begin
    return query select s.sid,
       s.shift_name,
       s.shift_date,
       s.start_time,
       s.end_time,
       s.eid,
       e.firstname,
       e.lastname,
       s.no_show,
       s.student_level,
       s.student_count,
       s.worked_time,
       s.ct,
       s.cancelled,
       s.html_class
from shifts as s
full join employee as e on s.eid=e.eid
where s.shift_date=p_shift_date;

end; $$
LANGUAGE plpgsql;  

create or replace function list_shift(p_shift_date date)
    returns table (eid integer,
                   firstname varchar(50),
                   lastname varchar(50),
                   shift_name varchar(50),
                   start_time time,
                   end_time time,
                   html_class varchar(20)) as $$
begin
    return query select s.eid,
                        e.firstname,
                        e.lastname,
                        s.shift_name,
                        s.start_time,
                        s.end_time,
                        s.html_class
                        
                 from shifts as s
                 inner join employee as e on s.eid=e.eid
                 where s.shift_date=p_shift_date
                 order by e.lastname,e.firstname,s.start_time,s.end_time;
                
end; $$
LANGUAGE plpgsql;

create function update_employee_availability_dow(p_eaid integer,
                                                 p_dow varchar(15))
    returns integer as $$
begin
    update employee_availability set dow = p_dow where eaid=p_eaid;
    return 1;
end;$$
LANGUAGE plpgsql;

create function update_employee_availability_start(p_eaid integer,
                                                   p_start time)
    returns integer as $$
begin
    update employee_availability set start_time = p_start where eaid=p_eaid;
    return 1;
end; $$
LANGUAGE plpgsql;

create function update_employee_availability_end(p_eaid integer,
                                                 p_end time)
    returns integer as $$
begin
    update employee_availability set end_time = p_end where eaid=p_eaid;
    return 1;
end; $$
LANGUAGE plpgsql;
-- end update_employee_availablility_end()

create or replace function update_employee_extra_day(p_eeid integer,
                                                     p_eid integer,
                                                     p_et integer,
                                                     p_priority integer)
    returns integer as $$
begin
    update employee_extra_days
        set eid=p_eid,
            et=p_et,
            priority=p_priority
        where eeid=p_eeid;
    return 1;
end; $$
LANGUAGE plpgsql;
-- end update_employee_extra_day()

create or replace function update_extra_days_template(p_et integer,
                                           p_title varchar(40),
                                           p_extra_date date,
                                           p_points integer,
                                           p_ideal_max integer)
    returns integer as $$
begin
    update extra_days_templates
           set title=p_title,
               extra_date=p_extra_date,
               points=p_points,
               ideal_max=p_ideal_max
           where et=p_et;
    return 1;
end; $$
LANGUAGE plpgsql;
-- end update_extra_days_template()

create function update_shifts_student_count(p_sid integer,
                                            p_student_count integer)
    returns integer as $$
begin
    update shifts set student_count=p_student_count where sid=p_sid;
    return 1;
end; $$
LANGUAGE plpgsql;

-- end update_shifts_student_count()
create function update_shifts_student_level(p_sid integer,
                                            p_student_level varchar(25))
    returns integer as $$
begin
    update shifts set student_level=p_student_level where sid=p_sid;
    return 1;
end; $$
LANGUAGE plpgsql;
-- end update_shifts_student_level()

create function update_shifts_worked_time(p_sid integer,
                                           p_worked_time numeric(6,2))
    returns integer as $$
begin
    update shifts set worked_time=p_worked_time where sid=p_sid;
    return 1;
end; $$
LANGUAGE plpgsql;

-- end update_shifts_worked_time(sid, worked_time)

create or replace function update_shift_template(p_stid integer,
                                        p_shift_name varchar(45),
                                        p_start_time time,
                                        p_end_time time,
                                        p_dow varchar(25),
                                        p_cert_required integer,
                                        p_said integer,
                                        p_number_needed integer
                                       )
    returns integer as $$
begin
    update shift_templates
        set shift_name=p_shift_name,
            start_time=p_start_time,
            end_time=p_end_time,
            dow=p_dow,
            cert_required=p_cert_required,
            said=p_said,
            number_needed=p_number_needed
        where stid=p_stid;
    return 1;
end; $$
LANGUAGE plpgsql;
-- end update_shift_template

create function shift_count_date_range(start_date date,
                                       end_date date)
    returns table(eid integer,
                  lastname varchar(45),
                  suffix varchar(5),
                  firstname varchar(45),
                  shift_count bigint,
                  scheduled_hours double precision,
                  worked_hours numeric(6,2)) as $$
begin
    return query select e.eid,
           e.lastname,
           e.suffix,
           e.firstname,
           count(s.eid),
           sum(extract(epoch from (s.end_time-s.start_time)) / 3600),
           sum(s.worked_time)
    from shifts as s
    inner join employee as e on s.eid=e.eid
    where s.shift_date between start_date and end_date
    group by e.eid
    order by e.lastname, e.suffix, e.firstname;
end; $$
LANGUAGE plpgsql;

create or replace function test_excute (hal varchar(45))
    returns table(sid integer,
                  pid integer,
                  eid integer) as $$
declare
    myquery text;
begin
    myquery := 'select sid, pid, assigned_eid from private_lesson where  c_firstname ilike '''||hal||''' ';
    return query execute myquery;
end; $$
LANGUAGE plpgsql;

    
create or replace function private_eid_null() returns trigger as $$
declare
    unassigned_eid integer;
begin

    if new.assigned_eid is Null then
        select into unassigned_eid eid from employee where firstname='Unassigned' and lastname='Shift';
        update private_lesson set assigned_eid = unassigned_eid where pid=new.pid;
    end if;
    return new; 
end; $$
LANGUAGE plpgsql;

create TRIGGER new_private
    after insert
    on private_lesson
    for each row
    execute procedure private_eid_null();
    
create or replace function get_sid_by_date_range(s_date date,
                                                 e_date date) returns 
---- hold -----
where 
                   p.s_lastname ilike p_student_lastname and
                   p.s_skill_level ilike p_student_skill and
                   p.c_firstname  ilike p_contact_firstname and
                   p.c_lastname ilike p_contact_lastname and
                   p.c_phone ilike p_student_skill and
                   p.lesson_type ilike p_type  and
                   p.lesson_disapline ilike p_disapline and 
                   p.s_age is null and
---- end hold ------
create or replace function get_avaliablity_count(p_start_time time,
                                                 p_end_time time,
                                                 p_dow varchar(25),
                                                 p_ct integer)
    returns integer as $$
declare
    p_count integer;
begin
    select into p_count count(*)
    from employee_availability
    where said=(select * from get_current_season()) and
          eid in (select eid from certs where ct in (select ct_min_equal from cert_min where ct=p_ct)) and
          dow=p_dow and
          start_time <= p_start_time and
          end_time >=p_end_time;
    return p_count;
end; $$
LANGUAGE plpgsql;

-- end get_avaliablity_count(time, time, varchar(25), integer)
select (select * from get_avaliablity_count('17:00', '18:00', 'tuesday', 2)) as Snowboard,
       (select * from get_avaliablity_count('17:00', '18:00', 'tuesday', 15)) as "SB Level 1",
       (select * from get_avaliablity_count('17:00', '18:00', 'tuesday', 16)) as "SB Level 2",
       (select * from get_avaliablity_count('17:00', '18:00', 'tuesday', 16)) as "SB Level 3",
       (select * from get_avaliablity_count('17:00', '18:00', 'tuesday', 3)) as "Ski",
       (select * from get_avaliablity_count('17:00', '18:00', 'tuesday', 18)) as "Ski level 1",
       (select * from get_avaliablity_count('17:00', '18:00', 'tuesday', 19)) as "Ski level 2",
       (select * from get_avaliablity_count('17:00', '18:00', 'tuesday', 20)) as "Ski level 3";

select (select * from get_avaliablity_count('18:00', '19:00', 'tuesday', 2)) as Snowboard,
       (select * from get_avaliablity_count('18:00', '19:00', 'tuesday', 15)) as "SB Level 1",
       (select * from get_avaliablity_count('18:00', '19:00', 'tuesday', 16)) as "SB Level 2",
       (select * from get_avaliablity_count('18:00', '19:00', 'tuesday', 16)) as "SB Level 3",
       (select * from get_avaliablity_count('18:00', '19:00', 'tuesday', 3)) as "Ski",
       (select * from get_avaliablity_count('18:00', '19:00', 'tuesday', 18)) as "Ski level 1",
       (select * from get_avaliablity_count('18:00', '19:00', 'tuesday', 19)) as "Ski level 2",
       (select * from get_avaliablity_count('18:00', '19:00', 'tuesday', 20)) as "Ski level 3";
