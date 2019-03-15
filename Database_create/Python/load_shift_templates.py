import psycopg2
import sys
import csv

print('loading shift templates ...')
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
    
    if d[0]!='Shift_Name':
        cur.callproc('add_shift_template',[d[0],d[1],d[2],d[3],d[4],d[5],])
        result = cur.fetchall()
        for r in result:
            #print(r[0])
            if r[0]==None:
                print("error on line " + str(count) + " "+ d[0] + ", " + d[4])
            else:
                count+=1
print """added %s entries""" % (count)
c.commit()
cur.close()
c.close()