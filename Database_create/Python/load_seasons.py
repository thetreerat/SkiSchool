import psycopg2
import sys
import csv

print(' ')
print('loading Seasons ...')
filename=sys.argv[1]

with open(filename) as csvfile:
    data = list(csv.reader(csvfile))
c = psycopg2.connect(user="postgres",
                     port="5432",
                     host="127.0.0.1",
                     database="skischool")
cur = c.cursor()
count = 0
line = 1
for d in data:
    if d[0]!='ss_date':
        if d[0]=='':
            d[0] = None	
        if d[1]=='':
            d[1] = None	
        cur.callproc('add_season',[d[2],d[0],d[1],])
        result = cur.fetchall()
        #for r in result:
            #if r[0][-6:]!='added!':
        #    print """%s season""" % (r)
            #else:
        count+=1
    line+=1
print """added %s Seasons """ % (count)
c.commit()
cur.close()
c.close()
