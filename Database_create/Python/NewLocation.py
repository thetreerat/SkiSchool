# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from location import location

class  NewLocation(location):
    """NewLocation"""
    def __init__(self,
                 location_name=None,
                 location_size=None,
                 start_range=1,
                 end_range=10,
                 prefix=None,
                 db_handle=None):
        """Create New Instanace of NewLocation"""
        self.set_db_handle(db_handle)
        location.__init__(self, location_name=location_name, location_size=location_size, db_handle=db_handle)
        self.startrange = start_range
        self.endrange =end_range
        self.prefix = prefix
        self.count = None

        self.Menu = Menu('New Location Menu', db_handle=self.db_handle)

    def __str__(self):
        return "NewLocation: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "NewLocation: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))

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
    
    def add_group_db(self):
        for x in range(int(self.startrange), int(self.endrange) + 1):
            if self.prefix==None:
                self.prefix=''
            self.location_name = """%s%s""" % (self.prefix,x)
            self.add_location_db()
            print(self.location_name)

    def Edit_NewLocation(self, options=None):
        raw_input('No working code for this option: ')
    
    def menu(self, options=None):
        M = self.Menu
        M.title = 'New Location Menu'
        M.add_item('Name', 'Name <string> - Edit location name.', self.Edit_NewLocation)
        M.add_item('Size', 'SIZE <string> - Edit location size description.', M.print_new)
        M.add_item('Prefix', 'PREFIX <string> - Edit Prefix for creating a range of New Locations', M.print_new)
        M.add_item('Start', 'Start <#> - Edit the starting point for the new locations range', M.print_new)
        M.add_item('End', 'End <#> - Edit the ending point for the new locations range', M.print_new)
        M.menu_display = self.print_menu
        M.Menu()
        
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

    def print_menu(self):
        print("""    -------------- --------------------------
    Location Name: %s
    Location Size: %s
    Prefix:        %s
    Start Range:   %s
    End Range:     %s
    -----------------------------------------""" % (self.location_name,
                                                    self.location_size,
                             self.prefix,
                             self.startrange,
                             self.endrange))
        
    def print_self(self):
        print("""    %s %s %s %s %s %s""" % str(count).ljust(6),
                                            self.location_name.ljust(30),
                                            self.location_size.ljust(33),
                                            self.prefix.ljust(7),
                                            str(self.startrange).ljust(12),
                                            str(self.endrange).ljust(7))
        
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='NewLocation')
        self.db_handle = db_handle
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : NewLocation
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
        




if __name__ == "__main__":
    from login import Login
    L = Login()
    L.Login()
    N = NewLocation(db_handle=L.db_handle)
    N.menu()
    N.About()