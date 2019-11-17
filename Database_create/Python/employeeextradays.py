# Author: Harold Clark
# Copyright Harold Clark 2019
#
from extradaystemplate import ExtraDaysTemplate
from database import database
from menu import Menu
from employee import employee

class  EmployeeExtraDays(ExtraDaysTemplate):
    """EmployeeExtraDays"""
    def __init__(self,
                 eeid=None,
                 eid=None,
                 et=None,
                 title=None,
                 extra_date=None,
                 points=None,
                 ideal_max=None,
                 booked=None,
                 priority=None,
                 db_handle=None):
        """Create New Instanace of New Class"""
        ExtraDaysTemplate.__init__(self,
                                   et=et,
                                   title=title,
                                   extra_date=extra_date,
                                   points=points,
                                   ideal_max=ideal_max,
                                   booked=booked,
                                   db_handle=db_handle)
        
        self._eeid = eeid
        self.set_new()
        self.eid = employee(eid=eid, db_handle=self.db_handle)
        self.eid.load_emp_db()
        self.priority = priority
        
        self.Menu = Menu('eeid Menu', db_handle=self.db_handle)
    
    def __str__(self):
        return "EmployeeExtraDays: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "EmployeeExtraDays: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def add_db(self, options=None):
        results = self.db_handle.fetchdata('add_employee_extra_day',
                                           [self.eid.eid,
                                            self.et,
                                            self.priority,])
        self._eeid = results[0][0]        
        self.set_new(False)
        self.set_update(False)
        
    def employee_total(self):
        result = self.db_handle.fetchdata('get_employee_extra_points', [self.eid.eid,])
        return result[0][0]
    
    def Edit_eeid(self, options=None):
        raw_input('No working code for this option: ')
        
    def eeid(self):
        if self._eeid:
            return self._eeid
        else:
            return ''
        
    def menu(self, options=None):
        M = self.Menu
        M.add_item('select', 'Select - set extra day from list', M.print_new)
        M.add_item('ET', 'ET <#> - set extra day by ID', self.set_et)
        M.add_item('Priority', 'Priority - Set Priority for Extra day', self.set_priority)
        M.menu_display = self.print_menu
        M.Menu()
        
    def print_menu(self):
        print("""
    eeid:               %s
    employee:           %s
    Extra Day:          %s
    Date:               %s
    Need/Booked:        %s/%s
    Points (day/total): %s/%s
    Priority:           %s""" % (self.eeid(),
                        self.eid.name(nickname=True),
                        self.day_title(),
                        self.extra_date.date(True),
                        self.ideal_max,
                        self._booked,
                        self.points,
                        self.employee_total(),
                        self.priority))
        
    def print_self(self):
        print("""    %s %s %s %s""" % (self.eeid(),
                                       self.day_title(),
                                       self.extra_date.date(True),
                                       self.points))
    
    def set_et(self, options=None):
        if options[1]:
            self.et = options[1]
        else:
            try:
                self.et = int(raw_input('Enter Extra Day ID: '))
            except:
                raw_input('invalid option retuning to menu: ')
                return 1
        self.load_template_db()
        self.set_update(True)
    
    def set_new(self, value=None):
        if value==None:
            
            try:                
                if self._eeid==None:
                    self.new = True
                else:
                    self.new = False
            except:
                return
        else:
            self.new = value

    def set_priority(self, options=None):
        if options[1]:
            self.priority = options[1]
        else:
            try:
                self.priority = int(raw_input('Enter priotity for extra day: '))
            except:
                raw_input('invalid option retuning to menu: ')
                return 1
        self.set_update(True)
    
    def update_db(self, options=None):
        raw_input(self.et)
        raw_input(self.eeid)
        self.db_handle.fetchdata('update_employee_extra_day',
                                 [self.eeid(),
                                  self.eid.eid,
                                  self.et,
                                  self.priority,])
        self.set_update(False)
    
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : EmployeeExtraDays
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
        


if __name__ == "__main__":
    db_handle = database(owner='emplyeeextradays.py - __main__')
    N = EmployeeExtraDays(db_handle=db_handle, eid=110)
    if N.et:
        N.load_template_db()
    N.menu()
    #N.About()
    #N.print_menu()
    #N.print_self()
    
    #print(N.employee_total())