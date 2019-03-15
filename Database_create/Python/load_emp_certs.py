import psycopg2
import sys
import csv

print('loading employee certs ...')
filename=sys.argv[1]

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
    #print("'" + d[1]+ "','" + d[0]+ "','" + d[2] + "'")
    
    if d[0]!='lastname':
        cur.callproc('add_emp_cert_title',[d[1],d[0],d[2],])
        result = cur.fetchall()
        for r in result:
            if r[0]==None:
                print """Error at line %s on employee %s %s """ % (count,d[0], d[1])
            #print r
            else:
                count+=1
print """add %s entries """ % (count)
c.commit()
cur.close()
c.close()