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

    def __repr__(self):
        return "Employee - %s, db=%s, pythonID: %s" % (self.name(), self.db_handle.owner, id(self))

    def __str__(self):
        return "Employees - %s, db=%s" % (self.name(), self.db_handle.owner)
           
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : New Class
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
    
    def append_shift(self, shift):
        self.shifts.append(shift)
        self.sort()
                        
    def sort(self):
        end_time = sorted(self.shifts, key=attrgetter('end_time'))
        start_time = sorted(end_time, key=attrgetter('start_time'))
        self.shifts = sorted(start_time, key=attrgetter('date'))
        
class employees(object):
    employee.index = 1
    employee.object = 2
    employee.eid = 3
    employee.full_name = 4
    employee.no_index = 5
    def __init__(self, db_handle=None):
        self.elist = []
        self.set_db_handle(db_handle)

    def __repr__(self):
        return "Employees - %s, db=%s, pythonID: %s" % (len(self.elist), self.db_handle.owner, id(self))

    def __str__(self):
        return "Employees - %s, db=%s" % (len(self.elist), self.db_handle.owner)
    
    def append(self, employee):
        if not self.check_name(employee.firstname, employee.lastname):
            self.elist.append(employee)
            self.sort_list()
    
    def check_id(self, eid, return_type=employee.index):
        i = 0
        for p in self.elist:
            if p.eid==eid:
                if return_type==employee.index:
                    return i
                elif return_type==employee.full_name:
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

    def list(self, return_type=employee.no_index, shifts=True):
        index = 0
        for e in self.elist:
            if return_type==employee.index:
                count = index
            else:
                count = None
            e.print_self(count=count)
            index += 1
            if shifts:
                for s in e.shifts:
                    s.print_shift()
        
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='employees')
        self.db_handle = db_handle

    def sort_list(self):
        firstname = sorted(self.elist, key=attrgetter('_firstname'))
        self.elist = sorted(self.elist, key=attrgetter('_lastname'))
        #print(len(firstname))
    
if __name__ == "__main__":
    db_handle = database(owner='employee.py - __main__')
    E = employee(db_handle=db_handle)
    #E.set_name()
    #E.set_DOB()
    #print(E.age())
    ##E.print_self()
    print(E)
    #E
    #print(E.name())