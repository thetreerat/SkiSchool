# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from candidate import Candidate
from season import Season

class  Candidates(object):
    """Candidates"""
    Candidate.index = 1
    Candidate.object = 2
    Candidate.id = 3

    def __init__(self, db_handle=None, said=None):
        """Create New Instanace of Candidates"""
        self.set_db_handle(db_handle)
        self.Candidate = []
        self.said = Season(db_handle=self.db_handle, said=said)
        if self.said.said==None:
            self.said.get_current_season_id()
            self.said.get_season_db()
        self.Menu = Menu('', db_handle=self.db_handle)
        
    
    def __str__(self):
        return "Candidates: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Candidates: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def __len__(self):
        return len(self.Candidate)
    
    def add_candidate(self, options=None):
        C = Candidate(db_handle=self.db_handle)
        C.menu()
        
    
    def append(self, Candidate):
        self.Candidate.append(Candidate)
        self.sort()
    
    def checkEID(self, eid, return_type=Candidate.object):
        i = 0
        for o in self.Candidate:
            if o.eid==eid:
                if return_type==Candidate.index:
                    return i
                elif return_type==Candidate.object:
                    return o
            i+=1
        
    def checkID(self, caid, return_type=Candidate.object):
        i = 0
        for o in self.Candidate:
            if o.caid==caid:
                if return_type==Candidate.index:
                    return i
                elif return_type==Candidate.object:
                    return o
            i += 1
        return None
    
    def clear(self):
        self.Candidate = []
    
    def edit_candidate(self, options=None):
        if options[1]:
            O = self.checkID(options[1], Candidate.object)
            O.menu()

    
    def load_current_candidates(self):
        self.clear()
        R = self.db_handle.fetchdata('list_candidates', [self.said.said])
        for r in R:
            C = Candidate(db_handle=self.db_handle,
                          caid=r[0],
                          eid=r[1],
                          said=r[2],
                          passed=r[3],
                          notes=r[4],
                          hire=r[5],
                          classranking=r[6],
                          discipline=r[7])
            C.load_emp_db()
            C.said.get_season_db()
            self.append(C)
            
    def menu(self):
        M = self.Menu
        M.menu_display = self.print_menu
        M.add_item('Add', 'ADD - add new cadidate', self.add_candidate)
        M.add_item('Edit', 'Edit <CAID - edit candidate', self.edit_candidate)
        M.Menu()
                
    def print_menu(self):
        self.load_current_candidates()
        print('Menu print needs info')
        print("-----------------")
        self.print_list()
        print("-----------------")
        print("    Count: %s" % (len(self)))
        
    
    def print_list(self):
        for c in self.Candidate:
            c.print_self()
        
    def sort(self):
        fristsort = sorted(self.Candidate, key=self.sort_key_firstname)
        self.Candidate = sorted(fristsort, key=self.sort_key_lastname)
    
    def sort_key_firstname(self, i):
        return i.firstname()
    
    def sort_key_lastname(self, i):
        return i.lastname()
    
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Candidates
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Candidates')
        self.db_handle = db_handle
        
        


if __name__ == "__main__":
    from login import Login
    L = Login(login='halc')
    L.Login()
    N = Candidates(db_handle=L.db_handle)
    #N.print_menu()
    N.menu()
    #N.About()