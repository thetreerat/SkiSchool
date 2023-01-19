import psycopg2
import sys
import csv
import datetime
from phone import phone
from database import database
class Headers(object):
    def __init__(self):
       """ """
       self.Headers = []
       
    def print_headers(self):
        count = 0
        for h in self.Headers:
            print """%s : %s""" % (count,h)
            count+=1

    def load_headers(self, H):
        for h in H:
			self.Headers.append(h)

    def find_header(self, f):
        index = 0
        for h in self.Headers:
            if h==f:
                return index
            index+=1
        return index
        
def fix_name(name):
    if name not in ['']:
         if name[0] != name[0].upper():
              name = name[0].upper() + name[1:]
    return name

def splitstring(s):
    newlist = s.split(',')
    c=0
    for i in newlist:
        newlist[c] = newlist[c].strip()
        c+=1
    return newlist
    
def fix_DOB(DOB):

    if DOB=='':
        DOB = None
    else:
        if DOB not in ["Date of Birth"]: 
            DOB = datetime.datetime.strptime(d[12], "%m/%d/%Y").date()
    return DOB

def emp_type_DOB(DOB):
    ap_cutoff = datetime.datetime.strptime("01/05/2007", "%m/%d/%Y").date()
    jr_cutoff = datetime.datetime.strptime("01/05/2005", "%m/%d/%Y").date()
    if DOB == None:
        emp_type = "Adult"
    elif ap_cutoff >= DOB >= jr_cutoff :
        emp_type = "JR"
    elif DOB >= ap_cutoff :
        emp_type = "AP"
    
    else:
        emp_type = "Adult"
    return emp_type 

def cleancerts(h):
    l = h.splitlines()
    rl = []
    for i in l:
        nl = splitstring(i)
        for n in nl:
            rl.append(n)
    return rl
def fix_cert(row_data):
	
    cert_list = []
    org = row_data[15]
    certs = row_data[16].strip()
    cert_list = cleancerts(certs)

    i = 0
    for c in cert_list:
		#print(c)
        cert_list[i] = clean_cert(c, row_data[13].upper().strip())	
        i+=1
		#print(c)	    
    #print("""Name: %s, %s """ % (row_data[0], row_data[1]))
    #print("""Active Certifications info: %s""" % (certs))
    
    #print(len(certs))
    return cert_list

def clean_cert(cert, disapline):
    cert = cert.strip()
    if cert in ['Alpine Level III', 
                'Alpine Level 3',
                'PSIA Level 3',
                'level 3 Psia',
                'Level 3 Alpine',
                'Level 3 Alpine and Development Team',
                'PSIA Alpine Level III',
                'alpine level 3']:
        return 'PSIA Level 3'

    elif cert in ['Level 3', '3'] and disapline=='SKI':
        return 'PSIA Level 3'        

    elif cert in ['Alpine level II',
                  'Level 2 PSIA',
                  'Alpine Level 2']:
        return 'PSIA Level 2'
        
    elif cert in ['II Alpine',
                  'Alpine level 2',
                  'alpine level 2',
                  'Level 2 Alpine']:
        return 'PSIA Level 2'
    elif cert in ['2', 
                  'Level 2'] and disapline=='SKI':
        return 'PSIA Level 2'

    elif cert in ['Lev 1 Alpine',
                  'Alpine 1',
                  'Alpine level 1',
                  'PSIA Level 1',
                  'Alpine Level 1',
                  ]:
		return 'PSIA Level 1'
    elif cert in ['Level 1', 'Level1', '1','one', 'ONE'] and disapline=='SKI':
        return 'PSIA Level 1'    
    elif cert in ['Level 1', '1'] and disapline=='SNOWBOARD':
		return 'AASI Level 1'
    elif cert in ['Level 2', '2'] and disapline=='SNOWBOARD':
		return 'AASI Level 2'
    elif cert in ['Level 3', '3'] and disapline=='SNOWBOARD':
		return 'AASI Level 3'
    elif cert in ['Level 1 Snowboard',
                  'AASI level 1',
                  'AASI Level 1',
                  'Snowboard level 1']:
        return 'AASI Level 1'
    elif cert in ['Level 1 Childrens',
                  'Childrens Specialist 1',
                  'childrens specialist 1',
                  'CS 1','CS  1']:
        return 'Childern 1'
    elif cert in ['Level 2 Childrens', 'CS 2','level 2 CS',
                  "Children's Specialist 2"]:
        return 'Childern 2'
    elif cert in ['Level III Inverted Aerial']:
        return 'Level 3 Aerials'
    elif cert in ['Level II Mogul']:
        return 'Level 200 Moguls'
    elif cert in ['FS1', 'Freestyle Level 1']:
		return 'Freestyle level 1'
    elif cert in ['Level 3 Freestyle and Trainer', 'Level 3 Freestyle']:
        return 'Freestyle Level 3'
    elif cert in ['Adaptive Level I', 'Adaptive Level 1',
                  'Adaptive 1',
                  'Lev 1 Adaptive']:
        return 'Adaptive Level 1'
    elif cert in ['PSIA Telemark Level I']:
        return 'Telemark Level 1'
    else:
        return cert

def clean_avalability(row_data, dow):
    a_list = []
    for d in dow:
        if row_data[d]not in ['', None]:
            AS,AE = emp_choice(dow,row_data[d]) 
            AD = {'dow':d, 'Start':AS, 'End':AE, 'tdow':tdow(d)}
            a_list.append(AD)
            #print(AD)
    return a_list  
	  	     
def split_command(command):
    item_index = False
    options = []
    action = None
    command = list(command.split())
    if len(command)>0:
        action = command.pop(0).upper()
        while len(command)>0:
            c = command.pop(0)
            try:
                item_index = int(c)
            except:
                #print('c values is:%s, and type is: %s' % (c, type(c)))
                options.append(c)
    return (action, item_index, options)
    
def write_DOW_files(row_data, file_list, columns, Headers):
    for i in columns:
        if file_list[str(i)] == None:
            #print  ("""file: %s column: %s""" % (file_list[str(i)], Headers[i]))
            print(i)
            print(Headers)
            print(Headers[i])
            file_list[str(i)] = open(Headers[i] + ".csv", "w")
        row_data[i] = emp_choice(Headers[i], row_data[i].strip())
        if d[i] != '':
            file_list[str(i)].write("""%s,%s,%s,%s,,%s\n""" % (d[1], d[0], d[13],emp_type_code(d[20], d[19], d[21]),d[i])) 
    return file_list

def write_phone_list(row_data, phone_file, Headers, phone_db):
    if phone_file == None:
        phone_file = open("Phone_list.csv", "w")
    P = phone(number=d[10], publish=False, db_handle=phone_db)
    H = phone(number=d[9], publish=False, db_handle=phone_db)
    W = phone(number=d[11], publish=False, db_handle=phone_db)
    person = """%s,%s,%s,%s,%s,%s,%s""" % (row_data[0],
                                     row_data[1],
                                     row_data[20],
                                     row_data[13], 
                                     P.number(number_only=False), 
                                     H.number(number_only=False), 
                                     W.number(number_only=False))
    print(person)
    phone_file.write("""%s\n""" % (person))
    return phone_file, phone_db    
    
def emp_type_code(pvalue, race=None, ft=None):
    type_code = None
    if pvalue in ["Apprentice  Instructor"]:
        type_code = "AP"
    elif pvalue in ["Junior Instructor"]:
        type_code = "JR"
    else:
        if race in ["Racing,Freestyle", "Racing","Racing,Brigades"]:
            type_code = "RACE" 
        elif race in ["Freestyle"]:
            type_code = "Free"
        elif ft in ["I'm interested in full-time employment"]:
            type_code = "FT"
        elif race in ["Brigades","Brigades,Park Crew","Brigades,Park Crew,Freestyle",
                      "Brigades,Freestyle", "", "Racing,Brigades,Freestyle"]:
            type_code = ""
        else:
            print(race)
            print(ft)
            print(pvalue)            
            type_code = ""
    return type_code

def tdow(dow):
    if dow==22:
        tdow = "monday"
    elif dow==23:
        tdow = "tuesday"
    elif dow==24:
        tdow = "wednesday"
    elif dow==25:
        tdow = "thursday"
    elif dow==26:
        tdow = "friday"
    elif dow==27:
        tdow = "saturday"
    elif dow==28:
        tdow = "sunday"    
    else:
        tdow = None
    return tdow
def emp_choice(dow, choice):
    short = None
    

    
    if choice in [None, ""]:
        short = ""
    elif choice in ["4:30pm / 8 pts / First Choice", 
                    "4:30pm / 8 pts / First Choice,4:30pm / 8 pts / Second Choice",
                    "4:30pm / 8 pts / First Choice,5:30pm / 6 pts / Second Choice",
                    "4:30pm / 8 pts / First Choice,5:30pm / 6 pts / First Choice"]:
        return ("4:30 PM", "8:30 PM")
    elif choice in ["4:30pm / 8 pts / Second Choice",
                    "4:30pm / 8 pts / Second Choice,5:30pm / 6 pts / Second Choice"]:
        return ("4:30 PM", "8:30 PM")
    elif choice in ["5:30pm / 6 pts / First Choice",
                    "5:30pm / 6 pts / First Choice,5:30pm / 6 pts / Second Choice", 
                    "5:30pm / 6 pts / First Choice,4:30pm / 8 pts / Second Choice"]:
        return ("5:30 PM", "8:30 PM")
    elif choice in ["9am-5pm / 8 pts / First Choice",
                    "9am-5pm / 8 pts / First Choice,9am-5pm / 8 pts / Second Choice", 
                    "8:30am-5pm / 11pts / First Choice",
                    "8:30am-5pm / 11pts / First Choice,8:30am-5pm / 11pts / Second Choice"]:
        return ("9:00 am", "5:30 PM")
    elif choice in ["9am-5pm / 8 pts / First Choice,4:30pm / 8 pts / First Choice,5:30pm / 6 pts / First Choice,9am-5pm / 8 pts / Second Choice,4:30pm / 8 pts / Second Choice,5:30pm / 6 pts / Second Choice",
                    "9am-5pm / 8 pts / First Choice,4:30pm / 8 pts / First Choice"]:
		return ("9:00 am", "8:30 PM")
    elif choice in ["8:30am-5pm / 11pts / Second Choice","9am-5pm / 8 pts / Second Choice",
                    "9am-5pm / 8 pts / Second Choice"]:
        return ("8:30 AM", "5:30 PM")
    elif choice in ["4:30pm / 8 pts / First Choice,9am-5pm / 8 pts / Second Choice"]:
        return ("9:00 AM", "8:30 PM")
    elif choice in ["4:30pm / 8 pts / Second Choice"]:
        return ("4:30 PM", "8:30 PM")
    elif choice in ["5:30pm / 6 pts / Second Choice"]:
        return ("5:30 PM", "8:30 PM")
    elif choice in ["9am-7pm / 21pts / First Choice", "9am-5pm / 8 pts / First Choice,5:30pm / 6 pts / First Choice", 
                    "9am-7pm / 21pts / First Choice,4pm / 8pts / Second Choice",
                    "8:30am-5pm / 11pts / First Choice,9am-7pm / 21pts / First Choice",
                    "9am-7pm / 21pts / First Choice,9am-7pm / 21pts / Second Choice",
                    "8:30am-5pm / 11pts / First Choice,9am-7pm / 21pts / First Choice,4pm / 8pts / First Choice",
                    "9am-5pm / 8 pts / First Choice,4:30pm / 8 pts / Second Choice,5:30pm / 6 pts / Second Choice",
                    "8:30am-5pm / 11pts / First Choice,9am-7pm / 21pts / First Choice,9am-7pm / 21pts / Second Choice",
                    "8:30am-5pm / 11pts / First Choice,9am-7pm / 21pts / First Choice,4pm / 8pts / First Choice,8:30am-5pm / 11pts / Second Choice,9am-7pm / 21pts / Second Choice,4pm / 8pts / Second Choice"]:
        return ("8:30 AM", "8:30 PM")
    elif choice in ["9am-7pm / 21pts / Second Choice"]:
        return ("8:30 AM", "8:30 PM")
    elif choice in ["8:30am-5pm / 11pts / First Choice,9am-7pm / 21pts / Second Choice", 
                    "9am-5pm / 8 pts / First Choice,5:30pm / 6 pts / Second Choice",
                    "9am-7pm / 21pts / First Choice,8:30am-5pm / 11pts / Second Choice"]:
        return ("8:30 AM", "8:30 PM")
    elif choice in ["8:30am-5pm / 11pts / First Choice,4pm / 8pts / Second Choice",
                    "4pm / 8pts / First Choice,9am-7pm / 21pts / Second Choice",
                    "4pm / 8pts / First Choice,8:30am-5pm / 11pts / Second Choice"]:
		return ("8:30 AM", "8:30 PM")
    elif choice=="9am-5pm / 8 pts / First Choice,4:30pm / 8 pts / Second Choice":
        return ("8:30 AM", "8:30 PM")
    elif choice in ["4pm / 8pts / First Choice",
                    "4pm / 8pts / First Choice,4pm / 8pts / Second Choice"]:
		return ("4:00 PM", "8:30 PM")
    else:	
        print("""%s: %s""" % (dow, choice)) 
    return short
            
print('loading employee certs ...')
filename=sys.argv[1]
db_handle = database(owner='load_emp_web.py - phone')
with open(filename) as csvfile:
    data = list(csv.reader(csvfile))

c = psycopg2.connect(user="postgres",
                     port="5432",
                     host="127.0.0.1",
                     database="skischool")
cur = c.cursor()
count = 0
h = 0
H = Headers()
phone_file = None
phone_db = None
hire_date = psycopg2.Date(2022, 12, 11)
DOW = [22,23,24,25,26,27,28]
files = {}
for w in DOW:
    files[str(w)] = None
for d in data:
    #print(d)
    #print("'" + d[1]+ "','" + d[0]+ "','" + d[2] + "'")
    #if count==0:
    #print(d)
    if d[0]=='Last Name':
        H.load_headers(d)
        H.print_headers()
    else:
        d[0] = fix_name(d[0])
        d[1] = fix_name(d[1])
        dob = fix_DOB(d[12])
        #print("""Name: %s, %s Cell: %s Email: %s Displine: %s, Type: %s, %s""" % (d[0], 
        #                                                                          d[1], 
        #                                                                          d[10], 
        #                                                                          d[7], 
        #                                                                          d[13],
        #                                                                          d[20], 
        #                                                                          dob))
        P = phone(number=d[10], publish=False, db_handle=db_handle)
        cur.callproc('add_employee', [d[1],d[0],P._number,False,d[7],dob,hire_date])
        result = cur.fetchall()
        print(result)
        emp_type = emp_type_DOB(dob)       
        if emp_type in ['AP']:
            cur.callproc('add_employee_cert', [d[1], d[0], 3])         
            result = cur.fetchall()
            #print(result)
        clist = fix_cert(d) 
        if len(clist):
            for ec in clist:
                cur.callproc('add_employee_cert', [d[1], d[0], ec])
                result = cur.fetchall()
                print(result)
                #print(c)
        alist = clean_avalability(d, DOW,)
        if len(alist):
            for ac in alist:
				cur.callproc('add_employee_aval', [d[1],d[0], ac['tdow'], ac['Start'], ac['End']])
				result = cur.fetchall()
				#print(result)
				#print(ac)
	    if d[14] is not "":
			cur.callproc('add_employee_language', [d[1],d[0], d[14]])
			result = cur.fetchall()
			print(result)
        print("end of Record %s" % (count))
    count+=1
for g in DOW:
    try:
        files[str(g)].close()
    except Exception as err: 
        print(err)
try:
	phone_file.close()
#except NoneType:
#	print("no file to close")
except Exception as err:
	print(err)
	
print """add %s entries """ % (count)
print ("""Headers list: %s, count: %s """ % (len(H.Headers),h))
c.commit()
cur.close()
c.close()
