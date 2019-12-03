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
        self.update = False
        self.set_new()
        self.Menu = Menu('Season Menu', db_handle=self.db_handle)

    
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
        
    def add_db(self, options=None):
        """Add shift object to the shift table in database"""
        result = self.db_handle.fetchdata('add_season', [self.season_name(),
                                                        self.ss_date.date(True),
                                                        self.se_date.date(True),
                                                       ]
                                         )
        self.said = result[0][0]
        self.set_update(False)
    
    def get_said(self, options=None):
        said = None
        if options[1]:
            said = options[1]
        else:
            while not said:
                try:
                    said = int(raw_input('Enter season ID: '))
                except:
                    said = None
                if said=='':
                    return 0
        self.said = said
        self.get_season_db()
        
    def get_season_db(self):
        if self.said:
            result = self.db_handle.fetchdata('get_seasons', [self.said, ])
            for r in result:
                #self.said = r[0]
                self._season_name = r[3]
                self.ss_date.set_date(r[1])
                self.se_date.set_date(r[2])
    def menu(self, options=None):
        SMenu = self.Menu
        SMenu.menu_display = self.print_self
        SMenu.add_item('Season', 'set/update Season display name', self.set_season_name)
        SMenu.add_item('Start', 'set season start date', self.set_ss_date)
        SMenu.add_item('End', 'set season end date', self.set_se_date)
        SMenu.Menu()
        
    def season_name(self):
        """Return season name"""
        if self._season_name:
            return self._season_name
        else:
            return ""

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Season')
        self.db_handle = db_handle

    def set_new(self, value=None):
        if value==None:
            if self.said==None:
                self.new = True
            else:
                self.new = False
        else:
            self.new = value
    
    def set_season_name(self, options=None):
        """Set the season name for season."""
        if self._season_name!=None:
            print(self._season_name)
            answer = raw_input('Change (yes/No)? ')
            if answer[0].upper()!='Y':
                #self.set_update(True)
                return
        self._season_name = raw_input("""Enter Season Display Name(%s): """ % self._season_name)
        self.set_update(True)

    def set_se_date(self, options=None):
        self.se_date.get_date(options)
        self.set_update(True)
    
    def set_ss_date(self, options=None):
        self.ss_date.get_date(options)
        self.set_update(True)
            
    def set_update(self, value):
        if value:
            if not self.update:
                M = self.Menu
                if not self.new:
                    M.add_item('Update', 'UPDATE - Update database with changes', self.update_db)
                else:
                    M.add_item('Save', 'SAVE - Add record to the database', self.add_db)
        else:
            pass
            #M.delete_item('Update')
            #Need to update menu 
        self.update = value

    def get_current_season_id(self):
        result = self.db_handle.fetchdata('get_current_season', [])
        for r in result:
            self.said = r[0]
        return self.said
                
    def print_self(self):
        print('Season Name: %s' % self._season_name)
        print('Season Start: %s' % self.ss_date.date(True))
        print('Season End: %s' % self.se_date.date(True))
    
    def update_db(self, options=None):
        self.db_handle.fetchdata('', [self.said,
                                      self.season_name,
                                      self.ss_date.date(True),
                                      self.se_date.date(True),])
        self.set_update(False)

if __name__ == "__main__":
    db_handle = database(owner='season.py - __main__')
    N = Season(db_handle)
    #N.get_season_db(4)
    N.menu()
    N.About()