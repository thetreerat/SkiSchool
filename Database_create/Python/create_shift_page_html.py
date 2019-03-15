import psycopg2
import sys
import csv
from time import strptime
from datetime import timedelta
from html_page import html
from shift import person
from shift import persons
from shift import shift

    
    
print('createing html shift page ...')
shift_date=sys.argv[1]
#password=sys.argv[2]
p = html()

c = psycopg2.connect(user="postgres",
                     port="5432",
                     host="127.0.0.1",
                     database="skischool")
cur = c.cursor()
cur.callproc('list_shift', [shift_date,])
result = cur.fetchall()
count = 0
#data = {}
data = persons()
for r in result:
    count+=1
    s = shift(r[2],r[3],r[4],r[5])
    i = data.check_name(r[0],r[1])
    if i==None:
        e = person(r[0],r[1])
        e.shifts.append(s)
        data.add_person(e)
    else:
        data.list[i].shifts.append(s)
    
print """Total rows: %s""" % (count)
t = p.shift_table_header()
for d in data.list:
    d.printperson()
    t = """%s
%s""" % (t, p.employee_table_row(d,30))


p.setdate(shift_date)
p.filename="""shift%s.html""" % (p.datestring())
p.path = """/Users/halc/source/SkiSchedule/root/"""
p.PageTitle = p.wraprow(p.wrapcell("""<h1>%s %s</h1>""" % (p.dateDOW(), p.dateHeaderString()),'Title',30))
t = """%s%s%s""" % (p.PageTitle,chr(13), t)
t = p.wraptable(t)
p.setbody(t)
p.wrapAsHtml()
p.write_html()
#print(p.page)