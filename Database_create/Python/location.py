# Author: Harold Clark
# Copyright Harold Clark 2019
#
import psycopg2
import sys
import os
from database import database

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
        
    def add_location_db(self):
        """Add a location to the database"""
        result = self.db_handle.fetchdata('add_location', [self.location_name,self.location_size,self.notes,])
        self.lid = result[0][0]
    
    def assign_location_db(self, eid):
        """Assign location to instructor in database"""
        result = self.db_handle.fetchdata('assign_location', [eid, self.lid])
            
    def edit_location(self):        
        Edit=True
        while Edit:
            self.print_location('Long')
            answer = raw_input('Please enter Selection: ').upper()
            answer = list(answer.split())
            while answer:
                if answer[0] in ['RETURN', 'RETUR','RETU','RET','RE' ]:
                    Edit = False
                    break

                elif answer[0] in ['ASSIGN','ASSIG','ASSI','ASS','AS', 'A']:
                    eid = raw_input('Enter EID: ')
                    self.assign_location_db(eid)
                    break
                elif answer[0]=='E':
                    answer = raw_input('EXIT or END? ').upper()
                    answer = list(answer.split())

                elif answer[0] in ['END', 'EN']:
                    end = raw_input("""Enter End Range (%s)""" % (self.endrange))
                    if end!=self.endrange and end!='':
                        self.endrange = end
                    break

                elif answer[0] in ['EXIT','EX','EXI']:
                    sys.exit(1)

                elif answer[0] in ['NAME','NAM','NA','N']:
                    d = raw_input("""Enter Location Name (%s)""" % (self.location_name))
                    if d!=self.location_name and d!='':
                        self.location_name = d                   
                    break

                elif answer[0] in ['PREFIX','PREFI','PREF','PRE','PR','P']:
                    d = raw_input("""Enter Prefix (%s)""" % (self.prefix))
                    if d!=self.prefix and d!='':
                        self.prefix = d                   
                    break

                elif answer[0]=='S':
                    answer = raw_input('START or SIZE? ').upper()
                    answer = list(answer.split())    

                elif answer[0] in ['SIZE','SIZ','SI']:
                    d = raw_input("""Enter Location Name (%s)""" % (self.location_size))
                    if d!=self.location_size and d!='':
                        self.location_size = d                   
                    break

                elif answer[0] in ['START','STAR','STA','ST']:
                    d = raw_input("""Enter Start Range (%s)""" % (self.startrange))
                    if d!=self.startrange and d!='':
                        self.startrange = d
                    break

                else:
                    print("""Lost in space!!!""")
                    print(answer)
                    dump = raw_input('ready?')
                    break
                                
    def pad(self, item, length):
        """depricated fundton use ljust """
        if item==None:
            item=''
        length = length - len(item)
        pad = item
        for l in range(length):
            pad = pad + chr(32)
        return pad

    def print_location(self, list_type, count=None):
        if list_type=='short':
            print("""    %s %s %s""" % (self.pad(str(count), 6),
                                             self.pad(self.location_name,30),
                                             self.pad(self.location_size,33)
                                             ))
        elif list_type=='Employee':
            print("""    %s %s %s """ % (self.pad(str(self.lid), 6),
                                         self.pad(self.location_name, 33),
                                         self.location_size))

        elif list_type=='Long':
            os.system('clear')
            
            print("""    Edit New Location Group
    -------------- --------------------------
    Location Name: %s
    Location Size: %s
    -------------- --------------------------
    NAME   - Edit location Name
    SIZE   - Edit Location Size
    ASSIGN - Assign Location to employee
    RETURN - Return to prevois Menu
    EXIT   - Exit to system Prompt
    -----------------------------------------
""" % (self.location_name,
                             self.location_size,
                             self.prefix,
                             self.startrange,
                             self.endrange))
            
            
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
            print("""    %s %s %s %s %s %s""" % (self.pad(str(count), 6),
                                             self.pad(self.location_name,30),
                                             self.pad(self.location_size,33),
                                             self.pad(self.prefix,7),
                                             self.pad(str(self.startrange),12),
                                             self.pad(str(self.endrange), 7)))
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
    def __init__(self, db_handle=None):
        """init object """
        self.llist = []
        if db_handle==None:
            db_handle = database('location.py - locations')
        self.db_handle = db_handle
        
    def clear(self):
        self.llist = []
    
    def get_locations_employee_db(self, eid):
        """get loactions assigned to an employee"""
        result = self.db_handle.fetchdata('get_locations_for_eid', [eid])
        for r in result:
            l = location(lid=r[2],
                         location_name=r[0],
                         location_size=r[1],
                         db_handle=self.db_handle)
            self.llist.append(l)        
    
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
        #print(len(self.llist))
        
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
    
    def New_Menu(self, call_from=None):
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

from instructor import instructor 
from instructor import instructors
        
if __name__ == '__main__':
    L = locations()
    #L.get_locations_free()
    L.get_locations_employee_db(15)
    L.New_Menu(call_from='short')
    
    