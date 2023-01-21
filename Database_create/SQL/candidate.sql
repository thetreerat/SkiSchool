create table candidates
     (  caid serial primary key,
        eid integer,
        lastname character varying(30),
        firstname character varying(30),
        suffix varchar(5),
        nickname varchar(30),
        sex varchar(1),
        dob date,
        passed boolean default null,
        notes text,
        hire date default null,
        classranking integer default Null,
        discipline integer,
        phone_cell varchar(10),
        said integer default get_current_season(),
        cat integer
     )
;
