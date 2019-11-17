# Author: Harold Clark
# Copyright Harold Clark 2019
#
import psycopg2
import sys
import os
from database import database
from menu import Menu
from employee import employee

class location(object):
    """locatoin class object """
    def __init__(self,
                 lid=None,
                 location_name=None,
                 location_size=None,
                 elist=None,
                 notes=None,
                 db_handle=None):
        self.lid = lid
        self.location_name = location_name
        self.location_size = location_size
        self.elist = elist
        self.notes = notes
        if db_handle==None:
            db_handle = database(owner='location.py - location')
        self.db_handle = db_handle
        
    def add_location_db(self, options=None):
        """Add a location to the database"""
        result = self.db_handle.fetchdata('add_location', [self.location_name,self.location_size,self.notes,])
        self.lid = result[0][0]
        
    def assign_location(self, options=None):
        if options[1]:
            eid = options[1]
        else:
            eid = raw_input('Enter EID: ')
        self.assign_location_db(eid)
        
    def assign_location_db(self, eid):
        """Assign location to instructor in database"""
        result = self.db_handle.fetchdata('assign_location', [eid, self.lid])
            
    def edit_location(self):
        M = Menu(db_handle=self.db_handle)
        M.menu_display = self.print_location
        M.add_item('Assign', 'ASSIGN <eid> - assgin employee to location by Employee ID', self.assign_location)
        M.add_item('End', 'END  - assgin end for range for new locations group', self.set_end)
        M.add_item('Prefix', 'PREFIX <string> - Enter location prefix for new locations group', self.set_prefix)
        M.add_item('Name', 'NAME', self.set_location_name)
        M.add_item('Size' 'SIZE <string> - Enter location size description', self.set_size)
        M.add_item('Start', 'START <#> - Enter the Start for range for New Locker Group', M.print_new)
    
    def set_end(self, options=None):
        if options[1]:
            end = options[1]
        else:
            end = raw_input("""Enter End Range (%s)""" % (self.endrange))
        if end!=self.endrange and end!='':
            self.endrange = end
                            
    def set_location_name(self, options=None):
        d = raw_input("""Enter Location Name (%s)""" % (self.location_name))
        if d!=self.location_name and d!='':
            self.location_name = d                   

    def set_prefix(self, options=None):
        #if options[2]:
        raw_input(options)    
        d = raw_input("""Enter Prefix (%s)""" % (self.prefix))
        if d!=self.prefix and d!='':
            self.prefix = d
            
    def set_size(self, options=None):
        d = raw_input("""Enter Location Name (%s)""" % (self.location_size))
        if d!=self.location_size and d!='':
            self.location_size = d                   

    def set_start(self, options=None):
        d = raw_input("""Enter Start Range (%s)""" % (self.startrange))
        if d!=self.startrange and d!='':
            self.startrange = d
    
    def print_location(self, list_type, count=None):
        if list_type=='Short':
            if count:
                print ("""  %s %s %s %s""" % (str(count).ljust(4),
                                              str(self.lid).ljust(4),
                                              self.location_name.ljust(30),
                                              self.location_size.ljust(10)))
            else:
                print ("""    %s %s %s""" % (str(self.lid).ljust(4),
                                             self.location_name.ljust(30),
                                             self.location_size.ljust(10)))
                
class NewLocation(location):
    """class object based on location for loading groups of New locations"""
    def __init__(self,
                 location_name=None,
                 location_size=None,
                 start_range=1,
                 end_range=10,
                 prefix=None,
                 db_handle = None):
        if db_handle==None:
            db_handle=database(owner='location.py - NewLocation')
        location.__init__(self, location_name=location_name, location_size=location_size, db_handle=db_handle)
        self.startrange = start_range
        self.endrange =end_range
        self.prefix = prefix
        self.count = None
        
    def add_group_db(self):
        for x in range(int(self.startrange), int(self.endrange) + 1):
            if self.prefix==None:
                self.prefix=''
            self.location_name = """%s%s""" % (self.prefix,x)
            self.add_location_db()
            print(self.location_name)
        
    def add_group(self):
        self.location_size = raw_input('Enter location Size: ')
        prefix = raw_input("""Enter Prefix (%s): """ % (self.prefix))
        if prefix!=None:
            self.prefix = prefix
        startrange = raw_input("""Eneter Start Range (%s): """ % (self.startrange))
        if startrange!='':
            self.startrange = startrange
        endrange = raw_input("""Enter End Range (%s): """ % (self.endrange))
        if endrange!='':
            self.endrange = endrange
    
    def print_location(self, list_type,count=None):
        if list_type=='New':
            print("""    %s %s %s %s %s %s""" % str(count).ljust(6),
                                             self.location_name.ljust(30),
                                             self.location_size.ljust(33),
                                             self.prefix.ljust(7),
                                             str(self.startrange).ljust(12),
                                             str(self.endrange).ljust(7))
        elif list_type=='Long':
            os.system('clear')
            
            print("""    Edit New Location Group
    -------------- --------------------------
    Location Name: %s
    Location Size: %s
    Prefix:        %s
    Start Range:   %s
    End Range:     %s
    -------------- --------------------------
    NAME   - Edit location Name
    SIZE   - Edit Location Size
    PREFIX - Edit Prefix
    START  - Edit Start Range
    END    - Edit End Range
    RETURN - Return to prevois Menu
    EXIT   - Exit to system Prompt
    -----------------------------------------
""" % (self.location_name,
                             self.location_size,
                             self.prefix,
                             self.startrange,
                             self.endrange))

    
class locations(object):
    """class object for holding location objects"""
    def __init__(self, db_handle=None, eid=None):
        """init object """
        self.llist = []
        self.set_db_handle(db_handle)
        self.eid = employee(eid=eid)
        self.eid.load_emp_db()
    
    def __len__(self):
        return len(self.llist)
    
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
                    
        
    def clear(self):
        self.llist = []
    
    def get_locations_employee_db(self):
        """get loactions assigned to an employee"""
        if self.eid:
            self.clear()
            result = self.db_handle.fetchdata('get_locations_for_eid', [self.eid.eid,])
            for r in result:
                l = location(lid=r[2],
                             location_name=r[0],
                             location_size=r[1],
                             db_handle=self.db_handle)
                self.llist.append(l)        

    def menu_new(self, call_from=None):
        """Menu loop for New locations """
        run=True
        while run:
            L.print_new_location_menu(call_from=call_from)
            answer = raw_input('Please enter Selection: ').upper()
            answer = list(answer.split())
            while answer:
                if answer[0] in ['RETURN', 'RETUR','RETU','RET','RE' ]:
                    run = False
                    break
                
                elif answer[0] == 'A':
                    answer = raw_input('ADD or ASSIGN? ')
                    answer = list(answer.split())
                    
                elif answer[0] in ['ADD', 'AD']:
                    n = NewLocation()
                    n.add_group()
                    L.llist.append(n)
                    break
                
                elif answer[0] in ['ASSIGN','ASSIG','ASSI','ASS','AS']:
                    if len(answer)==2:
                        line = int(answer[1])
                        eid = int(raw_input('Enter EID: '))
                    elif len(answer)==1:
                        line = int(raw_input('Enter line number: '))
                        eid = int(raw_input('Enter EID: '))
                    elif len(answer)==3:
                        line = int(answer[1])
                        eid = int(answer[2])
                    L.llist[line].assign_location_db(eid)
                    break
                
                elif answer[0]=='E':
                    answer = raw_input('EXIT or EDIT #? ').upper()
                    answer = list(answer.split())
                elif answer[0] in ['EDIT','ED','EDI']:
                    if len(answer)==1:
                        break
                    L.llist[int(answer[1])].edit_location()
                    break
                elif answer[0] in ['EXIT','EX','EXI']:
                    sys.exit(1)
                elif answer[0] in ['LOAD','LOA','LO','L']:
                    L.llist[0].add_group_db()
                    dump = raw_input('ready?')
                    break
                else:
                    print("""Lost in space!!!""")
                    print(answer)
                    dump = raw_input('ready?')
                    break 
    
    def menu_employee(self, options=None):
        M = Menu('Employee Locations Menu', self.db_handle)
        M.menu_display = self.print_employee_menu
        M.add_item('Free', 'FREE <lid> - Return location to avaliable list', M.print_new)
        M.add_item('Find', 'FIND  - Find an avaliable location to assign', M.print_new)
        M.add_item('Assign', 'ASSIGN <LID> - assign a location ID to emplpoyee', self.assign_location) 
        M.Menu()
    
    def print_employee_menu(self):
        print("""    Lid   Location Name                      Location Size
    ----- ---------------------------------- -----------------""")
        for l in self.llist:
            l.print_location('Short')
        print("""    ----------------------------------------------------------
    count %s""" % (len(self)))
        
    def print_list(self, call_from='New'):
        """print list of locations """
        if call_from=='Employee':
            print("""
    Lid   Location Name                      Location Size
    ----- ---------------------------------- -----------------""")
        count = 0
        for l in self.llist:
            l.print_location(call_from, count)
            count+= 1
        if call_from=='Employee':
            print("""    ----------------------------------------------------------""")
            
    def get_locations_free(self, size=None):
        if size==None or size=='ALL':
            result = self.db_handle.fetchdata('list_available_location', [])
        else:
            result = self.db_handle.fetchdata('list_available_location', [size,])
        for r in results:
            e = instructor(eid=r[2], db_handle=self.db_handle)
            e.firstname = r[5]
            e.lastname=r[6]
            E = instructors(db_handle=self.db_handle)
            E.ilist.append(e)
            l = location(lid=r[1],
                         location_name=r[3],
                         location_size=r[4],
                         elist=E,
                         db_handle=self.db_handle)
            self.llist.append(l)
        
        
    def print_new_location_menu(self, call_from='New'):
        os.system('clear')
        if call_from=='short':
            assign = """    ASSIGN - Assign location to employee"""
        else:
            assign = """    ADD    - Add a Group
    EDIT   - Edit a Group Line
    LOAD   - Load Locations into Database"""
        print("""        New Location Group Menu
              
    Line # Location Name                  Location Size                     Prefix  Start Range  End Range
    ------ ------------------------------ --------------------------------- ------- ------------ ----------""")
        self.print_list(call_from=call_from)
        print("""    ------ ------------------------------ --------------------------------- ------- ------------ ----------
%s
    RETURN - Return to Previous Menu
    EXIT   - Exit to system prompt""" % (assign))
    

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database('location.py - locations __init__')
        self.db_handle = db_handle
        
#from instructor import instructor 
#from instructor import instructors
        
if __name__ == '__main__':
    from login import Login
    l = Login()
    l.Login()
    #raw_input(l.db_handle)
    #D = database(owner='main')
    #L = locations(db_handle=D, eid=15)
    L = locations(db_handle=l.db_handle, eid=15)
    #L.get_locations_free()
    L.get_locations_employee_db()
    print(len(L))
    L.print_employee_menu()
    L.menu_employee()
    
    