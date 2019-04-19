# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from datetime import datetime

class  date(object):
    """project date object"""
    def __init__(self, date=None, question_text='Enter Date: ', db_handle=None):
        """Create New Instanace of New Class"""
        self.set_date(date)
        self.question = question_text
        self.set_db_handle(db_handle)
    
    def __str__(self):
        return "date: %s, question: %s, db: %s" % (self.date(True), self.question, self.db_handle.owner)
    
    def __repr__(self):
        return "date - %s, question:,  db=%s, pythonID: %s" % (self.date(True), self.question, self.db_handle.owner, id(self))
    
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : date
Inputs         : date, db_handle, question
Returns        : a project object of date
Output         : None
Methods        : set_date, set_db_handle
Purpose        : This Class for handleing dates in ski_school

""")
    
    def date(self, as_string=False):
        if as_string==False:
            return self._date()
        else:
            return self._date.strftime('%m/%d/%Y')

    def get_date(self, options):
        """method for getting date, verifing, and setting in object""" 
        try:
            self.date = datetime.strptime(options[2][0], '%m/%d/%Y')
        except:
            self.date = datetime.strptime(raw_input(self.question), '%m/%d/%Y')
            
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='date.py - date')
        self.db_handle = db_handle
    
    def set_date(self, date):
        """method for getting date, verifing, and setting in object"""
        if date!=None:
            try:
                self._date = datetime.strptime(date, '%m/%d/%Y')
            except:
                pass
        if not hasattr(self, '_date'):
            self._date = None    

class DOB(date):
    """project Date of Birth date object, subclassed from date"""
    def __init__(self, DOB=None, db_handle=None):
        date.__init__(date=DOB, question_text='', db_handle=db_handle)
               
    def age(self, adult=False, use_date=None):
        """method that returns age calculated on DOB,"""
        if use_date==None:
            use_date = datetime.now()
        age = int(int((use_date - self.date).days) / 365.2425)
        if adult:
            if age>18:
                age = 'Adult'
        return age

    def DOB(self, as_string=False):
        if as_string==False:
            return self._date()
        else:
            return self._date.strftime('%m/%d/%Y')
    
    def print_self(self, pad=5):
        title = 'DOB:'
        print('    %s%s' % (title.ljust(5), self.dob(as_string=True)))
        
class date_pair(object):
    """project date pair object"""
    def __init__(self, start_date=None, end_date=None, db_handle=None):
        self.set_db_handle(db_handle)
        self.start_date = date(date=start_date,
                               question_text='On or After Date(MM/DD/YYYY) : ',
                               db_handle=self.db_handle)
        self.end_date = date(date=start_date,
                             question_text='On or Before Date(MM/DD/YYYY) : ',
                             db_handle=self.db_handle)

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

    def check_date(self, key, value):
        try:
            if key.upper()=='START':
                self.start_date = self.start_date.set_date(value)
            elif key.upper()=='END':
                self.end_date = self.end_date.set_date(value)
        except:
            pass
        
    def set_dates(self, options=None):
        if options!=None:
            if len(options[2])==2:
                try:
                    self.start_date = datetime.strptime(options[2][0], '%m/%d/%Y')
                    self.end_date = datetime.strptime(options[2][1], '%m/%d/%Y')
                except:
                    self.check_date(options[2][0], options[2][1])
            elif len(options[2])==4:
                self.check_date(options[2][0], options[2][1])
                self.check_date(options[2][2], options[2][3])
            elif len(options[2])==1:
                self.start_date= datetime.strptime(options[2][0], '%m/%d/%Y')
                self.end_date= datetime.strptime(options[2][0], '%m/%d/%Y')
        else:
            self.start_date.set_date()
            self.end_date.set_date()
                 
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='date.py - date')
        self.db_handle = db_handle

        
if __name__ == "__main__":
    db_handle = database(owner='date.py - __main__')
    N = date(date='04/19/2019', question_text='test date: ', db_handle=db_handle)
    DOB = DOB(DOB='04/19/2019', db_handle=db_handle)
    print(DOB.age())
    print(DOB)
    print(N)