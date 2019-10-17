# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from date import date
from menu import Menu

class  Season(object):
    """init Season"""
    def __init__(self,
                 db_handle=None,
                 said=None,
                 ss_date=None,
                 se_date=None,
                 season_name=None):
        """Create New Instanace of Season"""
        self.set_db_handle(db_handle)
        self.said = said
        self.ss_date = date(ss_date, question_text='Enter Start of Season Date: ', db_handle=self.db_handle)
        self.se_date = date(se_date, question_text='Enter End of Season Date: ', db_handle=self.db_handle)
        self._season_name = season_name
    
    def __str__(self):
        return "Season: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Season: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Season
Inputs         : season_name, ss_date, se_date,said
Returns        : None
Output         : None
Purpose        : Season class 

""")
        
    def add_season_db(self):
        """Add shift object to the shift table in database"""
        result = self.db_handle.fetchdata('add_season', [self.season_name,
                                                        self.ss_date.date(True),
                                                        self.se_date.date(True),
                                                       ]
                                         )
        self.said = result[0][0]
        
    def season_name(self, season_name):
        """Return season name"""
        if self.season_name:
            return self._season_name
        else:
            return ""

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Season')
        self.db_handle = db_handle
        
    def set_season_name(self, season_name):
        """Set the season name for season."""
        if self._season_name!=None:
            print(self._season_name)
            answer = raw_input('Change (yes/No)? ')
            if answer[0].upper()!='Y':
                return
        self._season_name = raw_input("""Enter Season Display Name(%s): """ % self._season_name)        
        
    def print_self(self):
        print('Season Name: %s' % self._season_name)
        print('Season Start: %s' % self.ss_date.date(True))
        print('Season End: %s' % self.se_date.date(True))


if __name__ == "__main__":
    db_handle = database(owner='season.py - __main__')
    N = Season(db_handle)
    SMenu = Menu('Season Menu', db_handle=db_handle)
    SMenu.menu_display = N.print_self
    SMenu.add_item('Season', 'set/update Season display name', N.set_season_name)
    SMenu.add_item('Start', 'set season start date', N.ss_date.get_date)
    SMenu.add_item('End', 'set season end date', N.se_date.get_date)
    SMenu.Menu()
    N.About()