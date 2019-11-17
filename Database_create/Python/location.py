# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu

class  Location(object):
    """Location"""
    def __init__(self,
                 lid=None,
                 location_name=None,
                 location_size=None,
                 notes = None,
                 lock_sn = None,
                 lock_combination = None,
                 db_handle=None):
        """Create New Instanace of New Class"""
        self.set_db_handle(db_handle)
        self.lid = lid
        self.location_name = location_name
        self.location_size = location_size
        self.notes = notes
        self.lock_sn = lock_sn
        self.lock_combination =lock_combination
        self.Menu = Menu('lid Menu', db_handle=self.db_handle)
    
    def __str__(self):
        return "Location: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Location: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
        
    def load_location_db(self):
        """ """
        if self.lid:
            R = self.db_handle.fetchdata('get_location', [self.lid,])
            r = R[0]
            self.location_name = r[0]
            self.location_size = r[2]
            self.lock_sn = r[4]
            self.lock_combination = r[5]
            self.note = r[3]
            
    def menu(self, options=None):
        M = self.Menu
        #M.add_item('location_name', 'NAME <name> - edit Location name', M.print_new)
        #M.add_item('Size', 'SIZE <sting> - edit Location size', M.print_new)
        M.add_item('Notes', 'Notes - edit notes field', M.print_new)
        M.add_item('Combination', 'COMBINATION <string> - Edit Cobination field', M.print_new)
        M.add_item('Serial', 'SERIAL <string> - Edit serial number field', M.print_new)
        M.menu_display = self.print_menu
        M.Menu()
        
    def print_menu(self):
        print("""
    lid:              %s
    Name:             %s
    Size:             %s
    lock SN:          %s
    lock Combination: %s
    Notes:            %s""" % (self.lid,
                               self.location_name,
                               self.location_size,
                               self.lock_sn,
                               self.lock_combination,
                               self.notes))
        
    def print_self(self):
        print("""    %s %s %s %s %s %s %s""" % (self.lid,
                                                self.location_name,
                                                self.location_size,
                                                self.lock_sn,
                                                self.lock_combination,
                                                self.notes))
        
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Location')
        self.db_handle = db_handle
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Location
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
        


if __name__ == "__main__":
    db_handle=database(owner='Location.py - __main__')
    N = Location(lid=467, db_handle=db_handle)
    N.load_location_db()
    #N.print_menu()
    #N.location_name()
    N.menu()
    N.About()