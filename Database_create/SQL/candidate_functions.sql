create or replace function add_candidate(p_firstname varchar(30),
                              p_lastname varchar(30),
                              p_suffix varchar(5),
                              p_nickname varchar(30),
                              p_sex varchar(1),
                              p_dob date,
                              p_discipline integer,
                              p_phone_cell varchar(10)) returns varchar(150) as $$
declare
    r_caid integer;
    r_result varchar(150);
begin
    select into r_caid caid
    from candidates 
    where firstname=p_firstname and 
          lastname=p_lastname and
          said=get_current_season(); 
    if r_caid is null then 
      insert into candidates (firstname,
                              lastname,
                              suffix,
                              nickname,
                              sex,
                              dob,
                              discipline,
                              phone_cell)
          values (p_firstname,
                  p_lastname,
                  p_suffix,
                  p_nickname,
                  p_sex,
                  p_dob,
                  p_discipline,
                  p_phone_cell);
      select into r_caid caid
        from candidates
        where firstname=p_firstname and 
              lastname=p_lastname and
              said=get_current_season();
    end if;
    return r_caid;
end; $$
LANGUAGE plpgsql;

