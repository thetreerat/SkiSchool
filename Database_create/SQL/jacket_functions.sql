create function add_jacket(p_jacket_type varchar(250),
                           p_jacket_number varchar(5),
                           p_jacket_size varchar(5)) returns varchar(150) as $$
declare
    p_result varchar(150);
    p_eid integer;
    p_cot integer;
    p_lid integer;
    p_jid integer;
begin
    select into p_eid eid from employee where lastname='Jacket' and firstname='New';
    select into p_cot cot from jacket_condition_template where condition='New';
    select into p_lid lid from location where location_name ='Admin Office';
    insert into jacket (jacket_type,
                        jacket_number,
                        jacket_size,
                        eid,
                        modifiy_date,
                        jacket_condition,
                        lid)
    values (p_jacket_type,
            p_jacket_number,
            p_jacket_size,
            p_eid,
            now(),
            p_cot,
            p_lid);
    select into p_jid jid from jacket
    where jacket_type=p_jacket_type and
          jacket_number=p_jacket_number and
          jacket_size=p_jacket_size;
    insert into jacket_history (jid,
                                eid,
                                history_date,
                                in_out,
                                tracked_user)
    values (p_jid, p_eid, current_date, 'New', user);
    return p_result;
end; $$
LANGUAGE plpgsql;

-- end of add_jackete()
create function check_out_jacket(p_firstname varchar(30),
                                 p_lastname varchar(30,)
                                 p_jid integer,
                                 p_location_name varchar(30)) returns varchar(150) as $$
declare
    p_jacket_number integer;
    p_result varchar(150);
    p_name varchar(150);
    p_lid integer;
begin
    select into p_name firstname||' '||lastname from employee where eid=p_eid;
    select into p_lid lid from location where location_name=p_location_name;
    if p_name is not null then
        insert into jacket_history (eid,
                                    jid,
                                    tracked_user,
                                    in_out,
                                    old_eid,
                                    history_date)
        values (p_eid,
                p_jid,
                user,
                'Out',
                (select eid from jacket where jid=p_jid),
                current_date);
        select into p_jacket_number jacket_number from jacket where jid=p_jid;
        update jacket set eid=p_eid, lid=p_lid, modifiy_date=now() where jid=p_jid;
        p_result := 'jacket number: '||p_jacket_number||' assigned to '||p_name;
    else
        p_result := 'Error: eid '||p_eid||' is not in the database!!';
    end if;
    return p_result;
end; $$
LANGUAGE plpgsql;

create function check_out_jacket(p_eid integer,
                                 p_jid integer,
                                 p_lid integer)) returns integer as $$
declare
    p_jhid integer;
begin

        insert into jacket_history (eid,
                                    jid,
                                    tracked_user,
                                    in_out,
                                    old_eid,
                                    history_date)
        values (p_eid,
                p_jid,
                user,
                'Out',
                (select eid from jacket where jid=p_jid),
                current_date);                
        select into p_jhid max(jhid) from jacket_history where jid=p_jid;
        update jacket set eid=p_eid, lid=p_lid, modifiy_date=now() where jid=p_jid;
    
    return p_result;
end; $$
LANGUAGE plpgsql;

-- end of check_out_jacket()

create function check_in_jacket(p_jid integer,
                                p_returning integer,
                                p_lid integer) returns varchar(150) as $$
declare
    p_result varchar(150);
    p_eid integer;
    c_eid integer;
begin
    select into p_eid eid from employee where lastname = 'Jacket' and firstname='Unassigned';
    select into c_eid eid from jacket where jid=p_jid;
    insert into jacket_history (eid,
                                jid,
                                tracked_user,
                                in_out,
                                old_eid,
                                history_date)
    values (p_eid,
            p_jid,
            user,
            'In',
            c_eid,
            current_date);
    update employee_seasons set employee_returning=p_returning where eid=c_eid and said=get_current_season();
    update jacket set eid=p_eid, modifiy_date=now() where jid=p_jid;
    return p_result;
end; $$
LANGUAGE plpgsql;

-- end of check_in_jacket()

create function get_jacket(p_jid integer)
    returns table (jid integer,
                   jacket_type varchar(250),
                   jacket_number varchar(5),
                   jacket_size varchar(5),
                   eid integer,
                   firstname varchar(30),
                   lastname varchar(30),
                   cot integer,
                   condition varchar(30),
                   lid integer,
                   Location varchar(30)
                  ) as $$
begin
    return query select j.jid,
                        j.jacket_type,
                        j.jacket_number,
                        j.jacket_size,
                        j.eid,
                        e.firstname,
                        e.lastname,
                        j.jacket_condition,
                        c.condition,
                        j.lid,
                        l.location_name
                 from jacket as j
                 inner join employee as e on e.eid=j.eid
                 full join jacket_condition_template as c on c.cot=j.jacket_condition
                 full join location as l on j.lid=l.lid
                 where j.jid=p_jid;
                        
end; $$
Language plpgsql;

-- end get_jacket()
create function get_employee_jackets(p_eid integer)
    returns table (jid integer,
                   jacket_type varchar(250),
                   jacket_number varchar(5),
                   jacket_size varchar(5),
                   eid integer,
                   lid integer,
                   location_name varchar(30),
                   jacket_condition integer,
                   condition varchar(30)) as $$
begin
    return query select j.jid,
                        j.jacket_type,
                        j.jacket_number,
                        j.jacket_size,
                        j.eid,
                        j.lid,
                        l.location_name,
                        j.jacket_condition,
                        c.condition
                 from jacket as j
                 inner join jacket_condition_template as c on j.jacket_condition=c.cot
                 full join location as l on j.lid=l.lid
                 where j.eid=p_eid;
end; $$
Language plpgsql;

-- end get_employee_jackets()
create function get_jacket(p_jacket_type varchar(250),
                           p_jacket_size varchar(5),
                           p_jacket_number varchar(5)
                           )
        returns table (jid integer,
                   jacket_type varchar(250),
                   jacket_number varchar(5),
                   jacket_size varchar(5),
                   eid integer,
                   lid integer,
                   location_name varchar(30),
                   jacket_condition integer,
                   condition varchar(30)) as $$
begin
    return query select j.jid,
                        j.jacket_type,
                        j.jacket_number,
                        j.jacket_size,
                        j.eid,
                        j.lid,
                        l.location_name,
                        j.jacket_condition,
                        c.condition
                 from jacket as j
                 inner join jacket_condition_template as c on j.jacket_condition=c.cot
                 full join location as l on j.lid=l.lid
                 where j.jacket_type ilike p_jacket_type and
                       j.jacket_size ilike p_jacket_size and
                       j.jacket_number ilike p_jacket_number;
end; $$
Language plpgsql;

-- end of get_jacket(jacket_size, jacket_type, jacket_number)
create function get_jacket_history(p_jid integer)
    returns table (history_date date,
                   in_out varchar(4),
                   firstname varchar(30),
                   lastname varchar(30),
                   who_updated varchar(50),
                   eid integer
                   ) as $$
begin
    return query select  h.history_date,
                         h.in_out,
                         e.firstname, 
                         e.lastname,
                         h.tracked_user,
                         h.eid
    from jacket_history as h
    inner join employee as e on h.eid=e.eid
    where jid=p_jid
    order by history_date;
end; $$
Language plpgsql;

-- end get_jacket_history()

create function list_available_jacket(p_jacket_size varchar(5),
                                      p_jacket_type varchar(250))
    returns table (jid integer,
                   jacket_type varchar(250),
                   jacket_number varchar(5),
                   jacket_size varchar(5),
                   jacket_condition varchar(30)
                   ) as $$
begin
    return query select j.jid,
                        j.jacket_type,
                        j.jacket_number,
                        j.jacket_size,
                        t.condition
                 from jacket as j
                 inner join jacket_condition_template as t on j.jacket_condition=t.cot
                 where eid in ((select eid from employee where lastname='Jacket' and firstname='New'),
                               (select eid from employee where lastname='Jacket' and firstname='Unassigned')) and
                       j.jacket_size=p_jacket_size and
                       j.jacket_type like p_jacket_type
                 order by j.jacket_type, j.jacket_number, j.jacket_condition;
end; $$
Language plpgsql;

-- end of list_available_jacket(size, type)

create function list_available_jacket(p_jacket_size varchar(5))
    returns table (jid integer,
                   jacket_type varchar(250),
                   jacket_number varchar(5),
                   jacket_size varchar(5),
                   jacket_condition varchar(30),
                   lid integer,
                   location varchar(30)
                   ) as $$
begin
    return query select j.jid,
                        j.jacket_type,
                        j.jacket_number,
                        j.jacket_size,
                        t.condition,
                        j.lid,
                        l.location_name
                 from jacket as j
                 full join jacket_condition_template as t on j.jacket_condition=t.cot
                 full join location as l on j.lid=l.lid
                 where eid in ((select eid from employee where lastname='Jacket' and firstname='New'),
                               (select eid from employee where lastname='Jacket' and firstname='Unassigned')) and
                       j.jacket_size=p_jacket_size
                 order by j.jacket_type, j.jacket_number, j.jacket_condition;
end; $$
Language plpgsql;

-- end of list_avaliable_jacket()

create function add_location (p_location_name varchar(30),
                              p_location_size varchar(30),
                              p_notes varchar(300))
    returns integer as $$
declare
    p_lid integer;
    p_eid integer;
begin
    select into p_eid eid from employee where firstname='New' and lastname='Location';
    insert into location (location_name, location_size, notes) values (p_location_name, p_location_size, p_notes);
    select into p_lid max(lid) from location where location_name=p_location_name;
    insert into employee_locations (lid, eid) values (p_lid, p_eid);
    insert into location_history (lid,
                                  assigned_eid,
                                  history_datetime,
                                  tracking_user,
                                  in_out)
            values (p_lid,
                    p_eid,
                    now(),
                    current_user,
                    'New');
    return p_lid;
end; $$
LANGUAGE plpgsql;

-- end of add_location

create function assign_location (p_eid integer,
                                 p_lid integer)
    returns integer as $$
declare
    p_elid integer;
    c_eid integer;
begin
    select into p_elid max(elid) from employee_locations where lid=p_lid;
    select into c_eid eid from employee_locations where elid=p_elid;
    insert into location_history (lid,
                                  assigned_eid,
                                  previous_eid,
                                  tracking_user,
                                  in_out,
                                  history_datetime)
            values (p_lid, p_eid, c_eid, current_user, 'Assign', now());
            
    update employee_locations set eid = p_eid where elid=p_elid; 
    return p_elid;
end; $$
LANGUAGE plpgsql;
-- end of assing_locatoin()


create function list_available_location()
    returns table (elid integer,
                   lid integer,
                   eid integer,
                   location_name varchar(30),
                   location_size varchar(30),
                   firstname varchar(30),
                   lastname varchar(30)) as $$
begin
    return query select e.elid,
                        e.lid,
                        e.eid,
                        l.location_name,
                        l.location_size,
                        n.firstname,
                        n.lastname
                from location as l
                full join employee_locations as e on e.lid=l.lid
                full join employee as n on e.eid=n.eid
                where e.eid in ((select get_location_eid()))
                order by l.location_size, l.location_name;
end; $$
LANGUAGE plpgsql;

create function list_available_location(p_location_size varchar(30))
    returns table (elid integer,
                   lid integer,
                   eid integer,
                   location_name varchar(30),
                   location_size varchar(30),
                   firstname varchar(30),
                   lastname varchar(30)) as $$
begin
    return query select e.elid,
                        e.lid,
                        e.eid,
                        l.location_name,
                        l.location_size,
                        n.firstname,
                        n.lastname
                from location as l
                full join employee_locations as e on e.lid=l.lid
                full join employee as n on e.eid=n.eid
                where e.eid in (select get_location_eid()) and
                      l.location_size=p_location_size
                order by l.location_size, l.location_name;
end; $$
LANGUAGE plpgsql;

-- end get_available_locations(size)
create function get_locations_for_eid(p_eid integer)
    returns table (location_name varchar(30),
                   location_size varchar(30),
                   lid integer,
                   elid integer,
                   lock_sn varchar(10),
                   lock_comination varchar(10)) as $$
begin
    return query select l.location_name,
                        l.location_size,
                        l.lid,
                        e.elid,
                        l.lock_sn,
                        l.lock_combination
                 from employee_locations as e
                 inner join location as l on e.lid=l.lid
                 where e.eid=p_eid
                 order by l.lid;
end; $$
LANGUAGE plpgsql;

-- end of get_locations_for_id()
                 
create function get_location_eid()
    returns table (eid integer) as $$
begin
    return query select employee.eid from employee where lastname='Location';
end; $$
language plpgsql;

create function get_elid(p_lid integer)
    returns integer as $$
declare
    p_elid integer;
begin
    return p_elid;
end; $$
LANGUAGE plpgsql;
    