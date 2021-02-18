# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from person import person
from operator import attrgetter
import sys
import os
#from menu import Menu

class  employee(person):
    """employee object subclassed from person"""
    def __init__(self,
                 eid=None,
                 firstname=None,
                 lastname=None,
                 suffix=None,
                 nickname=None,
                 sex=None,
                 dob=None,
                 payroll_id=None,
                 db_handle=None):
        """Create new instanace of employee"""
        person.__init__(self,
                        firstname=firstname,
                        lastname=lastname,
                        suffix=suffix,
                        nickname=nickname,
                        sex=sex,
                        dob=dob,
                        db_handle=db_handle)
        self.eid = eid
        self.payroll_id=payroll_id
        self.shifts = []
    
    def __repr__(self):
        return "Employee - %s, db=%s, pythonID: %s" % (self.name(), self.db_handle.owner, id(self))

    def __str__(self):
        return "Employee - %s, db=%s" % (self.name(), self.db_handle.owner)
           
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : New Class
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
    
    # shouold this be a shifts object? 
    def append_shift(self, shift):
        self.shifts.append(shift)
        self.sort()
    
    def load_emp_db(self):
        if self.eid:
            result = self.db_handle.fetchdata('get_employee', [self.eid])
            for r in result:
                self._firstname = r[1]
                self._lastname = r[2]
                self._nickname = r[4]
                self._suffix = r[3]
                self.DOB.set_date(r[5])

    def save_emp_db(self, options=None):
        if eid:    
            R = self.db_handle.fetchdata('update_employee',[self.eid,
                                                            self.firstname(),
                                                            self.lastname(),
                                                            self.suffix(),
                                                            self.nickname(),
                                                            self.dob.date(),
                                                            self.phone_cell.number(),
                                                            self.sex])
        else:
            R = self.db_handle.fetchdata('Add_employee', [self.firstname(),
                                                          self.lastname(),
                                                          self.suffix(),
                                                          self.nickname(),
                                                          self.dob.date(),
                                                          self.phone_cell.number(),
                                                          self.sex])
        
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
        
    def __len__(self):
        return len(self.elist)
    
    def __repr__(self):
        return "Employees - %s, db=%s, pythonID: %s" % (len(self.elist), self.db_handle.owner, id(self))

    def __str__(self):
        return "Employees - %s, db=%s" % (len(self.elist), self.db_handle.owner)
    
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

    def find_name(self, options=None):
        os.system('clear')
        p = person(db_handle=self.db_handle)
        if len(options[2])==0:
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
        result = self.db_handle.fetchdata('get_employee', [p.firstname(), p.lastname(), ])
        self.load_from_db(result)
                
    def load_from_db(self, results):
        """Load employee list with results form a query"""
        for r in results:
            if self.check_id(r[0])==None:
                e = employee(eid=r[0], firstname=r[1], lastname=r[2], db_handle=self.db_handle)
                e._suffix = r[3]
                e._nickname = r[4]
                e.DOB.set_date(r[5])
                e.sex = r[6]
                self.append(e)

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
    
    def list_availability(self, sid):
        results = self.db_handle.fetchdata('list_available', [sid,])
        self.load_from_db(results)
        
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='employee.py - init_employee')
        self.db_handle = db_handle


    def sort(self):
        firstname = sorted(self.elist, key=attrgetter('_firstname'))
        self.elist = sorted(self.elist, key=attrgetter('_lastname'))
        #print(len(firstname))
    
if __name__ == "__main__":
    db_handle = database(owner='employee.py - __main__')
    E = employees(db_handle=db_handle)
#   M = menu('Employee Menu', db_handle=db_handle)
#    M.menu_display = self.print_menu
    E.set_name()
    E.DOB.get_date()
    print(E.DOB.age())
    E.print_self()
    print(E)
    #E
    #print(E.name())