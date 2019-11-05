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
        if dow:
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
        try: 
            dow = options[2]
        except:
            dow = None
        
        if not dow:
            dow = raw_input(self.question)
        else:
            dow = dow[0]
        self.set_dow(dow)
    
    def set_dow(self, dow=None):
        safe_dow = None
        if dow:
            try:
                if dow.lower() in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                    safe_dow = dow.lower()
                else:
                    dow = int(dow)
                    if dow==0:
                        safe_dow = 'monday'
                    elif dow==1:
                        safe_dow = 'tuesday'
                    elif dow==2:
                        safe_dow = 'wednesday'
                    elif dow==3:
                        safe_dow = 'thursday'
                    elif dow==4:
                        safe_dow = 'friday'
                    elif dow==5:
                        safe_dow = 'saturday'
                    elif dow==6:
                        safe_dow = 'sunday'
            except:
                print("""    invalid entery %s""" % (dow))
                safe_dow = raw_input(self.question).lower()
        self._dow = safe_dow


if __name__ == "__main__":
    db_handle = database(owner='dow.py - __main__')
    N = DOW(db_handle=db_handle)
    N.get_dow('monday')
    print(N.DOW())
    #N.About()