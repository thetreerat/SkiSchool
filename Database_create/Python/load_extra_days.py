import psycopg2
import sys
import csv

print('loading Languages ...')
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
    if d[0]!='title':
        if d[3]=='':
           d[3]=None
        if d[4]=='':
           d[4]=None
        print("""Title: %s, Date: %s, Points: %s, Idea Max: %s, ct: %s""" % (d[0],d[1],d[2], d[3],d[4]))
        cur.callproc('add_extra_days',[d[0],d[1],d[2],d[3],d[4]])
        result = cur.fetchall()
        for r in result:
            if r[0]==None:
                print """error on %s = %s """ % (d[0], d[1])
            #print(r)    
            else:
                count+=1
print """added %s entries""" % (count)
c.commit()
cur.close()
c.close()
