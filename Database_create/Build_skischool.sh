if psql -lqt | cut -d \| -f 1 | grep -qw skischool; then
    # database exists
    printf "%s\n"
    printf "%s\n" "Database already exists!"
    printf "%s\n"
    read -p 'Delete it?: ' databasedelete
    if [ $databasedelete = 'YES' ]
    then
      printf "%s\n" "bye bye database!"
      psql -f /Users/halc/source/SkiSchedule/Database_create/sql/deleteskischool.sql postgres
    else
        printf "%s\n" $databasedelete
        printf "%s\n" "database left alone!"
        exit
    fi
fi
psql -f /Users/halc/source/SkiSchedule/Database_create/sql/Schedule_tables.sql -d postgres
psql -f /Users/halc/source/SkiSchedule/Database_create/sql/Schedule_functions.sql -d postgres
psql -f /Users/halc/source/SkiSchedule/Database_create/sql/jackets.sql -d skischool
python python/load_employees.py /Users/halc/source/SkiSchedule/Database_create/csv/Employee_data.csv
psql -f /Users/halc/source/SkiSchedule/Database_create/sql/data_load.sql -d skischool
psql -f /Users/halc/source/SkiSchedule/Database_create/sql/Add_test_data.sql -d skischool
psql -f /Users/halc/source/SkiSchedule/Database_create/sql/jacket_test_data.sql -d skischool
psql -f /Users/halc/source/SkiSchedule/Database_create/sql/calendar_dates.sql -d skischool
python python/load_emp_certs.py /Users/halc/source/SkiSchedule/Database_create/csv/emp_cert_list.csv
python python/load_emp_avail.py /Users/halc/source/SkiSchedule/Database_create/csv/emp_a.csv
python python/load_cert_min.py /Users/halc/source/SkiSchedule/Database_create/csv/cert_min.csv
python python/load_shift_templates.py /Users/halc/source/SkiSchedule/Database_create/csv/Shift_templates.csv