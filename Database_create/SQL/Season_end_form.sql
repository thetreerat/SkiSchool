create table season_end_form
    (  SEFID serial primary key,
       SID integer default 1,
       EID integer,
       returning integer,
       location_jacket character varying(25),
       message_id integer default 1,
       notes character varying(250),
       completed_date timestamp
    )
create table season_end_message
    (  message_id serial primary key,
       message character varying(500),
       create_date timestamp
    )