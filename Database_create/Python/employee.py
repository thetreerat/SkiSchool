# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from person import person
from operator import attrgetter

class  employee(person):
    """employee object subclassed from person"""
    def __init__(self, eid=None, firstname=None, lastname=None, db_handle=None):
        """Create new instanace of employee"""
        person.__init__(self, firstname=firstname, lastname=lastname, db_handle=db_handle)
        self.eid = eid
        self.shifts = []
        self.set_db_handle(db_handle)
    
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : New Class
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
    
    def append_shift(self, shift_name):
        self.shifts.append(shift_name)
        self.sort_list()
        
    def append_shift(self, shift_name):
        self.shifts.append(shift_name)
        
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='employee')
        self.db_handle = db_handle
        
    def sort_list(self):
        end_time = sorted(self.shifts, key=attrgetter(end_time))
        start_time = sorted(end_time, key=attrgetter(start_time))
        self.shifts = sorted(start_time, key=attrgetter(date))
        
class employees(object, db_handle=None):
    employee.index = 1
    employee.object = 2
    employee.eid = 3
    employee.name = 4
    def __init__(self):
        self.elist = []
        self.set_db_handle(db_handle)
    
    def append(self, employee):
        if not self.check_name(employee.firstname, employee.lastname):
            self.elist.append(employee)
            self.sort()
    
    def check_id(self, eid, return_type=employee.index):
        i = 0
        for p in self.elist:
            if p.eid==eid:
                if return_type==employee.index:
                    return i
                elif return_type==employee.name:
                    return p.name()
                elif return_type==employee.object:
                    return p
            i += 1
        return None
                
    def check_name(self, firstname, lastname, return_type=employee.index):
        i = 0
        for p in self.elist:
            if p._firstname==firstname and p._lastname==lastname:
                if return_type==employee.index:    
                    return i
                elif return_type==employee.object:
                    return p
                elif return_type==employee.eid:
                    return p.eid
            i+=1
        return None

    def list(self):
        for e in self.elist:
            e.print_self()
        
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='employee')
        self.db_handle = db_handle

    def sort(self):
        firstname = sorted(self.elist, key=attrgetter(firstname))
        self.elist = sorted(firstname, key=attrgetter(lastname))
        
if __name__ == "__main__":
    db_handle = database(owner='employee.py - __main__')
    