create table jacket
     (  JID serial primary key,
        jacket_type character varying(250),
        Jacket_number character varying(5),
        Jacket_size character varying(5),
        EID integer,
        Modifiy_date timestamp,
        jacket_condition integer,
        lid integer,
        notes varchar(300),
        foreign key (EID) references employee (EID) on delete restrict,
        foreign key (jacket_condition) references jacket_condition_template (cot) on delete restrict,
        foreign key (lid) references location (lid) on delete restrict
     )
;
Create table jacket_damage
    (  DID serial primary key,
       JID integer,
       Damage character varying(250),
       Fixed integer default 0,
       reported_date timestamp,
       fixed_date timestamp default null
    )
;
create table jacket_condition_template
    (cot serial primary key,
     condition varchar(30)
    );
    
Create table jacket_history
    (  JHID serial primary key,
       JID integer,
       EID integer,
       history_date date,
       old_eid integer,
       In_Out character varying(4),
       foreign key (eid) references employee (eid) on delete restrict,
       foreign key (old_eid) references employee (eid) on delete restrict,
       foreign key (jid) references jacket (jid) on delete restrict
    )
;

create table location
    (lid serial primary key,
     location_name varchar(30),
     location_size varchar(30),
     lock_sn varchar(10) UNIQUE,
     lock_combination varchar(10),
     notes varchar(300)
     );
     
create table employee_locations
    (elid serial primary key,
    lid integer,
    eid integer,
    foreign key (eid) references employee (eid) on delete restrict,
    foreign key (lid) references location (lid) on delete restrict);
    
create table location_history
    (lhid serial primary key,
     lid integer,
     assigned_eid integer,
     previous_eid integer,
     tracking_user varchar(30),
     in_out varchar(5),
     history_datetime timestamp,
     foreign key (assigned_eid) references employee (eid) on delete restrict,
     foreign key (previous_eid) references employee (eid) on delete restrict,
     foreign key (lid) references location (lid) on delete restrict);