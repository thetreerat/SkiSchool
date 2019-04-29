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
from phone import phone
from person import person
from date import date

            
class instructor(person):
    """Class for instructor object based on person class object"""
    def __init__(self, eid=None, firstname=None, lastname=None, db_handle=None):
        """Init a instructor object"""
        person.__init__(self, firstname=firstname, lastname=lastname, db_handle=db_handle)
        self.eid = eid
        self.cell_phone = phone(db_handle=self.db_handle)
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
        self.start_date = date(None,
                               db_handle=self.db_handle,
                               default_date = '11/01/19')
        self.start_date.question = 'Enter Start date (%s):' % (self.start_date.default_date)
        self.end_date = date(None,
                             db_handle=self.db_handle,
                             default_date = '03/24/19')
        self.end_date.question = 'Enter End date (%s):' % (self.start_date.default_date)
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
                    self.cell_phone.set_phone()
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

    def instructor_name(self):
        """return instructor name first name<sp> last name as string"""
        return """%s %s""" % (self.firstname, self.lastname)
 
    def get_cell_db(self):
        """get employee cell from database"""
        result = self.db_handle.fetchdata('get_employee_cell', [self.eid, ])
        self.cell_phone.set_phone(result[0][0])
        return True
            
    def get_season_dates_db(self):
        """get current season dates and return status from database"""
        result = self.db_handle.fetchdata('get_employee_season_dates', [self.eid,])
        if len(result)>0:
            if result[0][0]==self.eid:
                self.start_date.set_date(result[0][1])
                self.end_date.set_date(result[0][2])
                self.employee_returning = result[0][3]
                self.return_title = result[0][4]
                self.start_date_New = False
        
    def print_instructor(self, form='short'):
        """Print instructor object"""
        if form=='short':
            print """%s - %s""" % (self.eid, self.name(nickname=True))
        elif form=='Long':
            print("""    Emp ID:             %s
    Name:               %s
    Cell Phone:         %s
    Cell Phone Publish: 
    Current Start Date: %s
    Current End Date:   %s""" % (self.eid,
                                 self.name(),
                                 self.cell_phone.number(),
                                 self.start_date.date(),
                                 self.end_date.date()
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
                        
    def set_end_date(self):
        if self.end_date.date()!=None:
            self.end_date._default = self.end_date._date
        self.end_date.get_date()
        self.db_handle.fetchdata('add_employee_end', [self.eid, self.end_date,])
    
    def set_start_date(self, sd='11/01/19'):
        """Set start date and update database"""
        self.start_date.get_date() 
        self.db_handle.fetchdata('add_employee_start', [self.eid, self.start_date.date(),])    
    
class instructors(object):
    def __init__(self, db_handle=None):
        """init a set of instructors"""
        self.ilist = []
        self.set_db_handle(db_handle)
    
    def __len__(self):
        return len(self.ilist)
    
    def __repr__(self):
        return "Instructors - %s, db=%s, pythonID: %s" % (len(self), self.db_handle.owner, id(self))

    def __str__(self):
        return "Instructors - %s, db=%s" % (len(self), self.db_handle.owner)
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
        for i in self.ilist:
            result = self.db_handle.fetchdata('add_employee', [i.firstname, i.lastname, ])
            result = self.db_handle.fetchdata('get_eid', [i.firstname, i.lastname, ])
            i.eid = result[0][0]
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
        #print('here')
        if i!=None:
            if i.cell_phone==None:
                i.get_cell_db()
            if i.start_date==None:
                i.get_season_dates_db()
            if i.jlist==None:
                i.jlist = jackets(db_handle=self.db_handle)
                i.jlist.get_employee_jackets_db(i.eid)
            if i.clist==None and i.eid!=None:
                i.clist= certs(eid=i.eid,
                               list_type='Employee',
                               db_handle=self.db_handle)
                i.clist.get_employee_certs_db()
            elif i.eid!=None:
                i.clist.clear()
                i.clist.get_employee_certs_db()
            if i.llist==None and i.eid!=None:
                i.llist = locations(db_handle=self.db_handle)
                i.llist.get_locations_employee_db(i.eid)
            if i.alist==None and i.eid!=None:
                i.alist = availablities(eid=i.eid,
                                        db_handle=self.db_handle)
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
        p = person(db_handle=self.db_handle)
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
            p.print_self()
        else:
            try:
                p.set_name(options)
            except:
                pass
        clearlist = raw_input('Clear list first Y/N (N)?').upper()
        try:
            if clearlist[0]=='Y':
                self.clear()
        except:
            pass
        self.find_name_db(p.firstname(), p.lastname())
                
    def find_name_db(self, firstname, lastname):
        result = self.db_handle.fetchdata('get_employee', [firstname, lastname, ])
        for r in result:
            if self.checkID(r[0])==None:
                i = instructor(eid=r[0], firstname=r[1], lastname=r[2], db_handle=self.db_handle)
                i._suffix = r[3]
                i._nickname = r[4]
                i.DOB.set_date(r[5])
                i.cell_phone.set_phone(r[6])
                i.cell_phone.set_publish(r[7])
                i.phone_2_text = r[8]
                i.phone_2 = r[9]
                i.phone_3_text = r[10]
                i.phone_3 = r[11]
                i.email = r[12]
                i.email_sms = r[13]
                i.payroll_id = r[14]
                i.psia_id = r[15]
                i.aasi_id = r[16]
                i.sex = r[17]
                self.ilist.append(i)
        
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
        result = self.db_handle.fetchdata('list_availble', [sid,])
        for r in result:
            i = instructor()
            i.eid = r[0]
            i.firstname = r[1]
            i.lastname = r[2]
            self.add_instructor(i)
        
    def list_instructors(self):
        """Print list of instructors"""
        if len(self.ilist)>0:
            for i in self.ilist:
                i.print_instructor('short')
        else:
            print("""No instructors in list!!""")
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='employee.py - init_employee')
        self.db_handle = db_handle
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