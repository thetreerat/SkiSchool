# Author: Harold Clark
# Copyright Harold Clark 2019
#
from datetime import datetime
import psycopg2
from operator import attrgetter
from employee import employee
from employee import employees
from database import database
from date import date
from skitime import SkiTime
from menu import Menu
    
class shift(object):
    def __init__(self,
                 shift_name=None,
                 start_time=None,
                 end_time=None,
                 html_class=None,
                 shift_date=None,
                 sid=None,
                 ct=None,
                 ct_title=None,
                 eid=None,
                 db_handle=None):
        """init a shift"""
        self.set_db_handle(db_handle)
        self.sid = sid
        self.shift_name = shift_name
        self.start_time = SkiTime(time=start_time,
                                   question='Enter Start Time',
                                   db_handle=self.db_handle)
        self.end_time = SkiTime(time=end_time,
                                 question='Enter End Time',
                                 db_handle=self.db_handle)
        self.html_class = html_class
        self.ct = ct
        self.ct_title = ct_title
        self.shift_date = date(db_handle=db_handle)
        self.eid = eid
        self.employee = employee(db_handle=self.db_handle)
        self.no_show = None
        self._student_level = None
        self._student_count = 0
        self.worked_time = None
        self.cancelled = False
        self.html_class = None   

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
                                                            self.shift_name.ljust(35),
                                                            self.start_time.time(True),
                                                            self.end_time.time(True),
                                                            self.eid)

    def print_self(self):
        if self.eid==None:
            eid = ''
        else:
            eid = self.eid
        if self.sid==None:
            sid = ''
        else:
            sid = str(self.sid)
        print("""    %s %s %s %s %s %s %s %s %s""" % (sid.ljust(4),
                                 self.shift_name.ljust(25),
                                 self.shift_date.date(True).ljust(11),
                                 self.start_time.time(True).ljust(11),
                                 self.end_time.time(True).ljust(9),
                                 self.employee.name().ljust(22),
                                 self.student_count(True).ljust(13),
                                 self.student_level().ljust(13),
                                 self.worked_time))
              
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='employee')
        self.db_handle = db_handle

    def set_student_count(self, count=None):
        if count==None:
            count = raw_input('Enter Student Count: ')
        try:
            print(count)
            self._student_count = int(count)
        except:
            self._student_count = None
        self.db_handle.fetchdata('update_shifts_student_count', [self.sid, self._student_count, ])
                
    def set_student_level(self, level=None):
        if level==None:
            level = raw_input('Enter Student Level: ')
        try:
            self._student_level = str(level)
        except:
            self._student_level = None
            
    def shift_length_segments(self):
        t = ((self.end_time.hour * 60 + self.end_time.minute) - (self.start_time.hour * 60 + self.start_time.minute)) /15
        return t
    
    def student_count(self, as_string=False):
        student_count = self._student_count
        if student_count==None:
            student_count=0
        if as_string:
            try:
                student_count = str(student_count)
            except:
                student_count = ''
        return student_count
        
    def student_level(self):
        student_level = self._student_level
        if student_level==None:
            student_level = ''
        if type(student_level)=='int':
            student_level = str(student_level)
        return student_level
        
class shifts(object):
    shift.object = 1
    def __init__(self, db_handle=None):
        self.shifts = []
        self.set_db_handle(db_handle)
    
    def append(self, shift):
        self.shifts.append(shift)
        self.sort()
    
    def check_sid(self, sid, return_type=shift.object):
        i = 0
        for s in self.shifts:
            if s.sid==sid:
                if return_type==shift.object:
                    return s
            i += 1
        return None

    def get_shifts_for_date(self, shift_date):
        result = self.db_handle.fetchdata('list_shifts_for_date', [shift_date, ])
        for r in result:
            s = shift(db_handle=self.db_handle)
            s.sid = r[0]
            s.eid = r[5]
            s.shift_name = r[1]           
            s.shift_date.set_date(r[2])
            s.start_time.set_time(r[3])
            s.end_time.set_time(r[4])
            s.employee.set_name([r[6], r[7]])
            s.employee.eid = r[5]
            s.no_show = r[8]
            s._student_level = r[9]
            s._student_count = r[10]
            s.worked_time = r[11]
            s.ct = r[12]
            s.cancelled = r[13]
            s.html_class = r[14]
            self.append(s)
    
    def menu_date(self, options=None):
        display_date = date(db_handle=self.db_handle, question_text='Enter Shift Date: ')
        display_date.get_date()
        self.get_shifts_for_date(shift_date=display_date.date(True))
        M = Menu(db_handle=self.db_handle, menu_title='Shfits for a Date')
        M.add_item('Count', 'COUNT <SID> - Add count to shift', self.update_student_count)
        M.add_item('Cancel', 'CANCEL <SID> - Cancel a shift', self.under_construction)
        M.add_item('Level', 'LEVEL <SID> - edit student level or assigment', self.under_construction)
        M.add_item('Hours', 'HOURS <SID> <HOURS> - Edit hours by instructor for Lesson', self.under_construction)
        M.add_item('NoShow', 'NOSHOW <SID> - Mark an instructor as no show for shift', self.under_construction)
        M.add_item('Instrcutor', 'INSTRUCTOR <SID> <firstname> <lastname> - add instructor for shift', self.under_construction)
        M.menu_display = self.print_list
        M.Menu()
        
        
    def print_list(self):
        print("""
    SID  Shift Name                shift date  shift start shift end instructor             student count student level
    ---- ------------------------- ----------- ----------- --------- ---------------------- ------------- -------------""") 
        for s in self.shifts:
            s.print_self()
        print("""    ------------------------------------------------------------------------------------------------------------------""")
        print("""    shift count: %s""" % (self.shift_count()))
        print("""    ------------------------------------------------------------------------------------------------------------------""")
        
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='employee')
        self.db_handle = db_handle

    def shift_count(self):
        return len(self.shifts)
    
    def sort(self):
        end_time = sorted(self.shifts, key=attrgetter('end_time'))
        start_time = sorted(end_time, key=attrgetter('start_time'))
        self.shifts = sorted(start_time, key=attrgetter('shift_date'))
    
    def update_student_count(self, options):
        s = self.check_sid(options[1])
        s.set_student_count()
    
    def under_construction(self, options):
        raw_input('%s - not functional yet' % options[0])
        
if __name__ == '__main__':
    db_handle = database(owner='shift.py - __main__')
    display_date = date(db_handle=db_handle, question_text='Enter Shift Date: ')
    display_date.get_date()
    S = shifts(db_handle=db_handle)
    