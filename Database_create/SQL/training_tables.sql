create table training_log_header
    (tlid serial primary key,
     training_date date,
     lead_instructor integer,
     location varchar(30),
     training_title varchar(40),
     training_description text,
     header_notes text,
     create_date date default now(),
     inserting_user varchar(30) default current_user,
     lock_roster boolean default False,
     said integer default get_current_season(),
     foreign key (lead_instructor) references employee (EID) on delete restrict,
     foreign key (said) references seasons (said) on delete restrict);
-- end table train_logs

create table employee_training_roster
    (rid serial primary key,
     tlid integer,
     eid integer,
     notes text,
     insert_date timestamp default now(),
     insert_user varchar(30) default current_user,
     said integer default get_current_season(),
     foreign key (eid) references employee (eid) on delete restrict,
     foreign key (tlid) references training_log_header on delete restrict,
     foreign key (said) references seasons on delete restrict);

create or replace function add_training_header(p_training_date date,
                                               p_lead_instructor integer,
                                               p_location varchar(30),
                                               p_training_title varchar(40),
                                               p_training_description text,
                                               p_notes text,
                                               
                                               )
    returns integer as $$
declare
    r_tlid integer;
begin
    insert into training_log_header (training_date,
                                     lead_instructor,
                                     location,
                                     training_title,
                                     training_description,
                                     header_notes,
                                     insert_user,)
    values (p_training_date,
            p_lead_instructor,
            p_location,
            p_training_title,
            p_training_description,
            p_notes,
            );
    select into r_tlid max(tlid)
        from training_log_header
        where training_date=p_training_date and
              training_title=p_training_title;
    return r_tlid;
end; $$
LANGUAGE plpgsql;
-- end list_avlailable_location()

create or replace function update_training_header(p_tlid integer,
                                                  p_training_date date,
                                                  p_lead_instructor integer,
                                                  p_location varchar(30),
                                                  p_training_title varchar(40),
                                                  p_training_description text,
                                                  p_notes text
                                               )
    returns integer as $$
begin
    update training_log_header
    set training_date=p_training_date,
                                   lead_instructor=p_lead_instructor,
                                   location=p_location,
                                   training_title=p_training_title,
                                   training_description=p_training_description,
                                   header_notes=p_notes
    where tlid=p_tlid;                            
    return p_tlid;
end; $$
LANGUAGE plpgsql;
-- end update_training_header()

create or replace function get_current_tlid()
    returns table(r_tlid integer) as $$
begin
    return query select tlid
                 from training_log_header
                 where lock_roster=False and
                       said=get_current_season();
end; $$
LANGUAGE plpgsql;
-- end get_current_tlid(integer)

create or replace function get_season_tlid(p_said integer)
    returns table(r_tlid integer) as $$
begin
    return query select tlid
                 from training_log_header
                 where said=p_said;
end; $$
LANGUAGE plpgsql;
-- end get_season_tlid(p_said integer)
create or replace function get_season_open_tlid(p_said integer)
    returns table(r_tlid integer) as $$
begin
    return query select tlid
                 from training_log_header
                 where lock_roster=False and
                       said=p_said;
end; $$
LANGUAGE plpgsql;
-- end get_season_tlid(said integer)

create or replace function get_training_log_header(p_tlid integer)
    returns table(tlid integer,
                  training_date date,
                  lead_instructor integer,
                  location varchar(30),
                  training_title varchar(40),
                  training_description text,
                  header_notes text,
                  said integer) as $$
begin
    return query
           select h.tlid,
                  h.training_date,
                  h.lead_instructor,
                  h.location,
                  h.training_title,
                  h.training_description,
                  h.header_notes,
                  h.said
            from training_log_header as h
            where h.tlid=p_tlid;
end; $$
LANGUAGE plpgsql;
-- end get_training_log_header()

create or replace function update_eid_roster(p_rid integer,
                                             p_tlid integer,
                                             p_eid integer,
                                             p_notes text)
    returns integer as $$
declare
    locked boolean;
begin
    select into locked lock_roster from training_log_header where tlid=p_tlid;
    if not locked then
        update employee_training_roster
           set tlid=p_tlid,
               eid=p_eid,
               notes=p_notes
           where rid=p_rid;
        return 1;
    end if;
    return 0;
end; $$
LANGUAGE plpgsql;
-- end of update_eid_roster
create or replace function list_training_roster(p_tlid integer)
    returns table(rid integer,
                  tlid integer,
                  eid integer,
                  notes text,
                  said integer) as $$
begin
    return query select r.rid,
                        r.tlid,
                        r.eid,
                        r.notes,
                        r.said
                 from employee_training_roster as r
                 where r.tlid=p_tlid;
end; $$
LANGUAGE plpgsql;
-- end list_training_roster(tlid)

create or replace function lock_roster(p_tlid integer)
    returns integer as $$
declare
    r_tlid integer;
begin
    select into r_tlid tlid from training_log_header where tlid=p_tlid;
    if r_tlid is null then
        return 0;
    else
        update training_log_header set lock_roster=True where tlid=p_tlid;
    end if;    
    return r_tlid;
end; $$
LANGUAGE plpgsql;
-- end lock_roster(integer)
create or replace function add_eid_roster(p_tlid integer, p_eid integer, p_notes text)
    returns integer as $$
declare
    r_rid integer;
    locked boolean;
begin
    select into locked lock_roster from training_log_header where tlid=p_tlid;
    if locked then
        return 0;
    else
        select into r_rid rid from employee_training_roster where tlid=p_tlid and eid=p_eid;
        if r_rid is null then
            insert into employee_training_roster (tlid, eid, notes)
                values (p_tlid, p_eid, p_notes);
            
            select into r_rid rid
            from employee_training_roster
            where eid=p_eid and
                  tlid=p_tlid;
              
        end if;
    end if;
    return r_rid;
end; $$
LANGUAGE plpgsql;
-- end add_eid_roster()

create or replace function delete_rid_training_roster(p_rid integer)
    returns integer as $$
begin
    delete from employee_training_roster where rid=p_rid;
    return 1;
end; $$
LANGUAGE plpgsql;
-- end delete_eid_training_roster(integer)