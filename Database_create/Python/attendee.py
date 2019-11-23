# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from employee import employee
from employee import employees
class  Attendee(employee):
    """Attendee"""
    def __init__(self,
                 rid=None,
                 notes=None,
                 eid=None,
                 firstname=None,
                 lastname=None,
                 suffix=None,
                 nickname=None,
                 tlid=None,
                 db_handle=None):
        """Create New Instanace of Attendee"""
        
        employee.__init__(self,
                          eid=eid,
                          firstname=firstname,
                          lastname=lastname,
                          suffix=suffix,
                          nickname=nickname,
                          db_handle=db_handle)
        self.rid = rid
        self._notes = notes
        self.tlid = tlid
        self.Menu = Menu('Attendee Menu', db_handle=self.db_handle)
    
    def __str__(self):
        return "Attendee: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Attendee: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def add_eid(self, options=None):
        eid = None
        if options[1]:
            eid = options[1]
        else:
            while not eid:
                try:
                    eid = int(raw_input('Enter eid: '))    
                except:
                    eid = None
        self.eid = eid
        self.load_emp_db()
    
    def find_eid(self, options=None):
        E = employees(db_handle=self.db_handle)
        E.find_name(options)
        for e in E.elist:
            e.print_self()
        self.eid = raw_input('Enter employee id: ' )
            
    def get_notes(self, options=None):
        notes = None
        if len(options[2])>0:
            notes = " ".join(options[2])
        while not notes:
            try:
                notes = raw_input('Enter notes: ')
            except:
                notes = None
        self.set_notes(notes)
        
    def notes(self, pad=10):
        if self._notes:
            return self._notes.ljust(pad)
        else:
            return "".ljust(pad)
    

    def menu(self, options=None):
        M = self.Menu
        M.add_item('Notes', 'notes - Menu test item', self.get_notes)
        M.add_item('Attendee','ATTENDEE <eid> - set attendee to employee ID', self.add_eid)
        M.add_item('Find', 'FIND <fristname> <lastname>   - find attendee by name', self.find_eid)
        M.add_item('List', 'LIST - List current employee to select an attendee', M.print_new)
        M.add_item('Save', 'SAVE - save record to database', self.save_attendee_db)
        M.menu_display = self.print_menu
        M.Menu()
        
    def print_menu(self):
        print("""
    tlid:     %s
    rid:      %s
    Attendee: %s
    Notes:    %s""" % (self.tlid, self.rid, self.name(), self.notes()))
        
    def print_self(self):
        print("""    %s %s %s %s %s""" % (
                                       str(self.tlid).ljust(5),
                                       str(self.rid).ljust(5),
                                       str(self.eid).ljust(5),
                                       self.name(nickname=True).ljust(35), 
                                       self.notes()))

    def save_attendee_db(self, options=None):
        if self.rid:
            print("   rid: %s tlid: %s eid: %s notes: %s" % (self.rid, self.tlid, self.eid, self.notes()))
            self.db_handle.fetchdata('update_eid_roster', [self.rid, self.tlid, self.eid, self.notes(),])
        else:
            self.db_handle.featchdata('add_eid_roster',[self.tlid, self.eid, self.notes])
    def set_notes(self, notes=None):
        if notes:
            self._notes = notes
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Attendee')
        self.db_handle = db_handle
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Attendee
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
        


if __name__ == "__main__":
    from login import Login
    L = Login(login='halc')
    L.Login()
    N = Attendee(db_handle=L.db_handle)
    N.menu()
    #N.print_menu()
    #N.About()