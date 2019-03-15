import psycopg2
import sys
filename=sys.argv[1]
print('Loading employee availablity')
import csv

with open(filename) as csvfile:
    data = list(csv.reader(csvfile))
c = psycopg2.connect(user="postgres",
                     port="5432",
                     host="127.0.0.1",
                     database="skischool")
cur = c.cursor()
count = 0
for d in data:
    #print(d)  
    if d[0]!='lastname':
        cur.callproc('add_employee_aval',[d[1],d[0],d[2],d[3],d[4],])
        result = cur.fetchall()
        #print(result)
        for r in result:
            if r[0]==None:
                print """Error on employee %s %s""" % (d[1],d[0])
            else:
                count+=1
print """added %s entries""" % (count)
c.commit()
cur.close()
c.close()