# Author: Harold Clark
# Copyright Harold Clark 2019
#
from datetime import datetime
import psycopg2

class employee(object):
    def __init__(self, firstname=None, lastname=None):
        """Init a employee"""
        self.eid = None
        self._firstname = firstname
        self._lastname = lastname
        self.shifts = []
        
    def append_shift(self, shift_name):
        self.shifts.append(shift_name)
        
    def firstname(self):
        return self._firstname
    
    def lastname(self):
        return self._lastname
    
    def printperson(self):
        print("""%s %s: %s""" % (self._firstname, self._lastname, len(self.shifts)))
    
class employees(object):
    def __init__(self):
        self.list = []
    
    def add_employee(self, employee):
        self.list.append(person)
        
    def check_name(self, firstname, lastname):
        i = 0
        for p in self.list:
            if p._firstname==firstname and p._lastname==lastname:
                return i
            i+=1
        return None
    
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
        self.shift_name = shift_name
        self.start_time = start_time
        self.end_time = end_time
        self.html_class = html_class
        self.sid = sid
        self.ct = ct
        self.ct_title = ct_title
        self.date = date
        self.eid = eid
        self.db_handle = db_handle

    def print_shift(self):
        print """sid: %s %s: %s-%s""" % (self.sid, self.shift_name, self.start_time, self.end_time)
    
    def shift_length_segments(self):
        t = ((self.end_time.hour * 60 + self.end_time.minute) - (self.start_time.hour * 60 + self.start_time.minute)) /15
        return t

    def add_shift_db(self):
        """Add shift object to the shift table in database"""
        result = self.db_handle.fetchdata('add_shift', [self.shift_name,
                                                        self.start_time,
                                                        self.end_time,
                                                        self.date,
                                                        self.ct_title,
                                                        self.html_class, ])
        self.sid = result[0][0]
    
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

if __name__ == '__main__':
    s = shift(shift_name = 'Private - test',
              start_time = '10:00',
              end_time = '11:30',
              html_class = 'Private',
              date = '03/13/19',
              ct_title = 'Ski Instructor')
    s.add_shift_db()
    s.print_shift()
    
    