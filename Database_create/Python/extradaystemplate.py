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
                 booked=None,
                 db_handle=None):
        """Create New Instanace of New Class"""
        self.set_db_handle(db_handle)
        self.et = et
        self._day_title = title
        self._booked=booked
        self.extra_date = date(date=extra_date, db_handle=self.db_handle)
        self.points = points
        self.ideal_max = ideal_max
        self.update = False
        self.set_new()
        self.Menu = Menu('Extra Days Template', db_handle=self.db_handle)
    
    def __str__(self):
        return "extradaystemplate: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "extradaystemplate: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))    
    
    def add_db(self, options=None):
        results = self.db_handle.fetchdata('add_extra_days',
                                           [self.day_title(),
                                            self.extra_date.date(True),
                                            self.points,
                                            self.ideal_max,])
        self.et = results[0][0]
        self.set_new(False)
        self.set_update(False)
    
    def load_template_db(self, options=None):
        result = self.db_handle.fetchdata('get_extra_days_template', [self.et, ])
        r = result[0]
        self._day_title = r[1]
        self.extra_date.set_date(r[2])
        self.points = r[3]
        self.ideal_max = r[4]
        self._booked = r[5]
    
    def get_extra_date(self, options=None):
        self.extra_date.get_date(options)
        self.set_update(True)

    def get_ideal_max(self, options=None):
        if type(options[1]) is int:
            self.ideal_max = options[1]
        else:
            self.ideal_max = raw_input('Enter Ideal Max instructors: ')
        self.set_update(True)
        
    def get_points(self, options=None):
        if type(options[1]) is int:
            self.points = options[1]
        else:
            self.points = raw_input('Enter Point value: ')
        self.set_update(True)

    def get_title(self, options=None):
        self._day_title = raw_input('Enter Title: ')
        self.set_update(True)
    
    def menu(self, options=None):
        M = self.Menu
        M.menu_display = self.print_menu
        M.add_item('Title', 'TITLE <VALUE> - set title for extra day', self.get_title)
        M.add_item('Date', 'DATE <DATE> - set date for extra day', self.get_extra_date)
        M.add_item('Points', 'POINTS <VALUE> - Set Points value for extra day', self.get_points)
        M.add_item('Max', 'MAX <VALUE> - Set the maximum ideal number of instructors', self.get_ideal_max)
        M.Menu()

    def print_list_heading(self):
        print("""
    ET   Extra Day Name                           Date           Points  Ideal Max  Booked
    ---- ---------------------------------------- -------------- ------- ---------- -----------""")
        
    def print_menu(self):
        print("""
    ID:        %s
    Title:     %s
    Date:      %s
    Points:    %s
    Ideal Max: %s
    Booked   : %s""" % (str(self.et).ljust(4),
                     self.day_title().ljust(40),
                     self.extra_date.date(True),
                     str(self.points).ljust(2),
                     str(self.ideal_max).ljust(3),
                     str(self._booked).ljust(3)))
    
    def print_self(self):
        print("""    %s %s %s %s %s %s""" % (str(self.et).ljust(4),
                                     self._day_title.ljust(40),
                                     self.extra_date.date(True).ljust(14),
                                     str(self.points).ljust(7),
                                     str(self.ideal_max).ljust(10),
                                     str(self._booked).ljust(3)))

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='extradaystemplate')
        self.db_handle = db_handle    
    
    def set_new(self, value=None):
        if value==None:
            if self.et==None:
                self.new = True
            else:
                self.new = False
        else:
            self.new = value
                
    def set_update(self, value):
        if value:
            if not self.update:
                M = self.Menu
                if not self.new:
                    M.add_item('Update', 'UPDATE - Update database with changes', self.update_db)
                else:
                    M.add_item('Save', 'SAVE - Add record to the database', self.add_db)
        else:
            pass
            #M.delete_item('Update')
            #Need to update menu 
        self.update = value
    
    def day_title(self):
        if self._day_title==None:
            return ''
        return self._day_title
    
    def update_db(self, options=None):
        self.db_handle.fetchdata('update_extra_days_template', [self.et, self.day_title(), self.extra_date.date(True), self.points, self.ideal_max, ])
        self.set_update(False)
    
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
    N = ExtraDaysTemplate(db_handle=db_handle)
    #N = ExtraDaysTemplate(db_handle=db_handle, title='Christmas Day', extra_date='12/25/2019', et=1, points=2, ideal_max=5)
    N.menu()
    #N.print_menu()
    #N.About()