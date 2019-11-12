# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from extradaystemplate import ExtraDaysTemplate


class  ExtraDays(object):
    """ExtraDays"""
    def __init__(self, db_handle=None):
        """Create New Instanace of ExtraDays"""
        self.set_db_handle(db_handle)
        self.extradays = []
    
    def __str__(self):
        return "ExtraDays: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "ExtraDays: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def __len__(self):
        return len(self.extradays)
    
    def append(self, newListObject):
        self.extradays.append(newListObject)
        self.sort()
    
    def get_current_extra_days(self):
        result = self.db_handle.fetchdata('get_current_extra_days', [])
        for r in result:
            d = ExtraDaysTemplate(et=r[0],
                                  title=r[1],
                                  extra_date=r[2],
                                  points=r[3],
                                  ideal_max=r[4],
                                  db_handle=self.db_handle)
            self.append(d)
        
    def menu(self, options=None):
        M = Menu('Extra Days Menu', db_handle=self.db_handle)
        M.menu_display = self.print_menu
        M.add_item('Add', 'ADD - Add a new extra day to the current season ', M.print_new)
        M.add_item('Copy', 'COPY <SAID> - Copy a seasons extra days', M.print_new)
        M.add_item('Edit', 'EDIT <ET> - Edit an extra day', M.print_new)
        M.add_item('Delete', 'DELETE <ET> - remove an extra day', M.print_new)
        M.Menu()
        
    def print_list(self):
        for e in self.extradays:
            e.print_self()
    
    def print_menu(self):
        self.print_list()
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='ExtraDays.py - init')
        self.db_handle = db_handle
        
    def sort(self):
        self.extradays = sorted(self.extradays, key=self.sort_key_date)
        #secondsort = sorted(firstsort, key=self.sort_key_lastname)
        #self.extradays = sorted(secondsort, key=self.sort_key_fistname) 
    
    def sort_key_date(self, ExtraDay):
        return ExtraDay.extra_date.date()
    
    def sort_key_lastname(self, ExtraDay):
        return ExtraDay.lastname()
    
    def sort_key_firstname(self, ExtraDay):
        return ExtraDay.firstname()
    
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : ExtraDays
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")

        
        


if __name__ == "__main__":
    db_handle = database(owner='extradays.py - __main__')
    N = ExtraDays(db_handle=db_handle)
    #d = ExtraDaysTemplate(db_handle=db_handle, title='Christmas Eve', extra_date='12/24/2019', et=1, points=2, ideal_max=5)
    #N.append(d)
    N.get_current_extra_days()
    N.menu()