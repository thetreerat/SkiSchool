# Author: Harold Clark
# Copyright Harold Clark 2019
#
import sys
import os
import psycopg2
from database import database
from cert import cert
from cert import certs
from jacket import jacket
from jacket import jackets
from datetime import datetime
from availability import availability
from availability import availablities


class person(object):
    """Class for Person Objects"""
    def __init__(self, firstname=None, lastname=None, suffix=None):
        self.firstname = firstname
        self.lastname = lastname
        self.suffix = suffix
        self.nickname = None
        self.DOB = None
        self.sex = None
        self._Age = None

    def name(self):      
        """return instructor name first name<sp> last name as string"""
        name = ''
        if self.firstname:
            name = self.firstname
        if self.lastname:
            if len(name)>0:
                name = '%s %s' % (name, self.lastname)
            else:
                name = self.lastname
        if self.suffix:
                name = '%s %s' % (name,self.suffix)
        return name
    
    def print_person(self):
        if self.suffix:
            print("""%s %s %s""" % (self.firstname, self.lastname, self.suffix))
        else:
            print("""%s %s""" % (self.firstname, self.lastname)) 
    

    def set_name(self, I=None):
        """Collect name and set"""
        if not I:
            #try:
                I = list(raw_input('Name: ').split())
                
            #except:
            #    return 
        icount = len(I)
        if icount==2:
            self.firstname = I[0]
            self.lastname = I[1]
        elif icount==3:
            self.firstname = I[0]
            self.lastname = I[1]
            self.suffix = I[2]
        else:
            self.firstname = I[0]
            self.lastname = raw_input('Last Name: ')
            self.suffix = raw_input('Suffix (Jr,Sr,III,..):')
        
class instructor(person):
    """Class for instructor object based on person class object"""
    def __init__(self, eid=None, firstname=None, lastname=None):
        """Init a instructor object"""
        person.__init__(self, firstname=firstname, lastname=lastname)
        self.eid = eid
        self.cell_phone = None
        self.cell_publish = None
        self.phone_2_text = 'Home'
        self.phone_2 = None
        self.phone_3_text = 'Work'
        self.phone_3 = None
        self.email = None
        self.email_sms = None
        self.psia_id = None
        self.aasi_id = None
        self.payroll_id = None
        self.start_date_New = True
        self.start_date = None
        self.end_date = None
        self.employee_returning = None
        self.return_title = None
        self.instructor_update = False
        self.jlist = None
        self.clist = None
        self.llist = None
        self.alist = None

    def add_cert(self, answer):
        os.system('clear')
        if len(answer)==1:
            org = raw_input('Enter Certification Organization search string: ')
            title = raw_input('Enter Title search string: ')
        cert_title_list = certs()
        cert_title_list.find_certs_db(organization=org, title=title)
        cert_title_list.print_certs('find')
        line = raw_input('Select line number: ')
        if line!='':
            cert_to_add = cert_title_list.clist[int(line)]
            cur_date = datetime.now().date()
            cert_date = (raw_input("""Enter Date (%s): """ % (cur_date)))
            if cert_date=='':
                cert_to_add.cert_date = cur_date
            else:
                cert_to_add.cert_date = datetime.strptime(cert_date, '%m/%d/%y')
            cert_current = raw_input('Current (Yes/No): ').upper()
            if cert_current in ['YES', '']:
                cert_to_add.cert_current = 1
            else:
                cert_to_add.cert_current = 0
            if line!='':
                if self.clist==None:
                    self.clist = certs()
                cert_to_add.assign_cert(self.eid)
                self.clist.clist.append(cert_to_add)
            
    def add_employee_end_date_db(self):
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('add_employee_end', [self.eid, self.end_date,])
        ski_db.close()        
    
    def add_employee_start_db(self):
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('add_employee_start', [self.eid, self.start_date,])
        ski_db.close()
    
    def assign_jacket(self, answer):
        """assign jacket to instructor"""
        J = jackets()
        answer_count = len(answer)
        if answer_count in [2,3, 4]:
            size = answer[1]
        else:    
            size = raw_input('select size (XXS,XS,S,M,L,XL,XXL): ').upper()
        if answer_count==4:
            J.get_jacket(jacket_size=size, jacket_number=answer[2], jacket_type=answer[3])
        else:
            J.get_jackets_for_size(size)
        os.system('clear')
        J.print_list('Short')
        jid = raw_input('Select Jacket ID to Checkout: ')
        if jid!='':
            jacket = J.checkID(jid)
            if jacket!=None:
                jacket.print_jacket('Long')
                answer = raw_input('checkout? <enter>')
                if answer=='':
                    jacket.check_out_db(eid=self.eid)
    
    def assign_location_db(self):
        """assign location to an Instructor """
        L = locations()
        size = raw_input('Enter Locker size(ALL,Standard,Big, Full Size): ')
        L.get_locations_free(size=size)
        L.print_list(call_from='short')
        line = raw_input('Enter Location line: ')
        if line!='':
            line = int(line)
        #print("""line value: |%s|""" % line)
        if line not in ['']:
            L.llist[line].assign_location_db(self.eid)
        
    def cell_display(self):
        """convert phone number to display value and return"""
        if self.cell_phone!=None:
            l = len(self.cell_phone)
            if l==7:
                phone = """%s-%s""" % (self.cell_phone[0:3], self.cell_phone[3:7])
            elif l==10:
                phone = """%s-%s-%s""" % (self.cell_phone[0:3], self.cell_phone[3:6], self.cell_phone[-4:])
            else:
                phone = self.cell_phone
                
            return phone
        else:
            return ''

    def edit_instructor(self):
        run = True
        while run:
            self.print_menu()
            answer = raw_input('Please eneter selection: ').upper()
            answer = list(answer.split())
            while answer:
                if answer[0] in ['MAIN','MAI','MA','M']:
                    self.jlist = None
                    run = False
                    break
                elif answer[0] in ['AVAILABILITY','AVAILABILIT','AVAILABILI',
                                   'AVAILABIL', 'AVAILABI','AVAILAB',
                                   'AVAILA','AVAIL','AVAI','AVA',
                                   'AV','A']:
                    self.alist.menu()
                    break
                elif answer[0] in ['CERT','CER','CE']:
                    if len(answer)>2:
                        if answer[1].upper() in ['ADD', 'AD', 'A']:
                            self.alist.list_type='EditEmp'
                            self.clist.add()
                        elif answer[1].upper() in ['EDIT', 'EDI', 'ED', 'E']:
                            c = self.alist.checkID(int(answer[2]))
                            if c!=None:
                                c.edit()
                    self.alist.menu()
                    self.add_cert(answer)
                    break

                elif answer[0] in ['CELL','CEL','CE']:
                    self.set_cell()
                    break

                elif answer[0] == 'C':
                    answer = raw_input('CEll or CERT').upper()
                    answer = list(answer.split())
                    
                elif answer[0] in ['HELP', 'HEL', 'HE','H', '?']:
                    self.print_help()
                    answer = raw_input('Enter Selectioin: ').upper()
                    answer = list(answer.split())
                    break
                
                elif answer[0] in ['JACKET','JACKE','JACK','JAC','JA','J' ]:
                    self.assign_jacket(answer)
                    if self.jlist==None:
                        self.jlist = jackets()
                        self.jlist.get_employee_jackets_db(self.eid)
                    else:
                        self.jlist.clear()
                        self.jlist.get_employee_jackets_db(self.eid)
                    break
                
                elif answer[0] in ['LOCATION','LOCATIO','LOCATI','LOCAT','LOCA','LOC','LO','L']:
                    self.assign_location_db()
                    if self.llist==None:
                        self.llist = locations()
                        self.llist.get_locations_employee_db(self.eid)
                    else:
                        self.llist.clear()
                        self.llist.get_locations_employee_db(self.eid)
                    break
                    
                elif answer[0] in ['NAME','NAM','NA','N']:
                    self.set_name()
                    break
                elif answer[0] in ['START','S','ST','STA','STAR']:
                    self.set_start_date()
                    break
                elif answer[0] in ['END','EN']:
                    self.set_end_date()
                    break                
                elif answer[0] in ['UPDATE','UPDAT','UPDA','UPD','UP','U' ]:
                    self.update_instructor()
                    break
                elif answer[0] in ['EXIT', 'EXI','EX','E']:
                    sys.exit(1)
                else:
                    print("""Lost in space!!!""")
                    print(answer)
                    dump = raw_input('ready?')
                    break        

    def get_cell_db(self):
        """get employee cell from database"""
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('get_employee_cell', [self.eid, ])
        result = ski_db.cur.fetchall()
        self.cell_phone = result[0][0]
        #dump = raw_input('ready? ')
        ski_db.close()
        return True
        
    def get_cert_db(self):
        pass
    
    def get_season_dates_db(self):
        """get current season dates and return status from database"""
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('get_employee_season_dates', [self.eid,])
        result = ski_db.cur.fetchall()
        if len(result)>0:
            if result[0][0]==self.eid:
                d,self.start_date,self.end_date,self.employee_returning, self.return_title = result[0]
                self.start_date_New = False
        ski_db.close()
        
    def print_instructor(self, form='short'):
        """Print instructor object"""
        if form=='short':
            print """%s - %s %s""" % (self.eid, self.firstname, self.lastname)
        elif form=='Long':
            print("""    Emp ID:             %s
    Name:               %s
    Cell Phone:         %s
    Cell Phone Publish: 
    Current Start Date: %s
    Current End Date:   %s""" % (self.eid,
                                 self.name(),
                                 self.cell_display(),
                                 self.start_date,
                                 self.end_date
                                ))
            if self.jlist!=None:
                self.jlist.print_list('Short')
            if self.clist!=None:
                self.clist.print_certs()
            if self.llist!=None:
                self.llist.print_list('Employee')
            if self.alist!=None:
                self.alist.print_list()
    
    def print_menu(self):
        """function to print menu """
        os.system('clear')
        self.print_instructor(form='Long')
        print("""    AVAILABILITY, CELL, CERT, END, START, JACKET, LOCATION, HELP,  MAIN, EXIT """)
        
    def print_help(self):
        print("""    ------------------------------------------------
    NAME     - Change Name (First Last suffix)
    CELL     - Change Cell phone number
    ADD      - ADD Cert
    START    - Season Start Date for Employee
    END      - Season End Date For Employee
    JACKET   - Assign Jacket 
    LOCATION - Assign Location
    MAIN     - return to Main menu
    EXIT     - exit to system prompt
    ------------------------------------------------""")
        
    def set_cell(self):
        """collect and set cell in instructor object """
        self.cell_phone = raw_input("""Cell Phone (%s): """ % (self.cell_phone))
            
    def instructor_name(self):
        """return instructor name first name<sp> last name as string"""
        return """%s %s""" % (self.firstname, self.lastname)
    
    def set_end_date(self):
    
        if self.end_date==None:
            ed = '03/24/19'
        else:
            ed = self.end_date
        self.end_date = raw_input("""Enter End Date (%s): """ % (ed))
        if self.end_date=='':
            self.end_date= ed
        self.add_employee_end_date_db()
    
    def set_start_date(self, sd='11/01/19'):
        """ """
        self.start_date = raw_input("""Enter Start date (%s): """% (sd))
        if self.start_date == '':
            self.start_date = sd
        self.add_employee_start_db()
                  
    def update_instructor_db(self):
        """update instructor in database """
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('update_employee', [self.eid,])
        result = ski_db.cur.fetchall()
        if len(result)>0:
            if result[0][0]==self.eid:
                d,self.start_date,self.end_date,self.employee_returning, self.return_title = result[0]
        ski_db.close()    
    
    
    
class instructors(object):
    def __init__(self, db_handle=None):
        """init a set of instructors"""
        self.ilist = []
        self.db = db_handle
    
    def sort_person_key(self, person):
        return person.name
    
    def add(self, options):
        i = instructor()
        i.set_name(options[2])
        self.add_instructor(i)
        self.ilist.sort(key=self.sort_person_key)
        
    def add_instructor(self, i, sort=True):
        """Add instructor to instructors list """
        if self.checkName(i.instructor_name)==None:
            self.ilist.append(i)
            self.ilist.sort(key=self.sort_person_key)
            
    def add_instructor_db(self, dump=None):
        """write list of new instructors to db"""
        c = psycopg2.connect(user="postgres",
                             port="5432",
                             host="127.0.0.1",
                             database="skischool")
        cur = c.cursor()
        for i in self.ilist:
            cur.callproc('add_employee', [i.firstname, i.lastname, ])
            result = cur.fetchall()
            #print(result)
            cur.callproc('get_eid', [i.firstname, i.lastname, ])
            result = cur.fetchall()
            i.eid = result[0][0]
            #print(i.eid)
        #self.print_shift()
        c.commit()
        cur.close()
        c.close()
        return True

    def clear(self, dump=None):        
        self.ilist = []
        
    def edit(self, answer):
        if len(answer)>1:
            print("""Edit Instructor %s """ % (answer[1]))
            eid = answer[1]
        else:
            eid(raw_input('enter ID: '))
        i = self.checkID(int(eid))
        print('here')
        if i!=None:
            if i.cell_phone==None:
                i.get_cell_db()
            if i.start_date==None:
                i.get_season_dates_db()
            if i.jlist==None:
                i.jlist = jackets()
                i.jlist.get_employee_jackets_db(i.eid)
            if i.clist==None and i.eid!=None:
                i.clist= certs(eid=i.eid, list_type='Employee')
                i.clist.get_employee_certs_db()
            if i.llist==None and i.eid!=None:
                i.llist = locations()
                i.llist.get_locations_employee_db(i.eid)
            if i.alist==None and i.eid!=None:
                i.alist = availablities(eid=i.eid)
                i.alist.get_employee_availablity()
                
                
            i.edit_instructor()
        
              
    def checkID(self, eid):
        for i in self.ilist:
            if i.eid==eid:
                return i
        return None
    
    def checkName(self, Name):
        for i in self.ilist:
            if i.instructor_name()==Name:
                return i
        return None
    
    def find_name(self, options=None):
        os.system('clear')
        p = person()
        if options==None : options = [None, None, []]
        if not options[2]:
            print("""
    Find employees ....
    
        wildcards
            %K    - find any name that ends in K
            Cl%   - find any name that starts with Cl
            %la%  - find any name that contains la
            _lark - find any name that has one letter that end in lark
            __ar% - find any name that ingoring frist to letter that has ar and any ending.
            """)
        
            p.set_name()
            p.print_person()
        else:
            try:
                p.firstname = options[2][0]
                p.lastname = options[2][1]
                p.suffix = options[2][2]
            except:
                pass
        self.find_name_db(p.firstname, p.lastname)
        
    def find_name_db(self, firstname, lastname):
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('get_employee', [firstname, lastname])
        result = ski_db.cur.fetchall()
        for r in result:
            if self.checkID(r[0])==None:
                i = instructor(eid=r[0], firstname=r[1], lastname=r[2])
                i.suffix = r[3]
                i.nickname = r[4]
                i.DOB = r[5]
                i.cell_phone = r[6]
                i.cell_publish = r[7]
                i.phone_2_text = r[8]
                i.phone_2 = r[9]
                i.phone_3_text = r[10]
                i.phone_3 = r[11]
                i.email = r[12]
                i.email_sms = r[13]
                i.payroll_id = r[14]
                i.psia_id = r[15]
                i.aasi_id = r[16]
                self.ilist.append(i)
        ski_db.close()
        
    def get_name(self, eid, return_type='INDEX'):
        """return index or name from eid"""
        index = 0
        for i in self.ilist:
            #print("""%s - %s""" % (index, i.eid))
            if int(i.eid)==int(eid):
                break
            index+=1
        rt=return_type.upper()
        if rt=='INDEX':
            return index
        elif rt=='NAME':
            return self.ilist[index].instructor_name()
        elif rt=='OBJECT':
            return self.ilist[index]

    def get_available_instructors(self, sid, Clear=True):
        print('get_available_instructors sid:%s' % (sid))
        if Clear:
            self.clear()
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('list_availble', [sid,])
        #results = ski_db.call_ski_proc('list_availble', [int(sid)])
        result = ski_db.cur.fetchall()
        for r in result:
            i = instructor()
            i.eid = r[0]
            i.firstname = r[1]
            i.lastname = r[2]
            self.add_instructor(i)
        ski_db.close()                


        
    def list_instructors(self):
        """Print list of instructors"""
        if len(self.ilist)>0:
            for i in self.ilist:
                i.print_instructor('short')
        else:
            print("""No instructors in list!!""")


    def print_menu(self):
        os.system('Clear')
        self.list_instructors()
        print("""    ----------------------------------------------------
     ADD       - Add New Instructor
     FIND      - find an instructor
     EDIT #    - Edit a Instructor
     LOAD      - Load Entered Data into Table
     CLEAR     - Clear list of intructors
     EXIT      - Quit or Exit program """)
 
        
from location import location
from location import locations

    
if __name__ == '__main__':
    sid = 233

    I = instructors()
    I.get_available_instructors(sid=sid)
    I.list_instructors()
    #ski_db = database()
    #ski_db.connect()
   # I.db = ski_db
   # while True:
   #     I.print_menu()
   #     answer = raw_input('Please enter a selection: ').upper()
    #    answer = list(answer.split())
     #   while answer:
      #      if answer[0] in ['EXIT', 'EXI', 'EX', 'QUIT', 'QUI', 'QU', 'Q']:
       #         sys.exit(1)
        #    elif answer[0] in ['ADD', 'AD', 'A']:
         #       #dump = raw_input('ready?')
          #      i = instructor()
           #     i.set_name()
            #    I.add_instructor(i)
             
             #   break
            #elif answer[0] in ['CLEAR','CLEA','CLE','CL', 'C']:
             #   print("""Clearing emloyee!""")
              #  dump = raw_input('ready?')
               # I.ilist = []
                #break
#            elif answer[0]=='E':
 #               answer = raw_input('EXIT or EDIT #: ').upper()
  #              answer = list(answer.split())
   #         elif answer[0] in ['EDIT','EDI','ED']:
    #            I.edit(answer)
     #           break
      #      elif answer[0] in ['FIND','FIN','FI','F']:
       #         I.find_name(answer)
        #        break
#
#            elif answer[0] in ['LOAD']:
#                print("""Load Instructors to DB""" % ())
#                I.add_instructor_db()
#                break
#            else:
#                print("""Lost in space!!!""")
#                dump = raw_input('ready?')
 #               break