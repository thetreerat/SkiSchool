# Author: Harold Clark
# Copyright Harold Clark 2019
#
from datetime import datetime
from instructor import instructor
from instructor import instructors
from shift import shift
import sys
import os
import psycopg2
                
        
class private(shift):
    def __init__(self,
                 shift_name=None,
                 start_time=None,
                 end_time=None,
                 html_class=None,
                 date=None,
                 sid=None,
                 ct=None,
                 ct_title=None):
        """Init a private lesson object"""
        shift.__init__(self, shift_name=shift_name,
                             start_time=start_time,
                             end_time=end_time,
                             html_class=html_class,
                             date=date,
                             sid=sid,
                             ct=ct,
                             ct_title=ct_title)
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
        self.eid = None
        self.instructor_firstname = None
        self.instructor_lastname = None
    
    def check_add_shift(self):
        if self.date==None:
            print('date not set!')
        elif self.start_time==None:
            print('start time not set!')
            return False
        elif self.end_time==None:
            print('end time not set!')
            return False
        elif self.discipline==None:
            print('disipline not set!')
            return False
        else:
            if self.shift_name==None:    
                self.set_shift_name()
            else:
                print("""Bad shift name: %s""" % (self.shift_name))
            return True
    
    def PrivateMenu(self):        
        print("""     Private screen
     --------------------------------
     Student Name:         %s %s
     Student Age:          %s
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
                                       self.contact_firstname,
                                       self.contact_lastname,
                                       self.contact_relation,
                                       self.phone_display(),
                                       self.date,
                                       self.start_time,
                                       self.end_time,
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
    
    def set_discipline(self):
        """collect discipline and set discpline and ct_title"""
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
            self.discipline = raw_input('please enter Ski, SB, or Tele: ')
            self.set_discipline()
            
    def set_shift_name(self):
        """set shift title"""
        self.shift_name = """Private - %s %s %s""" % (self.lesson_type, self.student_firstname, self.discipline )
        print(self.shift_name)
        
    def list_avalible(self, I):
        if self.check_add_shift():
            if self.sid==None:
                self.add_shift_db() 
            print("""shift sid: %s""" % (self.sid))     
            c = psycopg2.connect(user="postgres",
                                 port="5432",
                                 host="127.0.0.1",
                                 database="skischool")
            cur = c.cursor()
            cur.callproc('list_availble', [self.sid,])
            result = cur.fetchall()
            for r in result:
                i = instructor()
                i.eid = r[0]
                i.firstname = r[1]
                i.lastname = r[2]
                I.add_instructor(i)
            c.commit()
            cur.close()
            c.close()
            I.list_instructors()
            return True
        else:
            return False
        
    def print_private_all(self):
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
                                    self.date,
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

    def list_employees(self):
        I = instructors()
        e = l.list_avalible(I)
        if e:
            l.eid = raw_input('employee id: ')
            name = I.get_name(l.eid, 'Name')
            self.instructor_firstname, self.instructor_lastname = name.split()
        else:
            dump = raw_input('ready? ')
       
if __name__ == '__main__':
    l = private()
    print("""New Private Lesson""")

    while True:
        l.PrivateMenu()
        answer = raw_input('Please enter a selection: ').upper()
        #answer = list(answer.split())
        #answer[0] = answer[0].upper()
        while answer:
            if answer in ['EXIT', 'EXI', 'EX', 'E', 'QUIT', 'QUI', 'QU', 'Q']:
                sys.exit(1)
            elif answer in ['CONTACT','CONTAC','CONTA','CONT','CON','CO','C']:
                print(answer)
                l.contact_firstname = raw_input('Contact First Name: ')
                l.contact_lastname = raw_input('Contact Last Name: ')
                l.contact_relation = raw_input('Contact Relationship: ')
                break
            elif answer in ['NAME','NAM','NA','N']:
                l.student_firstname = raw_input('Student First Name: ')
                l.student_lastname = raw_input('Student Last Name: ')
                break
            elif answer in ['PHONE','PHON','PHO','PH','P']:
                l.contact_phone = raw_input('Contact Phone: ')
                break
            elif answer in ['TYPE','TYP','TY']:
                l.lesson_type = raw_input('A/D: ').upper()
                if l.lesson_type not in ['A','D']:
                    answer = raw_input("""%s is not valid A or D only: """ % (l.lesson_type))
                else:
                    if l.lesson_type=='A':
                        l.html_class='Assigned'
                    else:
                        l.html_class='Demand'
                    break
            elif answer in ['AGE', 'AG', 'A']:
                l.student_age = raw_input('Student Age: ')
                break
            elif answer in ['TIME','TIM','TI']:
                l.start_time = raw_input('Lesson Start: ')
                l.end_time = raw_input('Lesson End: ')
                l.lesson_length = datetime.strptime(l.end_time, '%H:%M') - datetime.strptime(l.start_time, '%H:%M')
                break
            elif answer in ['DISCIPLINE','DISCIPLIN','DISCIPLI','DISCIPL','DISCIP','DISCI','DISC','DIS','DI']:
                l.set_discipline()
                break
            elif answer in ['DATE','DAT','DA']:
                l.date = raw_input('Lesson Date: ')
                break
            elif answer=='D':
                answer = raw_input('DATE or DISCIPLINE? ').upper()
            elif answer=='L':
                answer = raw_input('LIST or LOAD? ').upper()
            elif answer=='T':
                answer = raw_input('TIME or TYPE? ').upper
            elif answer in ['HAL']:
                os.system('cls')
                l.print_private_all()
                raw_input('<enter>')
                os.system('cls')
                break
            elif answer in ['LIST','LIS','LI']:
                l.list_employees()
                break
            elif answer in ['LOAD','LOA','LO']:
                break
            else:
                print(answer)
                raw_input("ready?")
                break


    print("bye, bye")

#    l.student_firstname = input('Enter student First Name: ')
#    l.student_lastname = input('Enter student Last Name: ')
#    l.contact_firstname = input('Enter Contact First Name: ')
#    l.contact_lastname = input('Enter Contact Last Name: ')
#    l.contact_phone = input('Enter Contact Phone Number: ')
    
    
        