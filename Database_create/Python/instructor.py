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
from menu import Menu
from extradays import ExtraDays

            
class instructor(person):
    """Class for instructor object based on person class object"""
    def __init__(self, eid=None, firstname=None, lastname=None, db_handle=None):
        """Init a instructor object"""
        person.__init__(self, firstname=firstname, lastname=lastname, db_handle=db_handle)
        self.eid = eid
        
        self.cell_phone = phone(db_handle=self.db_handle)
        self.cell_publish = None
        self.phone2 = phone(db_handle=self.db_handle)
        self.phone_2_text = 'Home'
        self.phone_2 = None
        self.phone3 = phone(db_handle=self.db_handle)
        self.phone_3_text = 'Work'
        self.phone_3 = None
        self.email = None
        self.email_sms = None
        self.psia_id = None
        self.aasi_id = None
        self.payroll_id = None
        self.start_date_New = True
        self.start_date = date(date=None,
                               db_handle=self.db_handle,
                               default_date = '11/01/2019')
        
        self.start_date.question = 'Enter Start date (%s):' % (self.start_date.default_date)
        
        self.end_date = date(date=None,
                             db_handle=self.db_handle,
                             default_date = '03/24/2019')
        self.end_date.question = 'Enter End date (%s):' % (self.start_date.default_date_str)
        self.employee_returning = None
        self.return_title = None
        self.instructor_update = False
        self.jlist = None
        self.clist = None
        self.llist = None
        self.alist = None
        self._hours = 0
        self._hoursweek = 0
                
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
        L = Locations()
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
        m = Menu('Edit Instructor Menu', db_handle=self.db_handle)
        m.menu_display = self.print_menu
        m.add_item('Availabilitiy', 'Availability - manage instructors availability', self.alist.menu)
        m.add_item('Cert', 'CERT - Manage instructors certifications', self.clist.menu)
        m.add_item('Phone', 'Cell <number> <display text> - Set Instructor Cell number', self.cell_phone.set_phone)
        m.add_item('Phone2', 'Phone <number> <display text> - Set Instructor Cell number', self.phone2.set_phone)
        m.add_item('Phone3', 'Phone <number> - Set Instructor Cell number', self.phone3.set_phone)
        m.add_item('End', 'END <date> - set employee last day of season', m.print_new)
        m.add_item('Start', 'START <date> - set employe start of season', m.print_new)
        m.add_item('Jacket', 'JACKET - manage jackets for employee', m.print_new)
        m.add_item('Location', 'LOCATION - manage Locker for emlployee', m.print_new)
        m.add_item('Last', 'LAST <Lastname> - Change Last Name ', self.get_lastname)
        m.add_item('First', 'FIRST <Firstname> - Change First Name ', self.get_firstname)
        m.add_item('Nick', 'NICK <Nickname> - Change Nick Name ', m.print_new)
        m.Menu()

    def instructor_name(self):
        """return instructor name first name<sp> last name as string"""
        return """%s %s""" % (self.firstname, self.lastname)
 
    def get_cell_db(self):
        """get employee cell from database"""
        result = self.db_handle.fetchdata('get_employee_cell', [self.eid, ])
        self.cell_phone.set_phone(result[0][0])
        return True
    
    def get_emp_db(self):
        results = self.db_handle.fetchdata('get_employee', [self.eid])
        for r in results:
            self.set_lastname(r[2])
            self.set_firstname(r[1])
            self.set_suffix(r[3])
            self.set_nickname(r[4])
            self.DOB.set_date(r[5])
            self.cell_phone.set_phone(r[6])
            self.cell_publish = r[7]
            self.cell_phone.set_publish(r[7])
            self.phone2._display = r[8]
            self.phone2.set_phone(r[9])
            self.phone_2_text = r[8]
            self.phone_2 = r[9]
            self.phone3.set_phone(r[11])
            self.phone3._display = r[10]
            self.phone_3_text = r[10]
            self.phone_3 = r[11]
            self.email = r[12]
            self.email_sms = r[13]
            self.psia_id = r[14]
            self.aasi_id = r[16]
            self.payroll_id = r[14]
            self.sex = r[17]
            #self.jlist = None
            #self.clist = None
            #self.llist = None
            #self.alist = None
            self.get_season_dates_db()
            self.get_hours_season()
            self.get_hours_week()
            
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
    
    def get_hours_season(self):
        if self.eid:
            r = self.db_handle.fetchdata('get_employee_hours_season', [self.eid])
            self._hours = r[0][0]
            
    def get_hours_week(self):
        if self.eid:
            r = self.db_handle.fetchdata('get_employee_hours_week', [self.eid])
            self._hoursweek = r[0][0]
    
    def hours(self, pad=6):
        return str(self._hours).ljust(pad)
    
    def hoursweek(self, pad=6):
        return str(self._hoursweek).ljust(pad)
    
    def print_instructor(self, form='short'):
        """Print instructor object"""
        if form=='short':
            print """%s - %s""" % (str(self.eid).ljust(4), self.name(nickname=True))
        elif form=='Long':
            phone2 = self.phone2.display
            print("""
    Name:               %s Emp ID:               %s
    Cell Phone:         %s Publish:
    %s %s Publish:
    Current Start Date: %s Current End Date:   %s
    Hours Worked:       %s Hours work week:    %s""" % (
                                 self.name().ljust(20),
                                 str(self.eid).ljust(20),
                                 self.cell_phone.number(False, 20),
                                 self.phone2.display(pad=19),
                                 self.phone2.number(False, 20),
                                 self.start_date.date(True).ljust(20),
                                 self.end_date.date(True),
                                 self.hours(20),
                                 self.hoursweek(20)
                                ))
            if self.jlist!=None:
                self.jlist.print_list('Short')
            if self.clist!=None:
                self.clist.print_certs()
            if self.llist!=None:
                self.llist.print_list()
            if self.alist!=None:
                self.alist.print_list()
    
    def print_menu(self):
        """function to print menu """
        os.system('clear')
        self.print_instructor(form='Long')
        #print("""    AVAILABILITY, CELL, CERT, END, START, JACKET, LOCATION, HELP,  MAIN, EXIT """)
        
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
        
    def add(self, options):
        """creates and instructor object, and updates instructor name from options passed """
        i = instructor(db_handle=self.db_handle)
        i.set_name(options[2])
        result = self.db_handle.fetchdata('add_employee', [i.firstname(), i.lastname(), ])
        result = self.db_handle.fetchdata('get_eid', [i.firstname(), i.lastname(), ])
        i.eid = result[0][0]
        self.append(i)
        return i
        
    def add_candidate(self, options=None):
        i = self.add(options)
        disapline = raw_input('Enter Disapline (ski, snowboard, tele): ')
        if disapline=='ski':
            disapline = 'Ski Instructor'
        elif disapline=='snowboard':
            disapline = 'SB Instructor'
        else:
            disapline = 'Tele Instructor'        
        result = self.db_handle.fetchdata('add_candidate', [i.eid, disapline,])
        
    def append(self, i, sort=True):
        """Add instructor object to instructors list, and resort list """
        if self.checkName(i.instructor_name)==None:
            self.ilist.append(i)
            self.sort()
                    
    def add_instructor_db(self, dump=None):
        """write list of new instructors to db"""
        for i in self.ilist:
            result = self.db_handle.fetchdata('add_employee', [i.firstname(), i.lastname(), ])
            raw_input(result)
            result = self.db_handle.fetchdata('get_eid', [i.firstname(), i.lastname(), ])
            i.eid = result[0][0]
        return True

    def clear(self, dump=None):        
        self.ilist = []
        
    def edit(self, answer):
        #print('In edit')
        if len(answer)>1:
            #print("""Edit Instructor %s """ % (answer[1]))
            eid = answer[1]
        else:
            eid(raw_input('enter ID: '))
        i = self.checkID(int(eid))
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
                i.llist = Locations(db_handle=self.db_handle, eid=i.eid)
                #raw_input(i.llist.eid.eid)
                i.llist.get_locations_employee_db()
            if i.alist==None and i.eid!=None:
                i.alist = availablities(eid=i.eid,
                                        db_handle=self.db_handle)
                i.alist.get_employee_availablity()
                
                
            i.edit_instructor()
    
    def extradaystemplate(self, options):
        E = ExtraDays(db_handle=self.db_handle)
        
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
        if eid=='':
            return None
        index = 0
        for i in self.ilist:
            #print("""%s - %s""" % (index, i.eid))
            if int(i.eid)==int(eid):
                break
            index+=1
        if index==len(self.ilist):
            return None
        else:
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
            i = instructor(db_handle=self.db_handle)
            i.eid = r[0]
            i.firstname = r[1]
            i.lastname = r[2]
            i._suffix = r[3]
            i._nickname = r[4]
            i.DOB = r[5]
            i.sex = r[6]
            self.append(i)
            
    def get_current_instructors(self, options=None):
        """ """
        self.clear()
        result = self.db_handle.fetchdata('list_current_employees', [])
        for r in result:
            e = instructor(eid=r[0], db_handle=self.db_handle)
            e.get_emp_db()
            self.append(e)
        
    def list_instructors(self):
        """Print list of instructors"""
        if len(self)>0:
            for i in self.ilist:
                i.print_instructor('short')
            print("""    ------------------
    count: %s """ % (len(self)))
        else:
            print("""No instructors in list!!""")
    
    def menu(self, options=None):
        self.get_current_instructors()
        M=Menu('Instructor Menu', db_handle=self.db_handle)
        M.menu_display = self.list_instructors
        M.add_item('rehire', 'REHIRE <firstname> <lastname> - mark an exising employee for hire', self.rehire_employee)
        M.add_item('New', 'NEW - Create a new instructor record', self.add)
        M.add_item('Candidate', 'Candidate - create new record for new hire instructors', self.add_candidate)
        M.add_item('FIND', 'FIND <firstname> <lastname> - find all instructor records matching name', self.find_name)
        M.add_item('Edit', 'EDIT <#> - Edit instructor matching EID number entered', self.edit)
        M.add_item('Clear', 'Clear - clears the list of instructors', self.clear)
        M.add_item('Current', 'CURRENT - list current instructors', self.get_current_instructors)
        M.add_item('Extra', 'EXTRA - manage extra days', M.print_new)
        M.Menu()
        
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
    
    def sort(self):
        first_sort = sorted(self.ilist, key=self.sort_first_key)
        self.ilist = sorted(first_sort, key=self.sort_last_key)
    
    def sort_last_key(self, person):
        return person.lastname()
    
    def sort_first_key(self, person):        
        return person.firstname()

    def sort_person_key(self, person):
        return person.name()
    
    def rehire_employee(self, options=None):
        if options[1] == False and len(options[2]) >= 1:
            if len(options[2])==3:
                 rehire_date = options[2][2]
            else:
                results = self.db_handle.fetchdata('get_employee_default_start', [])
                rehire_date = results[0][0]
            results = self.db_handle.fetchdata('add_employee_start', [options[2][0], options[2][1], rehire_date])
        elif options[1]!=  False:
            if len(options[2])==0:
                results = self.db_handle.fetchdata('get_employee_default_start', [])
                rehire_date = results[0][0]
            
        #print """%s, %s, %s """ % (options[0], options[1],options[2])
        #print(options)

        
            #pass
        #print(rehire_date)
        #print(results) 
from location import Location
from locations import Locations

    
if __name__ == '__main__':
    sid = 233
    db_handle = database(owner='Instructors.py - __main__')
    I = instructor(eid=110, db_handle=db_handle)
    I.get_emp_db()
    list = instructors(db_handle=db_handle)
    list.append(I)
    
    options = ['EDIT', 110, [], db_handle]
    list.edit(options)
    I.print_menu()
    #I.edit_instructor()
    #
    #I.get_current_instructors()
    #I.get_available_instructors(sid=sid)
    #I.list_instructors()
    #M=Menu('Instructor Menu', db_handle=db_handle)
    #M.menu_display = I.list_instructors
    #M.add_item('rehire', 'HIRE <firstname> <lastname> - mark an exising employee for hire', I.rehire_employee)
    #M.add_item('New', 'NEW - Create a new instructor record', I.add)
    #M.add_item('Canidate', 'Canidate - create new record for new hire instructors', I.add_candidate)
    #M.add_item('FIND', 'FIND <firstname> <lastname> - find all instructor records matching name', I.find_name)
    #M.add_item('Edit', 'EDIT <#> - Edit instructor matching EID number entered', I.edit)
    #M.add_item('Clear', 'Clear - clears the list of instructors', I.clear)
    #M.add_item('Current', 'CURRENT - list current instructors', I.get_current_instructors)
    #M.Menu()
    
