# Author: Harold Clark
# Copyright Harold Clark 2019
#
import psycopg2
import sys
import os
from database import database
from menu import Menu
from employee import employee

class Location(object):
    """location class object """
    def __init__(self,
                 lid=None,
                 location_name=None,
                 location_size=None,
                 elist=None,
                 notes=None,
                 lock_sn=None,
                 lock_combination=None,
                 db_handle=None):
        self.lid = lid
        self._location_name = location_name
        self._location_size = location_size
        self._lock_sn = lock_sn
        self._lock_combination = lock_combination
        self.elist = elist
        self._notes = notes
        if db_handle==None:
            db_handle = database(owner='location.py - location')
        self.db_handle = db_handle
        
    def add_location_db(self, options=None):
        """Add a location to the database"""
        result = self.db_handle.fetchdata('add_location', [self.location_name,self.location_size,self.notes,])
        self.lid = result[0][0]
                    
    def edit_location(self):
        M = Menu(db_handle=self.db_handle)
        M.menu_display = self.print_location
        M.add_item('Assign', 'ASSIGN <eid> - assgin employee to location by Employee ID', self.assign_location)
        M.add_item('End', 'END  - assgin end for range for new locations group', self.set_end)
        M.add_item('Prefix', 'PREFIX <string> - Enter location prefix for new locations group', self.set_prefix)
        M.add_item('Name', 'NAME', self.set_location_name)
        M.add_item('Size' 'SIZE <string> - Enter location size description', self.set_size)
        M.add_item('Start', 'START <#> - Enter the Start for range for New Locker Group', M.print_new)
        
    def get_location_name(self, options=None):
        if len(options[2])>0:
            d = " ".join(options[2])
        else:
            d = raw_input("""Enter Location Name (%s)""" % (self.location_name))
        self.set_location_name(d)                   

    def get_location_size(self, options=None):
        if options[2]>0:
            size = " ".join(options[2])
        else:
            size = raw_input('Enter Size of location: ')
        self.set_location_size(size)
        
    def load_location_db(self, options=None):
        if self.lid:
            R = self.db_handle.fetchdata('get_location', [self.lid,])
            r = R[0]
            self.set_location_name(r[0])
            self.set_location_size(r[2])
            self._lock_sn = r[4]
            self._notes = r[3]
            self._lock_combination = r[5]
                
    def location_name(self, pad=20):
        if self._location_name:
            return self._location_name.ljust(pad)
        else:
            return "".ljust(pad)
        
    def location_size(self, pad=20):
        if self._location_size:
            return self._location_size.ljust(pad)
        else:
            return "".ljust(pad)
        
    def lock_sn(self, pad=10):
        if self._lock_sn:
            return self._lock_sn.ljust(pad)
        else:
            return "".ljust(pad)
    
    def lock_combination(self, pad=10):
        if self._lock_combination:
            return self._lock_combination.ljust(pad)
        else:
            return ''.ljust(pad)
    
    def menu(self, options=None):
        M = Menu('Edit Location Menu', db_handle=self.db_handle)
        M.menu_display = self.print_Menu
        
        #M.add_item('End', 'END  - assgin end for range for new locations group', self.set_end)
        #M.add_item('Prefix', 'PREFIX <string> - Enter location prefix for new locations group', self.set_prefix)
        M.add_item('Name', 'NAME', self.set_location_name)
        M.add_item('Size' 'SIZE <string> - Enter location size description', self.set_size)
        #M.add_item('Start', 'START <#> - Enter the Start for range for New Locker Group', M.print_new)
        M.add_item('Save', 'SAVE - Save updates to database', M.print_new)
        M.Menu
    
    def set_location_name(self, name):
        if name!=self.location_name and name!='':
                self._location_name = name
            
    def set_location_size(self, size):
        if size!=self._location_size and size!='':
            self._location_size = size                   
   
    def print_menu(self):
        pass
    
    def print_self(self, count=None):
        if count:
            print("""    %s %s %s %s %s""" % (count, self.location_name(), self.location_size(), self.lock_sn(), self.lock_combination()))
        else:
            print("""    %s %s %s %s %s""" % (str(self.lid).ljust(5),
                                              self.location_name(17),
                                              self.location_size(18),
                                              self.lock_sn(10),
                                              self.lock_combination(10)))
            
            
    def print_location(self, list_type, count=None):
        if list_type=='Short':
            if count:
                print ("""  %s %s %s %s""" % (str(count).ljust(4),
                                              str(self.lid).ljust(4),
                                              self.location_name(30),
                                              self.location_size(10)))
            else:
                print ("""    %s %s %s""" % (str(self.lid).ljust(4),
                                             self.location_name(30),
                                             self.location_size(10)))
                
        
if __name__ == '__main__':
    from login import Login
    l = Login()
    l.Login()
    #raw_input(l.db_handle)
    #D = database(owner='main')
    #L = locations(db_handle=D, eid=15)
    L = locations(db_handle=l.db_handle, eid=112)
    #L.get_locations_free()
    L.get_locations_employee_db()
    #print(L.eid.name())
    #L.print_employee_menu()
    L.menu_employee()
    
    