# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from datetime import datetime
from six import string_types

class  SkiTime(object):
    """skitime"""
    ampm = ['am', 'AM', 'PM', 'pm']
    def __init__(self, time=None, question='Enter Time: ', db_handle=None):
        """Create New Instanace of New Class"""
        self.set_db_handle(db_handle)
        if time==None:
            self._time = time
        else:
            self.set_time(time)
        self.question = question
    
    def __str__(self):
        return "Time - %s  timedb: %s" % (self.time(True), self.db_handle.owner)
        
    def __repr__(self):
        return "Time - %s db: %s, pythonID: %s" % (self.time(True), self.db_handle.owner, id(self))
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Time
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
    
    def print_self(self):
        print("""%s""" % (self._time))
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Time')
        self.db_handle = db_handle
    
    def set_time(self, time=None):
        print('skitime.set_time: time is %s' % (time))

        if type(time) is list:
            if len(time[2])==2:
                time = '%s %s' % (time[2][0], time[2][1])
        if time==None:
            time = raw_input(self.question).upper()
        if isinstance(time, string_types):
            try:
                time = time.upper()
                print('skitime.set_time: time is %s' % (time))
                if time.find('PM')==-1 and time.find('AM')==-1:
                    format_string = '%H:%M'
                else:
                    format_string = '%I:%M %p'
                self._time = datetime.strptime(time, format_string)
            except:
                self._time = None
                self.set_time()
        else:
            self._time = time
             
    def time(self, as_string=False):
        _time = self._time
        if as_string:
            try:
                _time = self._time.strftime('%H:%M')
            except:
                _time = ''
        return _time

    
if __name__ == "__main__":
    db_handle = database(owner='Time.py - __main__')
    N = SkiTime(question='What your time: ', db_handle=db_handle)
    N.set_time()
    print(N.time(True))
    N.print_self()
    print(N.ampm)
    