# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from date import date
from location import Location


class  LocationHistory(Location):
    """LocationHistory"""
    def __init__(self,
                 lhid=None,
                 lid=None,
                 assigned_eid=None,
                 assigned_name=None,
                 previous_eid=None,
                 previous_name=None,
                 tracked_user=None,
                 history_date=None,
                 db_handle=None):
        """Create New Instanace of LocationHistory"""
        Location.__init__(self,
                          lid=lid,
                          location_name=None,
                          location_size=None,
                          elist=None,
                          notes=None,
                          lock_sn=None,
                          lock_combination=None,
                          db_handle=db_handle)
        self.load_location_db()
        self.lhid = lhid
        self.lid = lid
        self._assigned_eid = assigned_eid
        self._assigned_name = assigned_name
        self._previous_eid = previous_eid
        self._previous_name = previous_name
        self._tracked_user = tracked_user
        self.history_date = date(db_handle=self.db_handle, date=history_date)
        
    def __str__(self):
        return "LocationHistory: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "LocationHistory: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def assigned_eid(self, pad=4):
        if self._assigned_eid:
            return str(self._assigned_eid).ljust(pad)
        else:
            return "".ljust(pad)
        
    def assigned_name(self, pad=20):
        if self._assigned_name:
            return self._assigned_name.ljust(pad)
        else:
            return "".ljust(pad)        

    def get_assigned_eid(self, options=None):
        """ """
        eid = None
        if options[1]:
            eid = options[1]
        while not eid:
            try:
                eid = int(raw_input('Enter assigned employee ID: '))
            except:
                pass
        self.set_assigned_eid(eid)

    def get_previous_eid(self, options=None):
        """ """
        eid = None
        if options[1]:
            eid = options[1]
        while not eid:
            try:
                eid = int(raw_input('Enter previous employee ID: '))
            except:
                pass
        self.set_previous_eid(eid)
            
    def load_lid_db(self):
        if self.lhid:
            R = self.db_handle.fetchdata('get_location_lid', [self.lhid,])
            self.lid = R[0][0]
    
    def load_location_history_db(self):
        if self.lhid:
            R = self.db_handle.fetchdata('get_location_histroy', [self.lhid,])
            r = R[0]
            self.set_assigned_eid(r[2])
            self._assigned_name = r[3]
            self.set_previous_eid(r[4])
            self._previous_name = r[5]
            self._tracked_user = r[6]
            self.history_date.date(r[7])
        
    def previous_eid(self, pad=4):
        if self._previous_eid:
            return str(self._previous_eid).ljust(pad)
        else:
            return "".ljust(pad)

    def previous_name(self, pad=20):
        if self._previous_name:
            return self._previous_name.ljust(pad)
        else:
            return "".ljust(pad)
            
    def print_menu(self):
        print("""lhid: %s""" % (self.lhid))
        
    def print_self(self):
        print("""    %s %s %s %s %s %s %s %s""" % (str(self.lhid).ljust(4),
                                       str(self.lid).ljust(4),
                                       self.assigned_eid(4),
                                       self.assigned_name(20),
                                       self.previous_eid(4),
                                       self.previous_name(20),
                                       self.tracked_user(15),
                                       self.history_date.date(True).ljust(10)))
        
    def set_assigned_eid(self, eid=None):
        """ """
        if eid:
            self._assigned_eid = eid
            
    def set_previous_eid(self, eid=None):
        if eid:
            self._previous_eid = eid
        pass
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='LocationHistory.py - __init__')
        self.db_handle = db_handle
    
    def tracked_user(self, pad=20):
        if self._tracked_user:
            return self._tracked_user.ljust(pad)
        else:
            return "".ljust(pad)
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : LocationHistory
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
        


if __name__ == "__main__":
    from login import Login
    L = Login(password='login', login='halc')
    L.Login()
    N = LocationHistory(db_handle=L.db_handle, lhid=594)
    N.load_lid_db()
    N.load_location_db()
    N.load_location_history_db()
    N.print_self()
    #N.About()