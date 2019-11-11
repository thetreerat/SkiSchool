# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from datetime import datetime

class  date(object):
    """project date object"""
    def __init__(self,
                 date=None,
                 question_text='Enter Date: ',
                 db_handle=None,
                 db_proc=None,
                 db_proc_options = None,
                 default_date=None):
        """Create New Instanace of New Class"""
        self._default_date = None
        self.set_date(date) 
        self.question = question_text
        self.set_db_handle(db_handle)
        self.db_proc = db_proc
        self.db_proc_options = db_proc_options
        self.set_default(default_date)
            
    def __str__(self):
        return "DATE - date: %s, question: %s, db: %s" % (self.date(True), self.question, self.db_handle.owner)
    
    def __repr__(self):
        return "DATE - date: %s, question: %s,  db: %s, pythonID: %s" % (self.date(True), self.question, self.db_handle.owner, id(self))
    
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
            return self._date
        else:
            if self._date == None:
                return ''
            else:
                return self._date.strftime('%m/%d/%Y')

    def default_date_str(self):
        if self._default_date:
            return self._default_date.strftime('%m/%d/%Y')
        else:
            return ''
        
    def default_date(self, as_string=False):
        if as_string:
            if self._default_date ==None:
                return ''
            else:
                return self._default_date.strftime('%m/%d/%Y')
        else:    
            return self._default_date
    
    def get_date(self, options=None):
        """method for getting date from user, verifing, and setting in object"""
        try:
            self._date = datetime.strptime(options[2][0], '%m/%d/%Y')
        except:
            try:
                userinput = raw_input(self.question)
                if userinput=='' and self.default_date!=None:
                    self._date = self._default_date
                    return
                else:
                    self._date = datetime.strptime(userinput, '%m/%d/%Y')
            except ValueError:
                self.get_date(options=None)
                       
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='date.py - date')
        self.db_handle = db_handle
    
    def set_date(self, date):
        """method for setting date from passed value after verifing is a date"""
        if 'datetime.date' in str(type(date)):
            self._date = date
            return
        if date!=None:
            try:
                self._date = datetime.strptime(date, '%m/%d/%Y')
            except:
                pass
        if not hasattr(self, '_date'):
            self._date = None    

    def set_default(self, default_date):
        if default_date==None:
            self._default_date = None
        else:
            try:
                self._default_date = datetime.strptime(default_date, '%m/%d/%Y')
            except ValueError:
                try:
                    self._default_date = datetime.strptime(default_date, '%m/%d/%y')                    
                except:
                    print('set_default_date had a ValueError')
            #try:
            #    print(default_date)
            #    self._default_date = datetime.strftime(default_date, '%m/%d/%y')
            #except:
            #    print('except: %s' % (ValueError))
                #pass
                #self._default_date = None
                    
                
class DOB(date):
    """project Date of Birth date object, subclassed from date"""
    def __init__(self, DOB=None, db_handle=None):
        date.__init__(self, date=DOB, question_text='Enter Date of Birth(MM/DD/YYYY): ', db_handle=db_handle)
        self.name = None
 
    def __str__(self):
        return "DOB - Date of Birth: %s, age: %s, question: %s, db: %s" % (self.date(True),
                                                                           self.age(),
                                                                           self.question,
                                                                           self.db_handle.owner)
    
    def __repr__(self):
        return "DOB - Date of Birth: %s, age: %s, question: %s,  db: %s, pythonID: %s" % (self.date(True),
                                                                                       self.age(),
                                                                                       self.question,
                                                                                       self.db_handle.owner,
                                                                                       id(self))
    
    def age(self, adult=False, use_date=None):
        """method that returns age calculated on DOB,"""
        try:
            if use_date==None:
                use_date = datetime.date(datetime.now())
            #raw_input("""use: %s dob: %s """ % (use_date, self.date))
            age = int(int((use_date - self.date()).days) / 365.2425)
            if adult:
                if age>18:
                    age = 'Adult'
        except:
            age = 0
        return age

    def DOB(self, as_string=False):
        if as_string==False:
            return self._date()
        else:
            return self._date.strftime('%m/%d/%Y')
    
    def print_self(self, pad=5):
        title = 'DOB:'
        print('    %s%s' % (title.ljust(5), self.dob(as_string=True)))
        
    def set_age(self, age):
        DOB = datetime.now()
        try:
            DOB = DOB.replace(year = DOB.year - age)
        except ValueError:
            DOB = DOB + (date(DOB.year - age, 3,1 ) - date(DOB.year, 3,1))
        self.set_date(DOB)
        
class date_pair(object):
    """project date pair object"""
    def __init__(self, start_date=None, end_date=None, db_handle=None):
        self.set_db_handle(db_handle)
        self.start_date = date(date=start_date,
                               question_text='On or After Date(MM/DD/YYYY) : ',
                               db_handle=self.db_handle)
        self.end_date = date(date=end_date,
                             question_text='On or Before Date(MM/DD/YYYY) : ',
                             db_handle=self.db_handle)

    def __str__(self):
        return "DATE_PAIR - date_start: %s date_end %s, db: %s" % (self.start_date.date(True),
                                                             self.end_date.date(True),
                                                             self.db_handle.owner)
    
    def __repr__(self):
        return "DATE_PAIR: start_date: %s, end_date: %s,  db=%s, pythonID: %s" % (self.start_date.date(),
                                                                     self.end_date.date(),
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
    eid = 15
    N = date(db_handle=db_handle,
             db_proc='add_employee_start',
             default_date='11/01/19',
             db_proc_options=[eid,])
    H = date(db_handle=db_handle,
             db_proc='add_employee_start',
             default_date='11/01/2019',
             db_proc_options=[eid,])
    
    #print(N.default_date(True))
    N.question = 'Enter Start date (%s):' % (N.default_date(True))
    #D = DOB(DOB='12/24/1969', db_handle=db_handle)
    #D.set_age(49)
    #print(D.age())
    #P = date_pair(start_date='04/01/2019', end_date='04/30/2019', db_handle=db_handle)
    #print(P)
    #print(D)
    #N.get_date()
    N.get_date()
    print(N.date())
    print(N)
    print(N.date())