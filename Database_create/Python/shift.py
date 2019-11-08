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
                                   question='Enter Start Time: ',
                                   db_handle=self.db_handle)
        self.end_time = SkiTime(time=end_time,
                                 question='Enter End Time: ',
                                 db_handle=self.db_handle)
        self.html_class = html_class
        self.ct = ct
        self.ct_title = ct_title
        self.shift_date = date(db_handle=self.db_handle)
        self.eid = eid
        self.employee = employee(db_handle=self.db_handle)
        self.no_show = None
        self._student_level = None
        self._student_count = 0
        self._worked_time = 0
        self.cancelled = False   

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
                                                        self.start_time.time(),
                                                        self.end_time.time(),
                                                        self.shift_date.date(True),
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
                                 self.worked_time(True)))
              
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='shift.py - set_db_handle')
        self.db_handle = db_handle
    
    def get_worked_time(self, hours=None):
        if hours==None:
            hours = raw_input('Enter hours worked for %s: ' % (self.employee.name()))
        self.set_worked_time(hours)
        self.db_handle.fetchdata('update_shifts_worked_time', [self.sid, self._worked_time, ])
    
    def set_worked_time(self, hours=None):
        try:
            self._worked_time = float(hours)
        except:
            self._worked_time = 0
            
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
        self.db_handle.fetchdata('update_shifts_student_level', [self.sid, self._student_level, ])
            
    def shift_length_segments(self):
        t = ((self.end_time.time().hour * 60 + self.end_time.time().minute) - (self.start_time.time().hour * 60 + self.start_time.time().minute)) /15
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
    
    def worked_time(self, as_string=False):
        worked_time = self._worked_time
        if worked_time==None:
            worked_time=0
        if as_string:
            try:
                worked_time = str(worked_time)
            except:
                worked_time = ''
        return worked_time    
        
class shifts(object):
    shift.object = 1
    def __init__(self, db_handle=None):
        self.set_db_handle(db_handle)
        self.date = date(db_handle=self.db_handle)
        self.shifts = []
        
    def __len__(self):
        return len(self.shifts)
        
    def __str__(self):
        return "Shifts: db: %s count: %s" % (self.db_handle.owner, len(self.shifts))
        
    def __repr__(self):
        return "Shifts: db: %s, pythonID: %s count: %s" % (self.db_handle.owner, id(self), len(self.shifts))

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

    def clear(self):
        self.shifts=[]
        
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
            s.set_worked_time(r[11])
            s.ct = r[12]
            s.cancelled = r[13]
            s.html_class = r[14]
            self.append(s)
    
    def menu_date(self, options=None):
        display_date = date(db_handle=self.db_handle,
                            default_date=datetime.now().strftime('%m/%d/%Y'))
        display_date.question =question_text='Enter Shift Date (%s): ' % (display_date.default_date(True))
        display_date.get_date()
        self.clear()
        self.get_shifts_for_date(shift_date=display_date.date(True))
        M = Menu(db_handle=self.db_handle, menu_title='Shfits for a Date')
        M.add_item('Count', 'COUNT <SID> - Add count to shift', self.update_student_count)
        M.add_item('Cancel', 'CANCEL <SID> - Cancel a shift', self.under_construction)
        M.add_item('Level', 'LEVEL <SID> - edit student level or assigment', self.update_student_level)
        M.add_item('Hours', 'HOURS <SID> <HOURS> - Edit hours by instructor for Lesson', self.update_worked_time)
        M.add_item('NoShow', 'NOSHOW <SID> - Mark an instructor as no show for shift', self.under_construction)
        M.add_item('Instructor', 'INSTRUCTOR <SID> <firstname> <lastname> - add instructor for shift', self.update_instructor)
        M.add_item('New', 'NEW - create a new adhoc shift', M.print_new)
        M.add_item('Publish', 'PUBLISH - Publish Shift', M.print_new)
        M.menu_display = self.print_list
        M.Menu()
                
    def print_list(self):
        print("""
    SID  Shift Name                Shift Date  Shift Start Shift End Instructor             Student Count Student Level Hours
    ---- ------------------------- ----------- ----------- --------- ---------------------- ------------- ------------- ------""") 
        for s in self.shifts:
            s.print_self()
        print("""    -------------------------------------------------------------------------------------------------------------------------""")
        print("""    shift count: %s""" % (len(self)))
        print("""    -------------------------------------------------------------------------------------------------------------------------""")
    
    def publish(self):
        pass
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='shift.py - init shifts')
        self.db_handle = db_handle
    
    def sort(self):
        end_time = sorted(self.shifts, key=self.sort_key_end)
        start_time = sorted(end_time, key=self.sort_key_start)
        self.shifts = sorted(start_time, key=self.sort_key_date)
    
    def sort_key_end(self, i):
        return i.end_time.time(True)
    
    def sort_key_start(self, i):
        return i.start_time.time(True)
    
    def sort_key_date(self, i):
        return i.shift_date.date(True)
    
    def update_worked_time(self, options):
        s = self.check_sid(options[1])
        s.get_worked_time()
        
    def update_instructor(self, options):
        s = self.check_sid(options[1])
        if s:
            E = employees(db_handle=self.db_handle)
            try:
                if options[2][0].lower() in ['available','availabl','availab','availa','avail','avai','ava','av', 'a']:
                    E.list_availability(s.sid)
                elif options[2][0].lower() in ['find', 'fin', 'fi', 'f']:
                    E.find_name(options)
                elif options[2][0].lower() in ['id']:
                    try:
                        eid = int(raw_input('Enter employee ID: '))
                        #e = employee(eid=eid, db_handle=self.db_handle)
                        #e.load_emp_db()
                        s.eid = eid
                        self.db_handle.fetchdata('add_employee_shift', [s.eid, s.sid,])
                        return
                    except:
                        return
                else:
                    E.find_name(options)
            except:
                E.list_availability(s.sid)
            s.print_self()
            E.list(return_type=employee.index, shifts=False)
            try:
                i = int(raw_input('select instructor number: '))
                print(i)
                s.eid = E.elist[i].eid
                print E.elist[i].eid
                s.employee = E.elist[i]
                self.db_handle.fetchdata('add_employee_shift', [s.eid, s.sid,])
            except:
                pass
                print('Invalid select')
                raw_input('ready?')
        
    def update_student_count(self, options):
        s = self.check_sid(options[1])
        s.set_student_count()

    def update_student_level(self, options):
        s = self.check_sid(options[1])
        s.set_student_level()
        
    def under_construction(self, options):
        raw_input('%s - not functional yet' % options[0])
        
if __name__ == '__main__':
    db_handle = database(owner='shift.py - __main__')
    display_date = date(db_handle=db_handle, question_text='Enter Shift Date: ')
    display_date.set_date('02/11/2019')
    #display_date.get_date()
    S = shifts(db_handle=db_handle)
    S.get_shifts_for_date(shift_date=display_date.date(True))
    print(len(S.shifts))
    #s = shift(db_handle=db_handle)
    #print(s.worked_time(True))
    #s.shift_name = 'Test shift'
    #S.append(s)
    S.print_list()    
    