# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database

class  DOW(object):
    """DOW"""
    def __init__(self, dow=None, question='Enter DOW: ',db_handle=None):
        """Create New Instanace of New Class"""
        self.set_db_handle(db_handle)
        self._dow = None
        self.question = question
        if not dow:
            self.set_dow(dow)
        
    
    def __str__(self):
        return "DOW: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "DOW: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : DOW
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
    
    def DOW(self):
        if self._dow:
            return self._dow
        else:
            return ""
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='dow.py - set_db_handle')
        self.db_handle = db_handle
    
    def get_dow(self, options=None):
        dow = options[2]
        if not dow:
            dow = raw_input(self.question)
        else:
            dow = dow[0]
        self.set_dow(dow)
    
    def set_dow(self, dow=None):
        if dow:
            try:
                if dow.lower() in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                    dow = dow.lower()
                else:
                    dow = int(dow)
                    if dow==0:
                        dow = 'monday'
                    elif dow==1:
                        dow = 'tuesday'
                    elif dow==2:
                        dow = 'wednesday'
                    elif dow==3:
                        dow = 'thursday'
                    elif dow==4:
                        dow = 'friday'
                    elif dow==5:
                        dow = 'saturday'
                    elif dow==6:
                        dow = 'sunday'
            except:
                dow = raw_input(self.question).lower()
            self._dow = dow
        else:
            self._dow = None

if __name__ == "__main__":
    db_handle = database(owner='dow.py - __main__')
    N = DOW(db_handle=db_handle)
    N.get_dow('monday')
    print(N.DOW())
    #N.About()