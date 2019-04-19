# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database

class  date(object):
    """project date object"""
    def __init__(self, date=None, question_text='Enter Date: ', db_handle=None):
        """Create New Instanace of New Class"""
        self.date = date
        self.question = question_text
        self.set_db_handle(db_handle)
    
    def __str__(self):
        return "date: %s, question: %s, db: %s" % (self.date, self.question, self.db_handle.owner)
    
    def __repr__(self):
        return "date - %s, question:,  db=%s, pythonID: %s" % (self.date, self.question, self.db_handle.owner, id(self))
    
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : date
Inputs         : date, db_handle, question
Returns        : a project object of date
Output         : None
Methods        : set_date, set_db_handle
Purpose        : This Class for handleing dates in ski_school

""")

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='date.py - date')
        self.db_handle = db_handle
        
    def set_date(self, options):
        """method for getting date, verifing, and setting in object""" 
        try:
            self.date = options[2][0]
        except:
            self.date = raw_input(self.question)            
        self.update = True
        
class date_pair(date):
    """project date pair object"""
    def __init__(self, start_date=None, end_date=None, db_handle=None):
        self.set_db_handle(db_handle)
        self.start_date = date(date=start_date, question_text='On or After Date: ', db_handle=self.db_handle)
        self.end_date = date(date=start_date, question_text='On or Before Date: ', db_handle=self.db_handle)

    def __str__(self):
        return "date_pair: %s - %s, question: %s, db: %s" % (self.start_date.date,
                                                             self.end_date.date,
                                                             self.question,
                                                             self.db_handle.owner)
    
    def __repr__(self):
        return "date_pair: %s - %s, question:,  db=%s, pythonID: %s" % (self.start_date.date,
                                                                     self.end_date.date,
                                                                     self.question,
                                                                     self.db_handle.owner,
                                                                     id(self))
    
    def set_dates(self, options=None):
        pass
        
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='date.py - date')
        self.db_handle = db_handle
        
if __name__ == "__main__":
    db_handle = database(owner='date.py - __main__')
    N = date(date='04/19/19', question_text='test date: ', db_handle=db_handle)
    print(N)