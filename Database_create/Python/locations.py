# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from location import Location

class  Locations(object):
    """Locations"""
    Location.index = 1
    Location.object = 2
    Location.id = 3

    def __init__(self, db_handle=None):
        """Create New Instanace of Locations"""
        self.set_db_handle(db_handle)
        self.locations = []
        self.Menu = Menu('', db_handle=self.db_handle)
        
    
    def __str__(self):
        return "Locations: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Locations: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def __len__(self):
        return len(self.locations)
    
    def append(self, location):
        self.locations.append(location)
        self.sort()
        
    def checkID(self, ID, return_type=Locations.object):
        i = 0
        for c in self.location:
            if c.ID==ID:
                if return_type==Locations.index:
                    return i
                elif return_type==Locations.object:
                    return t
            i += 1
        return None

    def menu(self):
        M = self.Menu
        M.menu_display = self.print_menu
        M.add_item('Test', 'TEST - this is a place holder', M.print_new)
        M.Menu()
                
    def print_menu(self):
        print('Menu print needs info')
        print("-----------------")
        self.print_list()
        print("-----------------")
        print("    Count: %s" % (len(self)))
        
    
    def print_list(self):
        i = 0
        for c in self.locations:
            print ('    %s' % (i))
            i=+1
        
    def sort(self):
        self.locations = sorted(self.locations, key=self.sort_key_location_name)
    
    def sort_key_(self):
        return i.listsortkey
    
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
    db_handle=database(owner='Locations.py - __main__')
    N = Locations(db_handle=db_handle)
    N.menu()
    #N.About()