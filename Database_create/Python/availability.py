# Author: Harold Clark
# Copyright Harold Clark 2019
#

import sys
import os
import psycopg2
from database import database
from menu import Menu

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
        self.eaid = eaid
        self.eid = eid
        self.dow = dow
        self.start_time = start_time
        self.end_time = end_time
        self.said = said
        if db_handle==None:
            db_handle = database(onwer='availability.py - availability')
        self.db_handle = db_handle
    
    def add(self):
        """create a new record and save to db"""
        dow = ''
        while dow not in ['monday', 'tuesday', 'wednesday', 'thursday','friday', 'saturday', 'sunday']:
            dow = raw_input("""Enter Day of week (%s): """ % (dow)).lower()
        self.dow = dow
        self.start_time = raw_input('Enter Start Time: ')
        self.end_time = raw_input('Enter End Time: ')
        result = self.db_handle.fetchdata('add_employee_availabilty', [self.eid, self.dow, self.start_time, self.end_time])
        self.eaid = result[0][0]

    def edit(self):
        """function for editing a availablility object"""
        run = True
        while run:
            os.system('clear')
            self.print_availability()
            self.print_options()
            answer = raw_input('Enter Selection: ').upper()
            answer = list(answer.split())
            while answer:
                if answer[0] in ['EXIT','EXI','EX']:
                    sys.exit(1)
                elif answer[0] in ['START','STAR','STA','ST','S']:
                    self.edit_start()
                    break
                elif answer[0] in ['END','EN']:
                    self.edit_end()
                    break
                elif answer[0]=='E':
                    answer = list(raw_input('END or EXIT? ').upper().split())
                    
                elif answer[0] in ['DOW','DO','D']:
                    self.edit_dow()
                    break
                elif answer[0] in ['RETURN','RETUR','RETU','RET','RE','R','MAIN','MAI','MA','M']:
                    run = False
                    break
                else:
                    answer = raw_input('Your Lost!: ')
                    break
        
    def edit_end(self):
        end = raw_input("""Enter End Time (%s): """ % (self.end_time))
        if end!='' and end!=self.end_time:
            self.database_update('update_employee_availability_end', [self.eaid, end])
            self.end_time = end

    def edit_dow(self):
        """edit dow string and update database"""
        dow = raw_input('Enter Day of Week (%s): ' % (self.dow)).lower()
        if dow!='' and dow!=self.dow:
            r = self.database_update('update_employee_availability_dow', [self.eaid, dow,])
            self.dow = dow
    
    def edit_start(self):
        start = raw_input("""Enter Start Time (%s): """ % (self.start_time))
        if start!='' and start!=self.start_time:
            self.database_update('update_employee_availability_start', [self.eaid, start])
            self.start_time = start
               
    def print_availability(self):
        try:
            start_time = self.start_time.strftime('%H:%M').ljust(15)
        except:
            start_time = self.start_time.ljust(15)
        try:
            end_time = self.end_time.strftime('%H:%M').ljust(15)
        except:
            end_time = self.end_time.ljust(15)
            
        print("""    %s %s %s %s""" % (str(self.eaid).ljust(7),
                                       self.dow.ljust(12),
                                       start_time,
                                       end_time))
    
    def print_options(self):
        print("""    DOW, START, END, EXIT, RETURN
            """)        
        

    
class availablities(object):
    """Class for list of availbilties"""
    def __init__(self, eid=None, db_handle=None):
        self.alist = []
        self.eid = eid
        if db_handle==None:
            db_handle = database(owner='availablity.py - availablitites')
        self.db_handle =  db_handle
                
    def add(self, answer):
        if self.eid!=None:
            a = availability(eid=self.eid)
            a.add()
            self.alist.append(a)
                        
    def checkID(self, ID):
        """check to list for ID"""
        for i in self.alist:
            if i.eaid==ID:
                return i
        return None
    
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
                        
    def get_employee_availablity(self):
        if self.eid!=None:
            result = self.db_handle.fetchdata('get_employee_availability',[self.eid,])
            for r in result:
                a = availability(eaid=r[0],
                                 eid=r[1],
                                 dow=r[2],
                                 start_time=r[3],
                                 end_time=r[4],
                                 db_handle=self.db_handle)
                self.alist.append(a)
                        
    def menu(self):
        """main menu for availability"""
        run = True
        while run:
            os.system('clear')
            self.print_list()
            self.print_menu()
            answer = list(raw_input('Enter selection: ').split())
            answer[0] = answer[0].upper()
            while answer:
                if answer[0] in ['EXIT', 'EXI', 'EX', 'QUIT', 'QUI', 'QU', 'Q']:
                    sys.exit(1)

                elif answer[0] in ['EDIT','ED','ED']:
                    self.edit(answer)
                    break
                elif answer[0] in ['ADD', 'AD', 'A']:
                    self.add(answer)
                    break
                elif answer[0] in ['RETURN','RETUR','RETU','RET','RE','R']:
                    run=False
                    break
           
    def print_menu(self, help_request=False):
        """menu options printed"""
        if help_request==True:
            print("""    Help Menu
    -----------------------------------------------------
    ADD    - Add new employee availability
    EDIT # - Edit employee availability Number #
    HELP   - This menu
    RETURN - Retrun to previous menu
    EXIT   - Exit to system prompt""")
        else:
            print("""    ADD, EDIT, HELP, RETURN, EXIT""")
                        
    def print_list(self):
        print("""    EAID    Day of Week  Start Time      End Time
    ------- ------------ --------------- ---------------- """)
        for a in self.alist:
            a.print_availability()
        print("""    -----------------------------------------------------""")

if __name__ == '__main__':
    A = availablities(eid=15)
    A.get_employee_availablity()
    A.eid
    A.menu()
    #A.print_list()
    #a = A.alist[0]
    #a.edit()