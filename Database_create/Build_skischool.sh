if psql -lqt | cut -d \| -f 1 | grep -qw skischool; then
    # database exists
    printf "%s\n"
    printf "%s\n" "Database already exists!"
    printf "%s\n"
    read -p 'Delete it?: ' databasedelete
    if [ $databasedelete = 'YES' ]
    then
      printf "%s\n" "bye bye database!"
      psql -f /Users/halc/source/SkiSchool/Database_create/sql/deleteskischool.sql postgres
    else
        printf "%s\n" $databasedelete
        printf "%s\n" "database left alone!"
        exit
    fi
fi
printf "%s\n Adding employee and schedule tables."
# add employee, schedule tables
psql -f /Users/halc/source/SkiSchool/Database_create/SQL/Schedule_tables.sql -d postgres
printf "%s\n Adding employee and schedule functions."
psql -f /Users/halc/source/SkiSchool/Database_create/SQL/Schedule_functions.sql -d skischool
psql -f /Users/halc/source/SkiSchool/Database_create/SQL/calendar_dates.sql -d skischool

printf "%s\n Adding jackets and location tables."
psql -f /Users/halc/source/SkiSchool/Database_create/SQL/jackets.sql -d skischool
psql -f /Users/halc/source/SkiSchool/Database_create/SQL/jacket_functions.sql -d skischool
psql -f /Users/halc/source/SkiSchool/Database_create/SQL/jacket_test_data.sql -d skischool

printf "%s\n Loading standard function data."
python python/load_seasons.py /Users/halc/source/SkiSchool/Database_create/CSV/seasons.csv
python python/load_cert.py /Users/halc/source/SkiSchool/Database_create/CSV/cert_data.csv
python python/load_emp_certs.py /Users/halc/source/SkiSchool/Database_create/CSV/emp_cert_list.csv
python python/load_cert_min.py /Users/halc/source/SkiSchool/Database_create/CSV/cert_min.csv
python python/load_languages.py /Users/halc/source/SkiSchool/Database_create/CSV/language.csv

printf "%s\n Loading current season data (extra days, Shift templates)."
python python/load_extra_days.py /Users/halc/source/SkiSchool/Database_create/CSV/extra_days.csv
python python/load_shift_templates.py /Users/halc/source/SkiSchool/Database_create/CSV/Shift_templates.csv

printf "%s\n Loading current season Test data (extra days, Shift templates)."
psql -f /Users/halc/source/SkiSchool/Database_create/SQL/data_load.sql -d skischool
psql -f /Users/halc/source/SkiSchool/Database_create/SQL/Add_test_data.sql -d skischool

printf "%s\n Loading existing employees."
python python/load_employees.py /Users/halc/source/SkiSchool/Database_create/CSV/Employee_data.csv

#printf "%s\n Loading avaliblity for employees from database export"
#python python/load_emp_avail.py /Users/halc/source/SkiSchool/Database_create/csv/emp_a.csv
printf "%s\n Database Build Complete!"
