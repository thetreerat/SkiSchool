# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from employee import employee
from season import Season
from phone import phone
from datetime import date

class  Candidate(employee):
    """Candidate"""
    def __init__(self,
                 caid=None,
                 eid=None,
                 firstname=None,
                 lastname=None,
                 suffix=None,
                 nickname=None,
                 sex=None,
                 dob=None,
                 passed=None,
                 notes=None,
                 hire=None,
                 classranking=None,
                 discipline=None,
                 phone_cell=None,
                 said=None,
                 cat=None,
                 db_handle=None):
        """Create New Instanace of Candidate"""
        employee.__init__(self,
                          eid=eid,
                          firstname=firstname,
                          lastname=lastname,
                          suffix=suffix,
                          nickname=nickname,
                          sex=sex,
                          dob=dob,
                          db_handle=db_handle)
        self.caid = caid
        self._passed = passed
        self.notes=notes
        self._hire=hire
        self._classranking=classranking
        self._discipline=discipline
        self.said = Season(db_handle=self.db_handle, said=said)
        self.phone = phone(db_handle=self.db_handle, number=phone_cell)
        self.cat = Candidate_Type(cat, db_handle=self.db_handle)
        self.Menu = Menu('Candidate Menu', db_handle=self.db_handle)
              
    def __str__(self):
        return "Candidate: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Candidate: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def classranking(self, display=False, pad=10):
        V = self._classranking
        if display:
            if self._classranking!=None:
                V = str(self._classranking).ljust(pad)
            else:
                V = ''.ljust(pad)
        return V
     
    def discipline(self, display=False, pad=10):
        if display:
            if self._discipline==1:
                v = 'Ski'.ljust(pad)
            elif self._discipline==2:
                v = 'SB'.ljust(pad)
            elif self._discipline==3:
                v = 'Tele'.ljust(pad)
            elif self._discipline==4:
                v = 'Xcountry'.ljust(pad)
            elif self._discipline==5:
                v = 'Race'.ljust(pad)
            else:
                v = ''.ljust(pad)
        else:
            v = self._discipline
        return v
 
    def det_cat(self, options=None):
        if options[1]:
            cat = options[1]
        elif len(options[2])>0:
            type = " ".join(options[2])
            
    def get_age(self, options=None):
        if options[1]:
            age = options[1]
        else:
            try:
                age = int(raw_input('How old today: '))
            except:
                return 0
        self.DOB.set_age(age)
        
    def get_classranking(self, options=None):
        rank = None
        if options[1]:
            rank = options[1]
        while not rank==None:
            try:
                rank = raw_input('Eanter rank(Yes/No): ').upper()
            except:
                rank = None
        self._class_ranking = rank
    
    def get_discipline(self, options=None):
        d = None
        while d==None:
            if len(options[2])>0:
                d = options[2].pop().upper()
            else:
                d = raw_input('Enter disapline (ski,sb,tele,x-ski,race): ').upper()
            if d=='SKI':
                self._discipline = 1
            elif d=='SB':
                self._discipline = 2
            elif d=='TELE':
                self._discipline = 3
            elif d=='X-SKI':
                self._discipline = 4
            elif d=='RACE':
                self._discipline = 5
            elif d=='':
                return
            else:
                d=None
                    
    def get_hire(self, options=None):
        hire = None        
        while hire==None:
            try:
                if len(options[2])>0:
                    hire = options[2][0].upper()
                    options[2].pop()
                    print(hire)
            
                if hire==None:
                    hire = raw_input('Enter Hire(Yes/No): ').upper()
                if hire=='YES':
                    hire=1
                elif hire=='NO':
                    hire=0
                elif hire=='CLEAR':
                    self._hire = None
                    return 
                else:
                    hire=None
            except:
                hire = None
            
        self._hire = hire
        if self._hire:
            hire_date = date.today()
            results = self.db_handle.fetchdata('add_employee_start', [self.eid ,hire_date])
    
    def get_passed(self, options=None):
        passed = None
        while passed==None:
            try:
                if len(options[2])>0:
                    passed = options[2][0].upper()
                    options[2].pop()
                if passed==None:
                    passed = raw_input('Enter Passed (Yes/No): ').upper()
                if passed=='YES':
                    passed=1
                elif passed=='NO':
                    passed=0
                elif passed=='CLEAR':
                    self._passed = None
                    return
                else:
                    passed=None
            except:
                passed = None
        
        self._passed = passed
        if self._passed:
            if self.discipline()==1:
                ct = 2
            elif self.discipline()==2:
                ct = 3
            results = self.db_handle.fetchdata('add_employee_cert', [self.eid ,ct,])
    
    def hire(self, display=False, pad=10):
        V = self._hire
        if display:
            if self._hire:
                V = 'Yes'.ljust(pad)
            else:
                if self._hire==None:
                    V = ''.ljust(pad)
                else:
                    V = 'No'.ljust(pad)
        return V
        
    def load_candidate_db(self, options=None):
        if self.eid:
            R = self.db_handle.fetchdata('get_candidate', [self.eid,])
            for r in R:
                self.caid = r[0]
                self.eid = r[1]
                self._passed = r[3]
                self._hire = r[5]
                self._classranking = r[6]
                self._discipline = r[7]
                self.notes = r[4]
                self.said.said = r[2]
            
                if self.said.said:
                    self.said.get_season_db()
                
    def menu(self, options=None):
        M = self.Menu
        M.add_item('Passed', 'Passed <YES/NO> - Menu test item', self.get_passed)
        M.add_item('Hire', 'HIRE <YES/NO> - set Hire status', self.get_hire)
        M.add_item('Discipline', 'DISCIPLINE <ski/sb> - set disapline.', self.get_discipline)
        M.add_item('Name', 'NAME <fristname> <lastname> <suffix> <nickname> - set name.', self.set_name)
        M.add_item('DOB', 'DOB <date> - set date of birth for canidate.', self.DOB.get_date)
        M.add_item('SEX', 'SEX <male/female> - set sex of canidate.', self.set_sex)
        M.add_item('SAVE', 'SAVE - Save the record in the database.', self.save_candidate_db)
        M.add_item('Phone', 'PHONE <number> - set the phone number in the database.', self.phone.set_phone)
        M.add_item('Age', 'AGE <integer> - set dob as to with age of' , self.get_age)
        M.menu_display = self.print_menu
        M.Menu()
    
    def passed(self, display=False, pad=10):
        if display:
            if self._passed:
                v = 'Yes'.ljust(pad)
            elif self._passed==None:
                v = "".ljust(pad)
            else:
                v = 'No'.ljust(pad)
        else:
            v = self._passed
        return v
        
    def print_menu(self):
        print("""
    Season:        %s
    Class Ranking: %s
    caid:          %s
    EID:           %s
    Name:          %s
    Age:           %s
    Sex:           %s
    Disapline:     %s
    Phone:         %s
    Passed:        %s
    Hired:         %s""" % (self.said.season_name(),
                            self.classranking(True),
                            self.caid,
                            self.eid,
                            self.name(nickname=True),
                            self.DOB.age(adult=True),
                            self.sex,
                            self.discipline(True),
                            self.phone.number(False),
                            self.passed(True),
                            self.hire(True),
                            ))
        
    def print_self(self):
        print("""    %s %s %s %s %s %s %s %s""" % (self.classranking(True,5),
                                                str(self.caid).ljust(5),
                                                str(self.eid).ljust(5),
                                                str(self.name(nickname=True)).ljust(40), 
                                                self.passed(True, 5),
                                                self.hire(True, 5),
                                                self.age(True),
                                                self.discipline(True)))
    
    def save_candidate_db(self, options=None):
        if self.caid:
            self.db_handle.fetchdata('update_candidate', [])
        else:
            R = self.db_handle.fetchdata('add_candidate', [self.firstname(),
                                                           self.lastname(),
                                                           self._suffix,
                                                           self._nickname,
                                                           self.sex,
                                                           self.DOB.date(True),
                                                           self.phone.number(),
                                                           self.discipline(),
                                                           ])
            if R[0][0]==0:
                raw_input('Candidate not added')    
    
    def set_passed(self, passed=None):
        if passed:
            self._passed = passed
            
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Candidate
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
  
class Candidate_Type(object):
    def __init__(self,
                 cat=None,
                 candidate_type=None,
                 db_handle=None):
        self.set_db_handle(db_handle)
        self.cat = cat
        self.cadidate_type = candidate_type
        
    def load_candidate_type_db(self):
        pass
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Candidate_type')
        self.db_handle = db_handle
     
        
if __name__ == "__main__":
    from login import Login
    L = Login(login='halc')
    N = Candidate(db_handle=L.db_handle)
    #N.load_candidate_db()
    #N.load_emp_db()
    #N.print_menu()
    N.menu()
    #N.About()