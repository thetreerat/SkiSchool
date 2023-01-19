# SkiSchool
postgres database with python data entry code

Warning this is only currently being test on mac os but is intened to be use on window, mac, and linux<br>
<br>
directory stucture and usess<br>
Database_create<br>
  \build_skischool.sh  - creates database base skischool, tables, views, stored procedures, and load test data<br>
  \CSV - test data csv files need by build_skischool.sh, you can use these files to load your own data by modifing them.<br>
  \Python - python scripts for loading and mangage data. files that start with load_*.py are for bulk data loads, and use functions of database.<br>
  \SQL - sql scripts for createing table, views, stored procedure, and some original load scripts.<br> 
 <br>
 To start Application in the python directory run main.py<br>
     python main.py
