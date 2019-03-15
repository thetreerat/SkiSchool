create table jacket
     (  JID serial primary key,
        jacket_type character varying(250),
        Jacket_number character varying(5),
        Jacket_size character varying(5),
        EID integer,
        Modifiy_date timestamp
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
Create table jacket_history
    (  JHID serial primary key,
       JID integer,
       EID integer,
       history_date date,
       In_Out character varying(4)
    )
;