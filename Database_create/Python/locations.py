# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from location import Location
from employee import employee


class  Locations(object):
    """Locations"""
    Location.index = 1
    Location.object = 2
    Location.id = 3

    def __init__(self, db_handle=None, eid=None):
        """Create New Instanace of Locations"""
        self.set_db_handle(db_handle)
        self.locations = []
        self.Menu = Menu('', db_handle=self.db_handle)
        self.eid = employee(eid=eid, db_handle=self.db_handle)
        self.eid.load_emp_db()

        
    
    def __str__(self):
        return "Locations: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Locations: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def __len__(self):
        return len(self.locations)
    
    def append(self, location):
        self.locations.append(location)
        self.sort()

    def add(self, options=None):
        n = NewLocation()
        n.add_group()
        L.llist.append(n)
        
    def assign_location(self, options=None):
        if self.eid.eid:
            if options[1]:
                lid = options[1]
            else:
                lid = None
                while not lid:
                    try:
                        lid = int(raw_input('Enter Location ID: '))
                    except:
                        lid = None            
            r = self.db_handle.fetchdata('is_location_available', [lid,])
            if r[0]:
                e = employee(eid=r[0])
                e.load_emp_db()
                a = raw_input('reassign from %s to %s (YES/NO)' % (e.name(), self.eid.name())).upper()
                if not a[0]=='Y':
                    return
            self.db_handle.fetchdata('assign_location', [self.eid.eid, lid])
            
    def checkID(self, ID, return_type=Location.object):
        i = 0
        for c in self.location:
            if c.ID==ID:
                if return_type==Location.index:
                    return i
                elif return_type==Location.object:
                    return t
            i += 1
        return None

    def clear(self):
        self.llist = []
    
    def get_locaitons_available_db(self):
        R = self.db_handle.fetchdata('list_available_location', [])
        for r in R:
            l = Location(lid=r[1],
                         location_name=r[3],
                         location_size=r[4])
            l.eid = employee(eid=r[2])
            l.eid._firstname = [5]
            l.eid._lastname = r[6]
            self.append(l)
    
    def get_locations_employee_db(self):
        """get loactions assigned to an employee"""
        if self.eid:
            self.clear()
            result = self.db_handle.fetchdata('get_locations_for_eid', [self.eid.eid,])
            for r in result:
                l = Location(lid=r[2],
                             location_name=r[0],
                             location_size=r[1],
                             db_handle=self.db_handle)
                self.append(l)
                
    def menu(self):
        M = self.Menu
        M.menu_display = self.print_menu
        M.add_item('Assign', 'ASSIGN <eid> - assgin employee to location by Employee ID', self.assign_location)
        M.add_item('Edit', 'EDIT <lid> - load Edit menu for <id> location', M.print_new)
        M.add_item('Add', 'ADD - Add new locations', M.print_new)
        M.Menu()
                
    def print_menu(self):
        print('')
        print("""    LID   Location Name     Location Size     Lock SN     Lock Combination
    ----- ----------------- ----------------- ----------- ----------------------""")
        self.print_list()
        print("""    ----------------------------------------------------------------------------
    Count: %s""" % (len(self)))
            
    def print_list(self):
        i = 0
        for c in self.locations:
            c.print_self()
            i=+1
        
    def sort(self):
        self.locations = sorted(self.locations, key=self.sort_key_location_name)
    
    def sort_key_location_name(self, i):
        return i.location_name
    
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Locations
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Locations.py - __init__')
        self.db_handle = db_handle
        
        

if __name__ == "__main__":
    #from instructor import instructor
    #from instructor import instructors
    from login import Login
    #db_handle=database(owner='Locations.py - __main__')
    #I = instructor(eid=15, db_handle=db_handle)
    #I.get_emp_db()
    #list = instructors(db_handle)
    #list.append(I)
    
    #options = ['EDIT', 15, [], db_handle]
    #list.edit(options)
    #I.print_menu()
    #list.ilist[0].print_instructor('Long')
    L = Login()
    L.Login()
    N = Locations(db_handle=L.db_handle)
    #N.eid.load_emp_db()
    #N.get_locations_employee_db()
    N.get_locaitons_available_db()
    #N.print_menu()
    N.menu()
    #N.menu()
    #N.About()