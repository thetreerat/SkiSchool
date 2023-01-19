import psycopg2
import sys
import csv

print('loading cert...')
filename=sys.argv[1]

with open(filename) as csvfile:
    data = list(csv.reader(csvfile))
c = psycopg2.connect(user="postgres",
                     port="5432",
                     host="127.0.0.1",
                     database="skischool")
cur = c.cursor()
count = 0
row = 0
for d in data:
    #print(d)
    #print("""Title: %s, Org: %s, html_class: %s""" %(d[0],d[1],d[2]))
    
    if d[0]!='title':
        cur.callproc('add_cert_template',[d[0],d[1],d[2]])
        result = cur.fetchall()
        for r in result:
            #print (r[0])
            if r[0]=="""%s with org %s in the database""" % (d[0],d[1]):
                print """count %s = title: %s, org: %s, %s  in database!""" % (row, d[0], d[1],d[2])
            #print(r)
            elif r[0]=="""%s with org %s updated html_class to %s""" % (d[0],d[1],d[2]):   
                print """row: %s html_class update on %s""" % (row, d[0])
            else:
                count+=1
    row+=1
print """added %s entries""" % (count)
c.commit()
cur.close()
c.close()
