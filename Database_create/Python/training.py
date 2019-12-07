# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from login import Login
from employee import employee
from date import date
from roster import Roster
from attendee import Attendee
from season import Season

class  Training(object):
    """Training"""
    def __init__(self,
                 tlid=None,
                 training_title=None,
                 lead_instructor=None,
                 location=None,
                 description=None,
                 notes=None,
                 db_handle=None,
                 training_date=None):
        """Create New Instanace of Training"""
        self.set_db_handle(db_handle)
        self.tlid = tlid
        self._training_title = training_title
        self._lead_instructor = employee(db_handle=self.db_handle, eid=lead_instructor)
        if lead_instructor:
            self._lead_instructor.load_emp_db()
        self._location=location
        self._description = description
        self._notes = notes
        self.training_date = date(date=training_date, db_handle=self.db_handle)
        self.Menu = Menu('Edit a Trianing Menu', db_handle=self.db_handle)
        self.Roster = Roster(tlid=self.tlid, db_handle=self.db_handle)
        self.said = Season(db_handle=self.db_handle)
    
    def __str__(self):
        return "Training: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Training: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def description(self, pad=20):
        print(self._description)
        if self._description==None:
            return "".ljust(pad)
        else:
            return self._description.ljust(pad)
          
    def training_title(self, pad=10):
        if self._training_title:
            return self._training_title.ljust(pad)
        else:
            return "".ljust(pad)

    def get_description(self, options=None):
        d = None
        if len(options[2])>0:
           d = " ".join(options[2])
        while not d:
            d = raw_input("Enter training description: ")
        self._description = d
    
    def get_lead_instructor(self, options=None):
        e= None
        if options[1]:
            e = options[1]
        while not e:
            try:
                e = int(raw_input("Enter Instructor ID: "))
            except:
                pass
        self.set_lead_instructor(e)
    
    def get_location(self, options=None):
        l = None
        if len(options[2])>0:
           l = " ".join(options[2])
        while not l:
            l = raw_input("Enter Location: ")
        self._location = l

    def get_notes(self, options=None):
        # will need to create a notes edit class so I can implement this. also should have a get class. 
        n = None
        if len(options[2])>0:
           n = " ".join(options[2])
        while not n:
            n = raw_input("Enter training notes: ")
        self._notes = n
    
    def get_training_title(self, options=None):
        training_title = None
        if options[2]:
            training_title = " ".join(options[2])
        while not training_title:
            try:
                training_title = raw_input('Enter training_title: ')
            except:
                training_title = None
        if len(training_title)>40:
            training = training_title[0:40]
        self.set_training_title(training_title)
    
    def location(self, pad=20):
        if self._location:
            return self._location.ljust(pad)
        else:
            return "".ljust(pad)
    
    def load_training_header_db(self):
        if self.tlid:
            R = self.db_handle.fetchdata('get_training_log_header', [self.tlid,])
            for r in R:
                self.set_lead_instructor(r[2])
                self.set_training_title(r[4])
                self._location = r[3]
                self._notes = r[6]
                self._description = r[5]
                self.training_date.set_date(r[1])
                self.said.said = r[7]
                self.said.get_season_db()
            
    def menu(self, options=None):
        M = self.Menu
        M.add_item('Title', 'training_title - Menu test item', self.get_training_title)
        M.add_item('Lead', 'LEAD <ID> - Set or change Lead Instructor', self.get_lead_instructor)
        M.add_item('Location', 'LOCATION <name> - set location name', self.get_location)
        M.add_item('Description', 'DESCTRIPTION <text> - set the Description for the trainint' , self.get_description)
        M.add_item('Notes', 'NOTES <text> - set the notes for a training sesion', self.get_notes)
        M.add_item('Save', 'SAVE - add or save training header to database', self.save_training_db)
        M.add_item('Date', 'DATE <date> - set training session date', self.training_date.get_date)
        M.add_item('Add', 'ADD <eid> - add an attendee to roster', self.Roster.add_eid)
        M.add_item('Delete', 'DELETE <rid> - remove an attendee from the roster', self.Roster.delete_rid)
        M.add_item('Edit', 'EDIT <rid> - edit notes on addendee from the roster', self.Roster.edit_rid)
        M.menu_display = self.print_menu
        M.Menu()
    
    def notes(self, pad=20):
        if self._notes==None:
            return "".ljust(pad)
        else:
            return self._notes.ljust(pad)
        
    def print_menu(self):
        print("""
    tlid:       %s
    Date:       %s
    Title:      %s
    Instructor: %s
    Location:   %s
    Descripton: %s
    Season:     %s
    Notes:      %s""" % (self.tlid,
                         self.training_date.date(True),
                         self.training_title(),
                         self._lead_instructor.name(nickname=True),
                         self.location(), 
                         self.description(),
                         self.said.season_name(),
                         self.notes()))
        self.Roster.print_menu()
        
    def print_self(self):
        print("""    %s %s %s %s %s %s""" % (str(self.tlid).ljust(4),
                                 self.training_date.date(True).ljust(12),
                                 self.training_title(33),
                                 self.location(26),
                                 str(len(self.Roster)).ljust(10),
                                 self._lead_instructor.name().ljust(20)
                                 ))
    
    def save_training_db(self, options=None):
        if self.tlid==None:
            R = self.db_handle.fetchdata('add_training_header', [self.training_date.db_date(),
                                                                 self._lead_instructor.eid,
                                                                 self.location(0),
                                                                 self.training_title(0),
                                                                 self.description(0),
                                                                 self.notes(0),])
            try:
                self.tlid = R[0][0]
            except Exception as e:
                print ("Unexpected error: %s" % e)
                raw_input('Resume:')
                
        else:
            R = self.db_handle.fetchdata('update_training_header', [self.tlid,
                                                                    self.training_date.date(True),
                                                                    self._lead_instructor.eid,
                                                                    self.location(0),
                                                                    self.training_title(0),
                                                                    self.description(0),
                                                                    self.notes(0),])
    
    def set_lead_instructor(self, lead):
        self._lead_instructor.eid = lead
        self._lead_instructor.load_emp_db()
    
    def set_training_title(self, training_title=None):
        if training_title:
            self._training_title = training_title
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Training')
        self.db_handle = db_handle
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Training
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
        


if __name__ == "__main__":
    L = Login(login='halc')
    L.Login()
    N = Training(db_handle=L.db_handle, tlid=1)
    N.load_training_header_db()

    #N.print_menu()
    N.menu()
    #N.About()