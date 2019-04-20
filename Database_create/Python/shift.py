# Author: Harold Clark
# Copyright Harold Clark 2019
#
from datetime import datetime
import psycopg2
from employee import employee
from employee import employees
from database import database
from date import date
    
class shift(object):
    def __init__(self,
                 shift_name=None,
                 start_time=None,
                 end_time=None,
                 html_class=None,
                 date=None,
                 sid=None,
                 ct=None,
                 ct_title=None,
                 eid=None,
                 db_handle=None):
        """init a shift"""
        self.set_db_handle(db_handle)
        self.shift_name = shift_name
        self.start_time = start_time
        self.end_time = end_time
        self.html_class = html_class
        self.sid = sid
        self.ct = ct
        self.ct_title = ct_title
        self.date = date(date=date, db_handle=self.db_handle)
        self.eid = eid
           

    def add_employee_shift(self):
        """add eid to shift"""
        c = psycopg2.connect(user="postgres",
                             port="5432",
                             host="127.0.0.1",
                             database="skischool")
        cur = c.cursor()
        cur.callproc('add_employee_shift', [self.eid, self.sid, ])
        result = cur.fetchall()

        
        #self.print_shift()
        c.commit()
        cur.close()
        c.close()

    def add_shift_db(self):
        """Add shift object to the shift table in database"""
        result = self.db_handle.fetchdata('add_shift', [self.shift_name,
                                                        self.start_time,
                                                        self.end_time,
                                                        self.date.date(True),
                                                        self.ct_title,
                                                        self.html_class, ])
        self.sid = result[0][0]

    def print_shift(self):
        if self.sid==None:
            sid = ''
        else:
            sid = str(self.sid)
        print """        sid: %s %s: %s-%s    eid: %s""" % (sid.ljust(5),
                                                            self.shift_name,
                                                            self.start_time,
                                                            self.end_time,
                                                            self.eid)

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='employee')
        self.db_handle = db_handle
    
    def shift_length_segments(self):
        t = ((self.end_time.hour * 60 + self.end_time.minute) - (self.start_time.hour * 60 + self.start_time.minute)) /15
        return t

class shifts(object):
    def __init__(self, db_handle=None):
        self.slist = []
        self.set_db_handle(db_handle)
    
    def append(self, shift):
        self.slist.append(shift)
        self.sort()
        
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='employee')
        self.db_handle = db_handle

    def sort(self):
        end_time = sorted(self.shifts, key=attrgetter('end_time'))
        start_time = sorted(end_time, key=attrgetter('start_time'))
        self.shifts = sorted(start_time, key=attrgetter('date'))        
        
if __name__ == '__main__':
    
    s = shift(shift_name = 'Private - test',
              start_time = '10:00',
              end_time = '11:30',
              html_class = 'Private',
              date = '04/13/19',
              ct_title = 'Ski Instructor')
    s.add_shift_db()
    s.print_shift()
    
    