# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from training import Training
from season import Season

class  Trainings(object):
    """Trainings"""
    Training.index = 1
    Training.object = 2
    Training.id = 3

    def __init__(self, db_handle=None):
        """Create New Instanace of Trainings"""
        self.set_db_handle(db_handle)
        self.trainings = []
        self.said = Season(db_handle=self.db_handle)
        self.said.get_current_season_id()
        self.said.get_season_db()
        self.database_function = 'get_season_open_tlid'
        self.Menu = Menu('', db_handle=self.db_handle)
            
    def __str__(self):
        return "Trainings: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Trainings: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def __len__(self):
        return len(self.trainings)
    
    def append(self, trainings):
        self.trainings.append(trainings)
        self.sort()
        
    def checkID(self, tlid, return_type=Training.object):
        i = 0
        for o in self.trainings:
            if o.tlid==tlid:
                if return_type==Training.index:
                    return i
                elif return_type==Training.object:
                    return o
                elif return_type==Training.id:
                    return o.tlid
            i += 1
        return None

    def clear(self):
        self.trainings = []
    
    def edit_training(self, options=None):
        if options[1]:
            tlid = options[1]
        else:
            try:
                tlid = int(raw_input('Enter tlid to edit: '))
            except:
                return
        T = self.checkID(tlid, Training.object)
        T.menu()
        
    def get_training_headers(self):
        self.clear()
        R = self.db_handle.fetchdata(self.database_function, [self.said.said])
        for r in R:
            T = Training(tlid=r[0], db_handle=self.db_handle)
            T.load_training_header_db()
            T.Roster.get_employees_db()
            self.append(T)

    def lock_training(self, options=None):
        if options[1]:
            tlid = options[1]
        else:
            try:
                tlid = int(raw_input('Enter tlid: '))
            except:
                return
        R = self.db_handle.fetchdata('lock_roster', [tlid,])
        if R[0][0]==0:
            raw_input('header not found okay? ')
        
    def menu(self):
        M = self.Menu
        M.menu_display = self.print_menu
        M.add_item('New', 'New - Add a new training', self.new_training)
        M.add_item('Edit', 'EDIT <tlid> - Edit a training header', self.edit_training)
        M.add_item('Delete', 'DELETE <tlid> - Delete a Training Header', M.print_new)
        M.add_item('Lock', 'Lock <tlid> - Lock a Training Header form edits', self.lock_training)
        M.add_item('All','All <said> - List all trainings for a season', self.set_all)
        M.add_item('Open', 'OPEN - List only open trainins for a season', self.set_open)
        M.add_item('Find', 'FIND - Advanced search for training headers', M.print_new)
        M.add_item('Season', 'SEASON - Set Season', self.set_season)
        M.Menu()
    
    def new_training(self, options=None):
        T = Training(db_handle=self.db_handle)
        T.menu()
    
    def print_menu(self):
        self.get_training_headers()

        print("""%s
    TLID Date         Training Title                    Trianing Location          Count      Lead Instructor
    ---- ------------ --------------------------------- -------------------------- ---------- -----------------------"""
        % (self.said.season_name().center(85, " ")))
        self.print_list()
        print("""    -----------------------------------------------------------------------------------------------------------------
    Count: %s""" % (len(self)))
            
    def print_list(self):
        i = 0
        for c in self.trainings:
            c.print_self()
            i=+1
    
    def set_all(self, options=None):
        self.database_function = 'get_season_tlid'
    
    def set_open(self, options=None):
        self.database_function = 'get_season_open_tlid'
        
    def set_season(self, options=None):
        if options[1]:
            said = options[1]
        else:
            try:    
                said = int(raw_input('Enter season id: '))
            except:
                return
        self.said.said = said
        self.said.get_season_db()
        
    def sort(self):
        sort1 = sorted(self.trainings, key=self.sort_key_title)
        self.trainings = sorted(sort1, key=self.sort_key_date)
    
    def sort_key_date(self, i):
        return i.training_date.date(True)

    def sort_key_title(self, i):
        return i.training_title(0)
    
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Trainings
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Trainings')
        self.db_handle = db_handle
        
        


if __name__ == "__main__":
    from login import Login
    L = Login(login='halc')
    L.Login()
    N = Trainings(db_handle=L.db_handle)
    N.print_menu()
    #N.menu()
    #N.About()