# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from employee import employee
from season import season

class  Candidate(employee):
    """Candidate"""
    def __init__(self,
                 caid=None,
                 firstname=None,
                 lastname=None,
                 nickname=None,
                 sex=None,
                 dob=None,
                 passed=None,
                 notes=None,
                 hire=None,
                 class_ranking=None,
                 discipline=None,
                 db_handle=None):
        """Create New Instanace of Candidate"""
        employee.__init__(self,
                          firstname=firstname,
                          lastname=lastname,
                          suffix=suffix,
                          nickname=nickname,
                          sex=sex,
                          dob=dob,
                          db_handle=db_handle)
        self.caid = caid
        self._passed = passed
        self.notes=notes,
        self._hire=hire,
        self._class_ranking=class_ranking,
        self._discipline=discipline
        self.Menu = Menu('classID Menu', db_handle=self.db_handle)
        
    def __str__(self):
        return "Candidate: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Candidate: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def class_ranking(self, display=False):
        V = self._class_ranking
        if display:
            if self._hire:
                V = str(self._class_ranking).ljust(pad)
            else:
                V = ''.ljust(pad)
        return V
       
    def get_class_ranking(self, options=None):
        rank = None
        if options[1]:
            rank = options[1]
        while not rank==None:
            try:
                rank = raw_input('Enter rank(Yes/No): ').upper()
            except:
                rank = None
        self._rank = rank
        
    def get_hire(self, options=None):
        hire = None
        if options[1]:
            hire = options[1]
        while not hire==None:
            try:
                hire = raw_input('Enter Hire(Yes/No): ').upper()
                if hire=='YES':
                    hire=1
                else:
                    hire=0
            except:
                hire = None
        self._hire = hire
    
    def get_passed(self, options=None):
        passed = None
        if options[1]:
            passed = options[1]
        while not passed:
            try:
                passed = raw_input('Enter Passed (Yes/No): ').upper()
                if passed=='YES':
                    passed=1
                else:
                    passed=0
            except:
                passed = None                
        self._passed = passed
    
    def hire(self, display=False):
        V = self._hire
        if display:
            if self._hire:
                V = 'Yes'
            else:
                V = 'No'
        return V
        
    def load_candidate_db(self, options=None):
        R = self.db_handle.fetchdata('get_candidate', [self.caid,])
        for r in R:
            self.eid = r[1]
            self._passed = r[1]
            self._hire = r[2]
            self._class_rank = r[3]
            self._discipline = r[4]
            self.notes = r[5]
            self.said.said = r[7]
                
    def menu(self, options=None):
        M = self.Menu
        M.add_item('passed', 'passed - Menu test item', self.get_passed)
        M.menu_display = self.print_menu
        M.Menu()
    
    def passed(self, pad=10):
        if self._passed:
            return self._passed.ljust(pad)
        else:
            return "".ljust(pad)
        
    def print_menu(self):
        print("""
    Class Ranking: %s
    caid:           %s
    EID:           %s
    Name:          %s
    Passed:        %s
    Hired:         %s
    Age:           %s""" % (self.class_ranking(True),
                            self.caid,
                            self.eid,
                            self.name(nickname=True), 
                            self.passed(True),
                            self.hire(True),
                            self.age(True)))
        
    def print_self(self):
        print("""    %s %s %s %s %s %s %s""" % (self.class_ranking(True),
                                                self.caid,
                                                self.eid,
                                                self.name(nickname=True), 
                                                self.passed(True),
                                                self.hire(True),
                                                self.age(True)))
    
    def set_passed(self, passed=None):
        if passed:
            self._passed = passed
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Candidate')
        self.db_handle = db_handle
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Candidate
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
        


if __name__ == "__main__":
    N = Candidate()
    N.About()