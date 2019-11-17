# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from extradaystemplate import ExtraDaysTemplate
from employeeextradays import EmployeeExtraDays


class  ExtraDays(object):
    
    ExtraDaysTemplate.index = 1
    ExtraDaysTemplate.object = 2
    ExtraDaysTemplate.et = 3
    ExtraDaysTemplate.title = 5
    def __init__(self, db_handle=None):
        """Create New Instanace of ExtraDays"""
        self.set_db_handle(db_handle)
        self.extradays = []
        self.eid = None
    
    def __str__(self):
        return "ExtraDays: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "ExtraDays: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def __len__(self):
        return len(self.extradays)

    def add_extra_days(self, options=None):
        e = ExtraDaysTemplate(db_handle=self.db_handle)
        e.print_menu()
        M = e.Menu
        M.add_item('Save', 'SAVE - Save new extra day', e.add_db)
        M.add_item('Title', 'TITLE <VALUE> - set title for extra day', e.get_title)
        M.add_item('Date', 'DATE <DATE> - set date for extra day', e.get_extra_date)
        M.add_item('Points', 'POINTS <VALUE> - Set Points value for extra day', e.get_points)
        M.add_item('Max', 'MAX <VALUE> - Set the maximum ideal number of instructors', e.get_ideal_max)

        M.menu_display = e.print_menu
        M.Menu()
        
    def append(self, newListObject):
        self.extradays.append(newListObject)
        self.sort()
    
    def checkID(self, v, return_type=ExtraDaysTemplate.object):
        i = 0
        for t in self.extradays:
            if t.et==v:
                if return_type==ExtraDaysTemplate.index:
                    return i
                elif return_type==ExtraDaysTemplate.title:
                    return t.shift_name
                elif return_type==ExtraDaysTemplate.object:
                    return t
            i += 1
        return None
        
    def clear(self, options=None):
        self.extradays = []
        
    def edit_extra_days(self, options=None):
        v = options[1]
        o = self.checkID(v=v)
        if o:
            o.menu(options)

    def get_employee_extra_days(self, options=None):
        self.clear()
        if self.eid:
            R = self.db_handle.fetchdata('get_employee_extra_days',[self.eid,])
            for r in R:
                EE = EmployeeExtraDays(eeid=r[0],
                                       eid=r[1],
                                       et=r[2],
                                       priority=r[3])
                EE.load_template_db()
                self.append(EE)
        pass
    
    def get_current_extra_days(self):
        result = self.db_handle.fetchdata('get_current_extra_days', [])
        for r in result:
            d = ExtraDaysTemplate(et=r[0],
                                  title=r[1],
                                  extra_date=r[2],
                                  points=r[3],
                                  ideal_max=r[4],
                                  booked=r[5],
                                  db_handle=self.db_handle)
            self.append(d)
        
    def menu(self, options=None):
        M = Menu('Extra Days Menu', db_handle=self.db_handle)
        M.menu_display = self.print_menu
        M.add_item('Add', 'ADD - Add a new extra day to the current season ', self.add_extra_days)
        M.add_item('Copy', 'COPY <SAID> - Copy a seasons extra days', M.print_new)
        M.add_item('Edit', 'EDIT <ET> - Edit an extra day', self.edit_extra_days)
        M.add_item('Delete', 'DELETE <ET> - remove an extra day', M.print_new)
        M.Menu()

    def menu_eed(self, options=None):
        M = Menu('Employee Extra Days List', db_handle=self.db_handle)
        M.menu_display = self.print_menu_eed
        M.add_itme('Add', 'ADD - Add a new extra day for employee', M.print_new)
        M.add_itme('Edit', 'EDIT <id> - edit an extra day for employee', M.print_new)
        M.add_item('find', 'FIND <title> - find an extra day for employee')
        M.Menu()
        
    def print_list(self):
        self.extradays[0].print_list_heading()
        for e in self.extradays:
            e.print_self()
        print("""    -------------------------------------------------------------------------------------------
    Count: %s""" % (len(self)))
    
    def print_menu(self):
        self.clear()
        self.get_current_extra_days()
        self.print_list()
    
    def print_menu_eed(self):
        self.extradays[0].eid.name(nickname=True)
        for e in self.extradays:
            e.print_self()
    
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
    #N.get_current_extra_days()
    N.eid = 110
    N.get_employee_extra_days()
    N.menu()
    #N.print_menu()