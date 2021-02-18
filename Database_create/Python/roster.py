# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from employee import employee
from attendee import Attendee

class  Roster(object):
    """Roster"""
    employee.index = 1
    employee.object = 2
    employee.id = 3

    def __init__(self, tlid=None, db_handle=None):
        """Create New Instanace of Roster"""
        self.set_db_handle(db_handle)
        self.tlid = tlid
        self.employees = []
        self.Menu = Menu('Roster List', db_handle=self.db_handle)
        
    
    def __str__(self):
        return "Roster: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Roster: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def __len__(self):
        return len(self.employees)
    
    def add_eid(self, options=None):
        
        eid = None
        if options[1]:
            eid = options[1]
        else:
            while not eid:
                try:
                    eid = (raw_input('Enter Employee ID: '))
                    eid = int(eid)
                except:
                    if eid=='':
                        return
                    else:
                        eid = None
        e = employee(eid=options[1], db_handle=self.db_handle)
        e.load_emp_db()
        self.append(e)
        if self.tlid:
            e.rid = self.db_handle.fetchdata('add_eid_roster',[self.tlid, eid, ''])
        
    def append(self, employee):
        self.employees.append(employee)
        self.sort()
        
    def checkID(self, rid, return_type=employee.object):
        i = 0
        for c in self.employees:
            if c.rid==rid:
                if return_type==employee.index:
                    return i
                elif return_type==employee.object:
                    return c
            i += 1
        return None
    
    def clear(self):
        self.employees = []
        
    def delete_rid(self, options=None):
        if options[1]:
            rid=options[1]
        else:
            try:
                rid = int(raw_input('Enter RID to delete:'))
            except:
                return 0
        R = self.db_handle.fetchdata('delete_rid_training_roster',[rid, self.tlid])
        
    def edit_rid(self, options=None):
        if options[1]:
            rid = options[1]
        else:
            try:
                rid = int(raw_input('Enter RID: '))
            except:
                return 1
        A = self.checkID(rid, employee.object)
        if A:
            A.menu()
                
    def get_employees_db(self):
        if self.tlid:
            R = self.db_handle.fetchdata('list_training_roster', [self.tlid,])
            for r in R:
                e = Attendee(rid=r[0],
                             eid=r[2],
                             tlid=r[1],
                             notes=r[3],
                             db_handle=self.db_handle)
                e.load_emp_db()
                self.append(e)
                
    def menu(self):
        M = self.Menu
        M.menu_display = self.print_menu
        M.add_item('Add', 'ADD <eid> - Add employee to roster', self.add_eid)
        M.add_item('Edit', 'EDIT <rid> - edit note', self.edit_rid)
        M.add_item('Delete', 'DELETE <rid> - delete record', self.delete_rid)
        M.Menu()
                
    def print_menu(self):
        self.clear()
        self.get_employees_db()
        print("""
    TLID  RID   EID   Name                    Notes
    ----- ----- ----- ----------------------- ------------------------------""")
        self.print_list()
        print("""    ------------------------------------------------------------------------""")
        print("    Count: %s" % (len(self)))
            
    def print_list(self):
        i = 1
        for c in self.employees:
            #print ('    %s %s %s' % (str(i).ljust(5), str(c.eid).ljust(5), c.name(nickname=True).ljust(30)))
            c.print_self()
            i=+1
        
    def sort(self):        
        name = sorted(self.employees, key=self.sort_key_firstname)
        self.employees = sorted(name, key=self.sort_key_lastname)

    def sort_key_lastname(self,i):
        return i.lastname()
    
    def sort_key_firstname(self, i):
        return i.firstname()
    
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Roster
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Roster')
        self.db_handle = db_handle
        
        


if __name__ == "__main__":
    from login import Login
    L = Login(login='halc')
    L.Login()
    N = Roster(db_handle=L.db_handle, tlid=1)
    N.get_employees_db()
    #N.print_list()
    N.menu()
    #N.About()