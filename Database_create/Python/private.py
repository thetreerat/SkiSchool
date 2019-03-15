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
                
        
class private(object):
    def __init__(self):
        """Init a private lesson object"""
        self.student_firstname = ''
        self.student_lastname = ''
        self.contact_firstname = ''
        self.contact_lastname = ''
        self.contact_phone = ''
        self.contact_relation = ''
        self.student_age = None
        self.student_skill_level = ''
        self.date = None
        self.start_time = None
        self.end_time = None
        self.lesson_length = None
        self.lesson_type = None
        self.discipline = None
        self.eid = None
        self.instructor_firstname = None
        self.instructor_lastname = None
    
    def check_add_shift():
        if self.date==None:
            print('date not set!')
        elif self.start_time==None:
            print('start time not set!')
            return False
        elif self.end_time==None:
            print('end time not set!')
        elif self.disipline==None:
            print('disipline not set!')
        else:
            

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
     NAME    - Input Student Name
     CONTACT - Input Contact Name
     PHONE   - Input Phone
     AGE     - Input Student Age
     DATE    - Input Lesson Date
     TIME    - Input lesson Time
     TYPE    - Input lesson type A/D
     LIST    - List instructors
     LOAD - Load Entered Data into Table
     EXIT - Quit or Exit program""" % (self.student_firstname,
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
    
    def list_avalible(self):
        if self.check_add_shift():
            c = psycopg2.connect(user="postgres",
                                 port="5432",
                                 host="127.0.0.1",
                                 database="skischool")
            cur = c.cursor()
            cur.callproc('list_availble', [142,])
            result = cur.fetchall()
            I = instructors()
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
                l.lesson_type = raw_input('A/D: ')
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
                l.discipline = raw_input('Ski/SB/Tele: ')
                break
            elif answer in ['DATE','DAT','DA']:
                l.date = raw_input('Lesson Date: ')
                break
            elif answer=='D':
                answer = raw_input('DATE or DISCIPLINE? ')
            elif answer in ['HAL']:
                os.system('cls')
                print("He is a good guy")
                raw_input('<enter>')
                os.system('cls')
                break
            elif answer in ['LIST','LIS','LI']:
                l.list_avalible()
                l.eid = raw_input('employee id: ')
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
    
    
        