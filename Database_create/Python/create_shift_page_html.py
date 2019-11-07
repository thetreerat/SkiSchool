import psycopg2
import sys
import csv
from time import strptime
from datetime import timedelta
from html_page import html
from employee import employee
from employee import employees
from shift import shift
from database import database

    
    
print('createing html shift page ...')
shift_columns=42
db_handle = database(owner='create_shift_page_html.py')
shift_date=sys.argv[1]
#password=sys.argv[2]
p = html()

#c = psycopg2.connect(user="postgres",
#                     port="5432",
#                     host="127.0.0.1",
#                     database="skischool")
#cur = c.cursor()
#cur.callproc
result = db_handle.fetchdata('list_shift', [shift_date,])

count = 0
#data = {}
data = employees(db_handle=db_handle)
for r in result:
    count+=1
    s = shift(shift_name=r[3],start_time=r[4],end_time=r[5],html_class=r[6])
    i = data.check_name(r[0],r[1])
    if i==None:
        e = employee(eid=r[0], firstname=r[1],lastname=r[2], db_handle=db_handle)
        e.shifts.append(s)
        data.append(e)
    else:
        data.elist[i].shifts.append(s)
    
print """Total rows: %s""" % (count)
t = p.shift_table_header(cells=shift_columns)
for d in data.elist:
    #print(d)
    d.print_self()
    t = """%s
%s""" % (t, p.employee_table_row(d,shift_columns))

p.setdate(shift_date)
p.filename="""shift%s.html""" % (p.datestring())
p.path = """/Users/halc/source/SkiSchedule/root/"""
p.PageTitle = p.wraprow(p.wrapcell("""<h1>%s %s</h1>""" % (p.dateDOW(), p.dateHeaderString()),'Title',shift_columns))
t = """%s%s%s""" % (p.PageTitle,chr(13), t)
t = p.wraptable(t)
p.setbody(t)
p.wrapAsHtml()
p.write_html()
#print(p.page)