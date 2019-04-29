# Author: Harold Clark
# Copyright Harold Clark 2019
#
from operator import attrgetter
from datetime import datetime
from instructor import instructor
from instructor import instructors
from instructor import person
#from instructor import person
from shift import shift
import sys
import os
import psycopg2
from menu import Menu
from database import database
from date import date


        
class private(shift):
    """class object for a private lesson, subclassed from shift"""
    def __init__(self,
                 shift_name=None,
                 start_time=None,
                 end_time=None,
                 html_class=None,
                 date=None,
                 sid=None,
                 ct=None,
                 ct_title=None,
                 db_handle=None):
        """Init a private lesson object"""
        shift.__init__(self, shift_name=shift_name,
                             start_time=start_time,
                             end_time=end_time,
                             html_class=html_class,
                             shift_date=date,
                             sid=sid,
                             ct=ct,
                             ct_title=ct_title,
                             db_handle=db_handle)
        self.student_firstname = ''
        self.student_lastname = ''
        self.contact_firstname = ''
        self.contact_lastname = ''
        self.contact_phone = ''
        self.contact_relation = ''
        self.student_age = None
        self.student_skill_level = ''
        self.lesson_length = None
        self.lesson_type = None
        self.discipline = None
        self.instructor_firstname = None
        self.instructor_lastname = None
        self.available_instructors = None
        self.update = False
        
    def add_private_db(self, options=None):
        """write private info to database """
        result = self.db_handle.fetchdata('add_private', [self.student_firstname,
                                                          self.student_lastname,
                                                          self.contact_firstname,
                                                          self.contact_lastname,
                                                          self.contact_phone,
                                                          self.lesson_type,
                                                          self.student_skill_level,
                                                          self.discipline,
                                                          self.eid,
                                                          self.sid, ])
        print(result)
        self.pid = result[0][0]
        return True
        
    def check_add_shift(self):
        """function for check if required fields are enter before writing to db"""
        message = 'Values not set:'
        if self.shift_date.date()==None:
            message = message + ' Date,'
        if self.start_time==None:
            message = message + ' Start Time,'
        if self.end_time==None:
            message = message + ' End Time,'
        if self.lesson_type==None:
            message = message + ' Lesson Type,'
        if self.discipline==None:
            message = message + ' Discipline,'
        if len(message)>17:
            message = message[:-1]
        else:
            message = None
        if self.shift_name==None and message==None:    
                self.set_shift_name()
        return message
    
    def find_instructor(self, options=None):
        """method for displaying instructor(s) by name, and selecting  for this private lesson."""
        if not self.available_instructors:
            self.available_instructors = instructors()
            self.available_instructors.find_name()
        os.system('clear')
        self.available_instructors.list_instructors()
        self.eid = raw_input('employee id: ')
        if self.lesson_type in [None, 'A']:
            demand = raw_input('Is this a demand lesson?(YES)')
            if demand in ['', 'YES', 'YE', 'Y']:
                self.lesson_type = 'D'
                if self.shift_name:
                    self.set_shift_name()
                    if self.sid:
                        print('Need to update database with new shift name, code not built.')
        else:
            print(self.lesson_type)
        instructor = self.available_instructors.get_name(eid=self.eid, return_type='Object')
        self.instructor_firstname = instructor.firstname
        self.instructor_lastname = instructor.lastname
        
    def PrivateMenu(self):
        """function for collecting and display private lesson while editing or creating"""
        print("""     Private screen
     --------------------------------
     Student Name:         %s %s
     Student Age:          %s
     Student Skill Level:  %s
     Contact Name:         %s %s
     Contact Relationship: %s
     Contact Phone:        %s
     Lesson Date:          %s
     Lesson Start:         %s
     Lesson End:           %s
     Lesson Length:        %s
     Instructor:           %s %s
     A/D:                  %s
     Ski/SB/Tele:          %s
     
     --------------------------------
     NAME      - Input Student Name
     CONTACT   - Input Contact Name
     PHONE     - Input Phone
     AGE       - Input Student Age
     DATE      - Input Lesson Date
     DISAPLINE - Input Ski/Tele/SB
     TIME      - Input lesson Time
     TYPE      - Input lesson type A/D
     LIST      - List instructors
     LOAD      - Load Entered Data into Table
     EXIT      - Quit or Exit program""" % (self.student_firstname,
                                       self.student_lastname,
                                       self.student_age,
                                       self.student_skill_level,
                                       self.contact_firstname,
                                       self.contact_lastname,
                                       self.contact_relation,
                                       self.phone_display(),
                                       self.shift_date.date(True),
                                       self.start_time.time(True),
                                       self.end_time.time(True),
                                       self.lesson_length,
                                       self.instructor_firstname,
                                       self.instructor_lastname,
                                       self.lesson_type,
                                       self.discipline))

    def phone_display(self):
        """convert phone number to display value and return"""
        l = len(self.contact_phone)
        if l==7:
            phone = """%s-%s""" % (self.contact_phone[0:3], self.contact_phone[3:7])
        elif l==10:
            phone = """%s-%s-%s""" % (self.contact_phone[0:3], self.contact_phone[3:6], self.contact_phone[-4:])
        else:
            phone = self.contact_phone
            
        return phone
    
    def list_avalible(self):
        """function for get avalable instructors based on private needs"""
        #print('List_avalible')
        not_set = self.check_add_shift()
        if not_set==None:
            if self.sid==None:
                self.add_shift_db() 
            print("""shift sid: %s""" % (self.sid))
            
            if not self.available_instructors:
                self.available_instructors = instructors()
            self.available_instructors.get_available_instructors(sid=self.sid)
            os.system('clear')
            print("    Available Instructor List ")
            print("    -----------------------------------------------------------------")
            self.available_instructors.list_instructors()
            return None
        else:
            return not_set

    def load_private(self, dump=None):
        """Save a new private, or update a private in the database"""
        if self.sid==None:
            m = self.check_add_shift()
            if m==None:
                self.add_shift_db()
            else:
                raw_input(m)
                return
        if self.pid==None:
            self.add_private_db()
        else:
            if self.update:
                self.update_private_db()
                
    def print_self(self, count):
        """function for displaying this private, in a list of privates"""
        print("""    %s %s %s %s %s""" % (str(count).ljust(4), self.date.ljust(10), self.start_time.ljust(8), self.end_time.ljust(8), self.shift_name))
        
    def print_private_all(self):
        """function for displaying private information in a long form"""
        print ("""shift_name = %s,
start_time = %s,
end_time = %s,
html_class = %s,
date = %s,
sid = %s,
ct = %s,
ct_title = %s
student_firstname = %s
self.student_lastname = %s
self.contact_firstname = %s
self.contact_lastname = %s
self.contact_phone = %s
self.contact_relation = %s
self.student_age = %s
self.student_skill_level = %s
self.lesson_length = %s
self.lesson_type = %s
self.discipline = %s
self.eid = %s
self.instructor_firstname = %s
self.instructor_lastname = %s""" % (self.shift_name,
                                    self.start_time,
                                    self.end_time,
                                    self.html_class,
                                    self.date.date(),
                                    self.sid,
                                    self.ct,
                                    self.ct_title,
                                    self.student_firstname,
                                    self.student_lastname,
                                    self.contact_firstname,
                                    self.contact_lastname,
                                    self.contact_phone,
                                    self.contact_relation,
                                    self.student_age,
                                    self.student_skill_level,
                                    self.lesson_length,
                                    self.lesson_type,
                                    self.discipline,
                                    self.eid,
                                    self.instructor_firstname,
                                    self.instructor_lastname))

    def set_age(self,options):
        """function for geting student age and seting in private object"""
        try:
            if options[1]:
                self.student_age = options[1]
            else:
                self.student_age = options[2][0]
        except:
            self.student_age = raw_input('Student Age: ')
        self.update = True
        
    def set_contact(self, options):
        """function for getting contact name and storing in private object"""
        try:
            self.contact_firstname = options[2][0].capitalize()
        except:
            self.contact_firstname = raw_input('Contact First Name: ').capitalize
        try:
            self.contact_lastname = options[2][1].capitalize()
        except:
            self.contact_lastname = raw_input('Contact Last Name: ').capitalize
        try:
            self.contact_relation = options[2][2].capitalize()
        except:
            self.contact_relation = raw_input('Contact Relationship: ').capitalize()
        self.update = True
        
    def set_discipline(self, options):
        """collect discipline and set discpline and ct_title"""
        
        try:
            if options[2]:
                self.discipline = options[2][0].capitalize()
        except:
            self.discipline = raw_input('Ski/SB/Tele: ').capitalize()
        if self.discipline=='Ski':
            self.ct_title = 'Ski Instructor'
            return True
        elif self.discipline=='Sb':
            self.ct_title = 'SB Instructor'
            self.discipline = self.discipline.upper()
            return True
        elif self.discipline=='Tele':
            self.ct_title = 'Tele Instructor'
            return True
        elif self.discipline in ['Exit', 'Exi', 'Ex', 'E']:
            return False
        else:
            self.set_discipline([])
        self.update = True
        
    def set_date(self, options):
        """method for getting date, verifing, and setting in private object""" 
        try:
            self.shift_date.date(options[2][0])
        except:
            self.shift_date.date(raw_input('Lesson Date: ') )          
        self.update = True
        
    def set_instructor(self, options):
        """Method for display available instructor(s) base on private needs and setting object with select instructor"""
        e = self.list_avalible()
        if not e:
            try:
                self.eid = int(raw_input('employee id: '))
                bad = False
            except:
                bad = True
            if not bad:
                instructor = self.available_instructors.get_name(eid=self.eid, return_type='Object')
                self.instructor_firstname = instructor.firstname
                self.instructor_lastname = instructor.lastname
                self.add_employee_shift()
                self.update = True
        else:
            dump = raw_input(e)

    def set_shift_name(self):
        """set shift title"""
        self.shift_name = """Private - %s %s %s""" % (self.lesson_type, self.student_firstname, self.discipline )
        self.update = True
        #print(self.shift_name)
                    
    def set_skill(self, options):
        try:
            if options[1]:
                print(options[1])
                self.student_skill_level = options[1]
            else:
                print(options[2][0])
                self.student_skill_level = options[2][0]
            
        except:
            self.student_skill_level = raw_input('Student Skill Level(1-9): ')
        self.update = True
        
    def set_student(self, options):
        try:
            self.student_firstname = options[2][0].capitalize()
        except:  
            self.student_firstname = raw_input('Student First Name: ').capitalize()
        try:
            self.student_lastname = options[2][1].capitalize()
        except:    
            self.student_lastname = raw_input('Student Last Name: ').capitalize()
        self.update = True
        
    def set_time(self, options):
        print(options)
        try:
            t = options[2][0]
            print(t)
        except:
            t = None
        self.start_time.set_time(t)
        try:
            t = options[2][1]
            print(t)
        except:
            t = None
        self.end_time.set_time(t)
        self.update = True
        print("""start time: %s, end time:%s""" % (self.start_time.time(True), self.end_time.time(True)))
        
    def set_type(self, options):
        self.lesson_type = ''
        while self.lesson_type not in ['A', 'D']:
            try:
                self.lesson_type = options[2][0].upper()
            except:    
                self.lesson_type = raw_input('A/D: ').upper()
            options = []
        if self.lesson_type=='A':
            self.html_class='Assigned'
        else:
            self.html_class='Demand'
        self.update = True
           
    def set_phone(self, options):
        print('set_phone: %s' % (options))
        try:
            if options[1]:
                self.contact_phone = str(options[1])
            else:
                self.contact_phone = options[2][0]
        except:
            self.contact_phone = raw_input('Contact Phone: ')
        self.update = True
    
    def update_private_db(self):
        #need to make work, only resets check
        if self.update:
            if self.sid!=None:
                #update_shift not implemented yet!
                #self.db_handle.fetchdata('update_shift', [self.sid,])
                pass
            else:
                self.add_shift_db()
            if self.pid!=None:
                    #Update_private not implemented yet!
                    #self.db_handle.fetchdata('update_private', [self.pid])
                    pass
            else:
                self.add_private_db()
            self.update = False
    
class privates(object):
    """Container for private objects"""
    def __init__(self, db_handle=None):
        self.privates = []
        self.db_handle = db_handle
    
    def append(private):
        self.privates.append(private)
        self.sort()

    def checkID(self, pid):
        for i in self.plist:
            if i.pid==pid:
                return i
        return None
    
    def find_privates(self, options):
        F = find_private(self.db_handle)
        F.menu(options)
        result = self.db_handle.fetchdata('Find_private',
                                 [F.student.firstname(),
                                  F.student.lastname(),
                                  F.contact.firstname(),
                                  F.contact.lastname(),
                                  F.instructor.firstname(),
                                  F.instructor.lastname(),
                                  F.date,
                                  F.displine,
                                  F.type,
                                  F.age,]
                                 )
        self.clear()
        for r in result:
            self.append(r)
                    
    def sort(self):
        end_time = sorted(self.privates, key=attrgetter('end_time'))
        start_time = sorted(end_time, key=attrgetter('start_time'))
        self.privates = sorted(start_time, key=attrgetter('shift_date'))

    def print_list(self):
        count = 0
        print("    Privates List")
        print("    --------------------------------------------------------")
        for p in self.plist:
            p.print_self(count)
            count += 1
    
    def print_this(self,dump):
        print('menu display text')
        
class find_private(object):
    def __init__(self, db_handle=None):
        self.set_db_handle(db_handle)
        self.contact = person(db_handle=self.db_handle)
        self.student = person(db_handle=self.db_handle)
        self.instructor = person(db_handle=self.db_handle)
        self.start_date = date(None,
                               question_text='Enter Start Date: ',
                               db_handle=self.db_handle)
        self.end_date = date(None,
                             question_text='Enter End Date: ',
                             db_handle=self.db_handle)
        self.disapline = None
        self.type = None
        self.age = None
                
    def print_self(self, dump=None):
        print("""
    Contact Name:       %s
    Student Name:       %s
    Instructor Name:    %s
    Search Start Date:  %s
    Search End Date:    %s
    Lesson Disapline:   %s
    Lesson Type:        %s
    Age:                %s""" % (self.contact.name(),
                                 self.student.name(),
                                 self.instructor.name(),
                                 self.start_date.date(True),
                                 self.end_date.date(True),
                                 self.disapline,
                                 self.type,
                                 self.age))

    def menu(self, options):
        try:
            m = Menu(db_handle=options[4], menu_title='Find Private Menu')
        except:
            m = Menu(menu_title='Find Private Menu')
        #try:
        #    action, index, option = m.split_command(option[2])
        #    if action in ['DATE', 'DAT', 'DA', 'D']:
        #        print(option)
        #    elif action in ['STUDENT']:
        #        pass
        #    else:
        #        find = find_private()
        #        print('find_private if action else section')
        #except:
        
        m.menu_display = self.print_self
        m.add_item('Student', 'Enter Student Name', self.student.set_name)
        m.add_item('Contact', 'Enter Student Name', self.contact.set_name)
        m.add_item('Instructor', 'Enter Instuctor Name', self.instructor.set_name)
        m.add_item('Start', 'Enter start date', self.start_date.get_date)
        m.add_item('End', 'Enter end date', self.end_date.get_date)
        m.add_item('Discipline', 'Enter Discipline (Ski/SB/Tele)', self.set_discipline)
        m.add_item('Type', 'Enter type (assigned/demand)', self.set_type)
        m.add_item('Find', 'Find privates matching', m.return_now)
        m.Menu()

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='private.py - find_private')
        self.db_handle = db_handle

    def set_discipline(self, options):
        raw_input('set discipline function, noting happening.')
    
    def set_type(self, options):
        raw_input('set type function, nothing happening yet!')

def menu(db_handle):
    P = private(db_handle=db_handle)
    private_new = Menu('Add New Private Menu', db_handle=db_handle)
    private_new.menu_display = P.PrivateMenu
    private_new.add_item('Contact', 'CONTACT <firstname> <lastname> <relationship> - Enter contact person information for private lesson', P.set_contact)
    private_new.add_item('Student', 'STUDENT <Firstname> <Lastname> - Name of person taking the lesson', P.set_student)
    private_new.add_item('Phone', 'PHONE <#> - Set contact phone number', P.set_phone)
    private_new.add_item('Type', 'TYPE <A/D> - set lesson type as assigned or Demand', P.set_type)
    private_new.add_item('Age', 'AGE <#> - Enter the students age', P.set_age)
    private_new.add_item('Time', 'TIME <starttime> <endtime> - Enter start and stop times', P.set_time)
    private_new.add_item('Discipline', 'DISCIPLINE <SKI/SB/TELE>- Set the disapline', P.set_discipline)
    private_new.add_item('Date', 'DATE <MM/DD/YYYY> - set date of the lesson', P.set_date)
    private_new.add_item('Load', 'LOAD - Save private to database', P.load_private)
    private_new.add_item('List', 'LIST - List instructors', P.set_instructor)
    private_new.add_item('Find', 'FIND <firstname> <lastname> - find instrutors by name', P.find_instructor)
    private_new.add_item('Skill', 'SKILL <1-9> or SKILL <Yellow,Yellow+,green,blue> - Skill level of the student', P.set_skill)
    private_new.Menu()
   
if __name__ == '__main__':    
    db_handle = database(owner='Private __Main__')
    F = find_private(db_handle)
    F.print_self()
    
        