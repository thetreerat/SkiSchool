# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from date import date
from menu import Menu

class  ExtraDaysTemplate(object):
    """extradaystemplate"""
    def __init__(self,
                 et=None,
                 title=None,
                 extra_date=None,
                 points=None,
                 ideal_max=None,
                 db_handle=None):
        """Create New Instanace of New Class"""
        self.set_db_handle(db_handle)
        self.et = et
        self.title = title
        self.extra_date = date(date=extra_date, db_handle=self.db_handle)
        self.points = points
        self.ideal_max = ideal_max
        self.update = False
        self.Menu = Menu('Extra Days Template', db_handle=self.db_handle)
    
    def __str__(self):
        return "extradaystemplate: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "extradaystemplate: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def get_title(self, options=None):
        self.title = raw_input('Enter Title: ')
        self.set_update(True)

    def menu(self):
        M = self.Menu
        M.menu_display = self.print_menu
        M.add_item('Title', 'TITLE <VALUE> - set title for extra day', self.get_title)
        M.add_item('Date', 'DATE <DATE> - set date for extra day', M.print_new)
        M.add_item('Points', 'POINTS <VALUE> - Set Points value for extra day', M.print_new)
        M.add_item('Max', 'MAX <VALUE> - Set the maximum ideal number of instructors', M.print_new)
        if self.update:
            M.add_item('Update', 'UPDATE - Update database with new values', M.print_new)
        M.Menu()
        
    def print_menu(self):
        print("""
    ID:        %s
    Title:     %s
    Date:      %s
    Points:    %s
    Ideal Max: %s""" % (str(self.et).ljust(4),
                                     self.title.ljust(40),
                                     self.extra_date.date(True),
                                     str(self.points).ljust(2),
                                     str(self.ideal_max).ljust(3)))
    
    def print_self(self):
        print("""    %s %s %s %s %s""" % (str(self.et).ljust(4),
                                     self.title.ljust(40),
                                     self.extra_date.date(True),
                                     str(self.points).ljust(2),
                                     str(self.ideal_max).ljust(3)))

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='extradaystemplate')
        self.db_handle = db_handle    

    def set_update(self, value):
        if value:
            if not self.update:
                M = self.Menu
                M.add_item('Update', 'UPDATE - Update database with changes', M.print_new)
        self.update = value
            
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : extradaystemplate
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")

        


if __name__ == "__main__":
    db_handle = database(owner='extradaystemplate.py - __main__')
    N = ExtraDaysTemplate(db_handle=db_handle, title='Christmas Day', extra_date='12/25/2019', et=1, points=2, ideal_max=5)
    N.menu()
    #N.print_self()
    #N.About()