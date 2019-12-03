# Author: Harold Clark
# Copyright Harold Clark 2019
#

import sys
import os
import psycopg2
from database import database
from date import date
from skitime import SkiTime
from dow import DOW
from menu import Menu
from employee import employee

class availability(object):
    """Base Class object for availbiltiy"""
    def __init__(self,
                 eaid=None,
                 eid=None,
                 dow=None,
                 start_time=None,
                 end_time=None,
                 said=None,
                 db_handle=None):
        """init availability object"""
        self.set_db_handle(db_handle)
        self.eaid = eaid
        self.eid = employee(eid=eid, db_handle=self.db_handle)
        if self.eid.eid:
            self.eid.load_emp_db()
        self.dow = DOW(dow=dow, db_handle=self.db_handle)
        self.start_time = SkiTime(time=start_time,
                                  question='Enter start Time of Availability: ',
                                  db_handle=self.db_handle)
        self.end_time = SkiTime(time=end_time,
                                question='Enter end time of availability: ',
                                db_handle=self.db_handle)
        self.said = said
        
    def add(self):
        """create a new record and save to db"""
        if not self.dow.DOW():
            self.dow.get_dow()
        self.start_time.set_time()
        self.end_time.set_time()
        result = self.db_handle.fetchdata('add_employee_availabilty', [self.eid.eid, self.dow.DOW(), self.start_time.time(True), self.end_time.time(True)])
        try:
            self.eaid = result[0][0]
        except Exception as e:
            print(e)
            raw_input('resume <enter>')

    def edit(self):
        """function for editing an availablility object"""
        M = Menu('Edit an employee availablity Menu', db_handle=self.db_handle)
        M.menu_display = self.print_edit_menu
        M.add_item('Start', 'Start - edit start time', self.edit_start)
        M.add_item('DOW', 'DOW <dow> - edit dow of the week.', self.edit_dow)
        M.add_item('End', 'END <time> - edit end time.', self.edit_end)
        M.Menu()
        
        
    def edit_end(self, options=None):
        end = raw_input("""Enter End Time (%s): """ % (self.end_time.time(True, True)))
        if end!='' and end!=self.end_time.time(True, True):
            # need to fix following line to use db_handle.bahbah()
            self.db_handle.fetchdata('update_employee_availability_end', [self.eaid, end])
            self.end_time.set_time(time=end)

    def edit_dow(self, options=None):
        """edit dow string and update database"""
        dow = raw_input('Enter Day of Week (%s): ' % (self.dow)).lower()
        if dow!='' and dow!=self.dow:
            # need to fix following line to use db_handle.bahbah()
            self.db_handle.fetchdata('update_employee_availability_dow', [self.eaid, dow,])
            self.dow = dow
    
    def edit_start(self, options=None):
        start = raw_input("""Enter Start Time (%s): """ % (self.start_time.time(True, True)))
        if start!='' and start!=self.start_time:
            self.db_handle.fetchdata('update_employee_availability_start', [self.eaid, start])
            self.start_time.set_time(start)
               
    def print_all(self, options=None):
        print("""    %s %s %s %s %s %s""" % (str(self.eaid).ljust(7),
                                       self.eid.name(True).ljust(30),
                                       str(self.eid.age()).ljust(4),
                                       self.dow.DOW().ljust(13),
                                       self.start_time.time(True).ljust(12),
                                       self.end_time.time(True).ljust(11)))
        
    def print_availability(self, options=None):
        print("""    %s %s %s %s""" % (str(self.eaid).ljust(7),
                                       self.dow.DOW().ljust(12),
                                       self.start_time.time(True).ljust(15),
                                       self.end_time.time(True).ljust(15)))
    
    def print_edit_menu(self, options=None):
        print("""    Employee:    %s
    Age:         %s
    EAID:        %s
    Day of Week: %s
    Start Time:  %s
    End Time:    %s""" % (self.eid.name(),
                          self.eid.age(),
                          self.eaid,
                          self.dow.DOW(),
                          self.start_time.time(True),
                          self.end_time.time(True)))

                
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='availablity.py - set_db_handle')
        self.db_handle = db_handle

    
class availablities(object):
    """Class for list of availbilties"""
    def __init__(self, eid=None, dow=None, db_handle=None):
        self.set_db_handle(db_handle)
        self.alist = []
        self.eid = employee(eid=eid, db_handle=self.db_handle)
        self.dow = DOW(dow=dow, db_handle=self.db_handle)    
        
    def __len__(self):
        return len(self.alist)
    
    def append(self, availablity):
        self.alist.append(availablity)
        self.sort()
        
    def add(self, options=None):
        if self.eid.eid!=None:
            a = availability(eid=self.eid.eid, db_handle=self.db_handle)
            a.add()
            self.append(a)
                        
    def checkID(self, ID):
        """check to list for ID"""
        for i in self.alist:
            if i.eaid==ID:
                return i
        return None
    
    def clear(self):
        self.alist = []
        
    def edit(self, answer):
        """edit an availablity by ID"""
        if len(answer)==1:
            ID = raw_input('Enter ID: ')
        else:
            ID = answer[1]
        try:
            ID = int(ID)     
        except:
            print('field not an integer')            
        a = self.checkID(ID)
        if a!=None:
            a.edit()

    def get_dow_availablity(self, options=None):
        
        if not self.dow.DOW():
            self.dow.get_dow(options)
        self.clear()
        result = self.db_handle.fetchdata('get_dow_avalibility', [self.dow.DOW(),])
        for r in result:
            a = availability(eaid=r[0],
                             eid=r[1],
                             dow=r[2],
                             start_time=r[3],
                             end_time=r[4],
                             said=r[5],
                             db_handle=self.db_handle)
            self.append(a)
                        
    def get_employee_availablity(self):
        if self.eid.eid!=None:
            result = self.db_handle.fetchdata('get_employee_availability',[self.eid.eid,])
            for r in result:
                a = availability(eaid=r[0],
                                 eid=r[1],
                                 dow=r[2],
                                 start_time=r[3],
                                 end_time=r[4],
                                 db_handle=self.db_handle)
                self.alist.append(a)
                        
    def menu_dow(self, options=None, db_handle=None):
        """main menu for availability"""
        self.get_dow_availablity(options=options)
        M = Menu('Day of Week Availablities Menu', db_handle=self.db_handle)
        M.menu_display = self.print_dow
        M.add_item('DOW', 'Add an availablity on a day for employee', self.dow.get_dow) # 
        M.add_item('Edit', 'Edit # - Edit availablity id for employee', self.edit)
        M.add_item('Delete', 'Delete # - Delete availablity id for employee', M.print_new)
        M.Menu()

    def menu(self, options=None, db_handle=None):
        """main menu for availability"""
        M = Menu('Employee Availablities Menu', db_handle=self.db_handle)
        M.menu_display = self.print_list
        M.add_item('Add', 'Add an availablity on a day for employee', self.add)
        M.add_item('Edit', 'Edit # - Edit availablity id for employee', self.edit)
        M.add_item('Delete', 'Delete # - Delete availablity id for employee', M.print_new)
        M.Menu()
    
    def print_dow(self):
        print(("""Availablity list of instructors on %ss""" % self.dow.DOW()).center(80))
        print("""
    EAID    Instructor                     Age  Day of Week   Start Time   End Time
    ------- ------------------------------ ---  ------------- ------------ ---------------""")
                                          
        for a in self.alist:
            a.print_all()
        print("""    -----------------------------------------------------""")
        print("""    Count: %s """ % (len(self)))
        

    def print_list(self):
        print("""    EAID    Day of Week  Start Time      End Time
    ------- ------------ --------------- ---------------- """)
        for a in self.alist:
            a.print_availability()
        print("""    -----------------------------------------------------""")
        print("""    Count: %s """ % (len(self)))

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='availability.py - set_db_handle')
        self.db_handle = db_handle
        
    def sort(self):
        eid_alist = sorted(self.alist, key=self.sort_eid)
        self.alist = sorted(eid_alist, key=self.sort_start)
    
    def sort_eid(self, i):
        return i.eid
    
    def sort_start(self, i):
        return i.start_time.time(True)
        
if __name__ == '__main__':
    from login import Login
    L = Login(login='halc')
    L.Login()
    A = availablities(db_handle=L.db_handle)
    A.dow.set_dow('tuesday')
    A.get_dow_availablity()
    #print(A.alist[0].eid)
    for a in A.alist:
        #a.print_all()
        a.print_edit_menu()
    #A.eid
    #A.alist[0].print_edit_menu()
    #A.menu_dow()
    #A.print_list()
    #A.menu()