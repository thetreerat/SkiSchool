# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from date import date
from menu import Menu
from season import Season

class  Seasons(object):
    """Seasons"""
    def __init__(self, db_handle=None):
        """Create New Instanace of New Class"""
        self.set_db_handle(db_handle)
        self.seasons = []
        
    
    def __str__(self):
        return "Seasons: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Seasons: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Seasons
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")

    def append(self, s, sort=True):
        """Add season object to seasons list, and resort list """
        if self.checkName(s.season_name)==None:
            self.seasons.append(s)
            self.seasons.sort(key=self.sort_person_key)

    def checkID(self, said):
        for s in self.seasons:
            if s.said==said:
                return i
        return None
    
    def checkName(self, season_name):
        for s in self.seasons:
            if s.season_name()==season_name:
                return s
        return None
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Seasons')
        self.db_handle = db_handle
        
    def sort(self):
        se_date = sorted(self.seasons, key=self.sort_key_end)
        self.seasons = sorted(se_date, key=self.sort_key_start)
    
    def sort_key_end(self, s):
        return s.se_date.Date(True)
    
    def sort_key_start(self, s):
        return i.ss_date.Date(True)
    
        


if __name__ == "__main__":
    N = Seasons()
    N.About()