# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from date import date
from skitime import SkiTime
from menu import Menu


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
                 number_needed=None):
        """Create New Instanace of ShiftTemplate"""
        self.set_db_handle(db_handle)
        self.stid = stid
        self.shift_name = shift_name
        self.start_time = start_time
        self.end_time = end_time
        self.dow = dow
        self.cert_required = cert_required
        self.set_said(said) 
        self.number_needed
    
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

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='ShiftTemplate')
        self.db_handle = db_handle
        
    def set_db_handle(self, said):
        if said==None:
            db_handle = database(onwer='ShiftTemplate')
        self.db_handle = db_handle
        


if __name__ == "__main__":
    N = ShiftTemplate()
    N.About()