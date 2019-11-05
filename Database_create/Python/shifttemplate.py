# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from date import date
from dow import DOW
from skitime import SkiTime
from menu import Menu
from season import Season
from cert import cert
from cert import certs


class  ShiftTemplate(object):
    """ShiftTemplate"""
    def __init__(self,
                 db_handle=None,
                 stid=None,
                 shift_name=None,
                 start_time=None,
                 end_time=None,
                 dow=None,
                 cert_required=None,
                 said=None,
                 number_needed=1):
        """Create New Instanace of ShiftTemplate"""
        self.set_db_handle(db_handle)
        self.stid = stid
        self.shift_name = shift_name
        self.start_time = SkiTime(start_time, 'Enter Shift Start Time:', db_handle=self.db_handle)
        self.end_time = SkiTime(end_time, 'Enter Shift End Time:', db_handle=self.db_handle)
        self.dow = DOW(dow=dow, db_handle=self.db_handle)
        self.cert_required = cert(ct=cert_required, db_handle=self.db_handle)
        self.cert_required.load_cert_db()
        self.said = Season(db_handle=self.db_handle)
        self.set_said(said) 
        self.number_needed = number_needed
    
    def __str__(self):
        return "ShiftTemplate: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "ShiftTemplate: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : ShiftTemplate
Inputs         : None
Returns        : None
Output         : None
Purpose        : This class is for handling shift templates. 

""")
        
    def add_template_db(self, options=None):
        """Load record into database """
        if self.start_time.time(True)=='':
            start = None
        else:
            start = self.start_time.time(True)
        
        if self.end_time.time(True)=='':
            end = None
        else:
            end = self.end_time.time(True)
        result = self.db_handle.fetchdata('add_shift_template', [self.shift_name,
                                                                 start,
                                                                 end,
                                                                 self.dow.DOW(),
                                                                 self.cert_required.ct,
                                                                 self.said.said,
                                                                 self.number_needed,
                                                        ])
        for r in result:
            self.stid = r[0]
        
    def find_cert(self, options=None):
        """find cert to assign to shift template"""
        clist = certs(list_type='cert', db_handle=self.db_handle)
        clist.find_certs_db()
        clist.print_certs()
        cert_index = clist.get_item_index()
        self.cert_required = clist.clist[cert_index]
        self.cert_required.print_cert(print_return='Find')
    
    def load_template_db(self, options=None):
        """get template data from the database"""
        results = self.db_handle.fetchdata('get_shift_template', [self.stid,])
        for r in results:
            self.shift_name = r[1]
            self.start_time.set_time(r[2])
            self.end_time.set_time(r[3])
            self.dow.set_dow(r[4])
            self.cert_required.ct = r[5]
            self.said.said = r[6]
            self.number_needed = r[7]
        self.cert_required.load_cert_db()
        
    def menu(self, options=None):
        """ """
        m = Menu('Shift Template Menu', db_handle=self.db_handle)
        m.menu_display = self.print_menu
        m.add_item('Name','NAME <text> - set or change the name of the shift.', self.set_shift_name)
        m.add_item('Start', 'START <TIME> - Set or change the start time of the current template', self.start_time.get_time)
        m.add_item('End', 'End <TIME> - Set or change the end time of the current template', self.end_time.get_time)
        m.add_item('DOW', 'DOW <DOW> - Set the Day of week for template', self.dow.get_dow)
        m.add_item('Certification', 'CERT <CID> - Set the required cert level for shift.', m.print_new)
        m.add_item('Needed', 'NEEDED <#> - set the number of shifts created from the template.', self.set_number_needed)
        m.add_item('Find', 'FIND - Find cert from list', self.find_cert)
        if options[0]=='NEW' or 'Copy':
            m.add_item('Save', 'SAVE - Save the record in the database', self.add_template_db)
        elif options[0]=='EDIT':
            m.add_item('Save', 'SAVE - Update the shift template in the database', self.update_template_db)
        m.Menu()
    
    def print_menu(self):
        print("""-------------------------------------------------------------------
STID:          %s
Season Name:   %s - %s
Shift Name:    %s
Shift Start:   %s
Shift End:     %s
Day of Week:   %s
Cert Required: %s - %s - %s
Number Needed: %s
-------------------------------------------------------------------
""" % (self.stid,
       self.said.said,
       self.said.season_name(),
       self.shift_name,
       self.start_time.time(True),
       self.end_time.time(True),
       self.dow.DOW(),
       self.cert_required.ct,
       self.cert_required.cert_name,
       self.cert_required.cert_org,
       self.number_needed 
      )
              )
    
    def print_self(self):
        print("""    %s %s %s %s %s %s %s %s""" % (str(self.stid).ljust(4),
                                                       self.shift_name.ljust(21),
                                                       self.start_time.time(True).ljust(12),
                                                       self.end_time.time(True).ljust(11),
                                                       self.dow.DOW().ljust(10),
                                                       self.cert_required.cert_name.ljust(23),
                                                       str(self.number_needed).ljust(15),
                                                       self.said.season_name().ljust(18)
                                                  )
             )
        
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='ShiftTemplate')
            db_handle = database(owner='shifttemplate.py - set_dbhandle')    
        self.db_handle = db_handle
        
    def set_DOW(self, option=None):
        print(options)
        self.DOW = raw_input('Enter DOW: ')
    
    def set_shift_name(self, options=None):
        #print(options)
        title = ''
        if options[2]:
            for o in options[2]:
                if len(title):
                    title = title + " " + o
                else:
                    title = o
            self.shift_name = title
            return
        name = raw_input('Enter Shift Name: ')
        if name!='':
            self.shift_name=name
        
    def set_number_needed(self, options=None):
        if options[1]:
            self.number_needed = options[1]
        else:
            try:
                self.number_needed = int(raw_input('Enter number: '))
            except:
                print('Please enter an integer, field unchanged')
        
    def set_said(self, said=None):
        if said:
            self.said.said = said
            self.said.get_season_db()
        else:
            said = self.said.get_current_season_id()
        self.said.get_season_db()
                   
    def update_template_db(self, options=None):
        self.db_handle.fetchdata('update_shift_template', [self.stid,
                                                           self.shift_name,
                                                           self.start_time.time(True),
                                                           self.end_time.time(True),
                                                           self.dow.DOW(),
                                                           self.cert_required.ct,
                                                           self.said.said,
                                                           self.number_needed,])
        

if __name__ == "__main__":
    db_handle = database(owner='shifttemplate.py - __main__')
    N = ShiftTemplate(db_handle=db_handle)
    #N.print_menu()
    #print(N.said.season_name())
    #N.said()
    #N.About()
    #N.said.print_self()
    #N.load_template_db()
    N.menu()    