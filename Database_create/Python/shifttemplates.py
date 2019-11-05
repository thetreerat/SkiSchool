# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from dow import DOW
from menu import Menu
from shifttemplate import ShiftTemplate

class  ShiftTemplates(object):
    
    ShiftTemplate.index = 1
    ShiftTemplate.object = 2
    ShiftTemplate.stid = 3
    ShiftTemplate.shift_name = 4
    ShiftTemplate.no_index = 5
    def __init__(self,
                 dow=None,
                 db_handle=None):
        """Create New Instanace of ShiftTemplates"""
        self.set_db_handle(db_handle)
        self.shifttemplates = []
        self.dow = DOW(dow, 'Enter Day of week to display:', db_handle=self.db_handle)
    
    def __len__(self):
        return len(self.shifttemplates)
    
    def __str__(self):
        return "ShiftTemplates: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "ShiftTemplates: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : ShiftTemplates
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")

    def append(self, shifttemplate):
        self.shifttemplates.append(shifttemplate)
        self.sort()
    
    def clear(self):
        """ """
        self.shifttemplates = []
    
    def check_id(self, stid, return_type=ShiftTemplate.object):
        i = 0
        for t in self.shifttemplates:
            if t.stid==stid:
                if return_type==ShiftTemplate.index:
                    return i
                elif return_type==ShiftTemplate.shift_name:
                    return t.shift_name
                elif return_type==ShiftTemplate.object:
                    return t
            i += 1
        return None
    
    def copy_template(self, options=None):
        if options[1]:
            t = self.check_id(options[1])
            n = ShiftTemplate(db_handle=self.db_handle)
            n.shift_name = t.shift_name
            n.start_time.set_time(t.start_time.time(True))
            n.end_time.set_time(t.end_time.time(True))
            n.dow.set_dow(t.dow.DOW())
            n.cert_required.ct = t.cert_required.ct
            n.cert_required.load_cert_db()
            n.set_said(said=t.said.said)
            n.number_needed = t.number_needed
            return n
            #n.menu(options)
                    
    def get_current_templates(self, options=None):
        self.clear()
        if self.dow.DOW():
            results = self.db_handle.fetchdata('get_current_shift_templates', [self.dow.DOW(),])
        else:
            results = self.db_handle.fetchdata('get_current_shift_templates',[])
        for r in results:
            
            t = ShiftTemplate(stid=r[0],
                              shift_name=r[1],
                              start_time=r[2],
                              end_time=r[3],
                              dow=r[4],
                              cert_required=r[5],
                              said=r[6],
                              number_needed=r[7],
                              db_handle=self.db_handle)
            self.append(t)
    
    def manage_template(self, options=None):
        #print(options)
        if options[0][0:2]=='ED':
            stid = options[1]
            T = ShiftTemplate(stid=stid, db_handle=self.db_handle)
            T.load_template_db()
            
        elif options[0][0:3]=='CO':
            T = self.copy_template(options)
            ## currently copy menu option calls copy_template, should come here. 
        else:
            stid = None
            T = ShiftTemplate(db_handle=self.db_handle)
        T.menu(options)
        
        self.clear()
        self.get_current_templates()
  
    def menu(self, options=None):
        
        self.get_current_templates()
        M = Menu('Shift Templates Menu', db_handle=self.db_handle)
        M.menu_display = self.print_menu
        M.add_item('DOW', 'DOW <dow> - Change/set DOW for Display templates', self.set_dow)
        M.add_item('New', 'NEW - Create new shift template', self.manage_template)
        M.add_item('Edit', 'EDIT <stid> - edit a shift Template', self.manage_template)
        M.add_item('Copy', 'COPY <stid> - make a copy of template', self.copy_template)
        #M.menu_display()
        M.Menu()
        
        
    def set_dow(self, options=None):
        cdow = self.dow.DOW()
        self.dow.get_dow(options)
        if cdow!=self.dow.DOW():
            self.clear()
            self.get_current_templates()
        
    def sort(self):
        
        name = sorted(self.shifttemplates, key=self.sort_shift_name)
        time = sorted(name, key=self.sort_start_time)
        self.shifttemplates = sorted(time, key=self.sort_dow)
    
    def sort_dow(self, i):
        return i.dow.sort()
    
    def sort_start_time(self, i):
        return i.start_time.time(True)

    def sort_shift_name(self, i):
        return i.shift_name
    
    def print_list(self):
        print("""
    STID Shift Name            Start Time   End Time    DOW        Certifiction Required   Number Needed   Season
    ---- --------------------- ------------ ----------- ---------- ----------------------- --------------- ---------------------""")
        for t in self.shifttemplates:
            t.print_self()
        
        
    def print_menu(self):
        """ """
        d = """Displaying Day of Week - %s""" % self.dow.DOW()
        d = d.center(90)
        print (d)
        self.print_list()
        
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='ShiftTemplates')
        self.db_handle = db_handle
        
        


if __name__ == "__main__":
    db_handle = database(owner='shifttemplates.py -- __main__')
    T = ShiftTemplates(db_handle=db_handle)
    T
    T.menu()
    
    
    
    print(len(T))
    #N.About()