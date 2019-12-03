# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from certtemplate import Cert
from employee import employee
from date import date

class  EmployeeCert(Cert):
    """EmployeeCert"""
    def __init__(self,
                 ct=None,
                 cert_name=None,
                 cert_org=None,
                 html_class=None,
                 cid=None,
                 cert_current=None,
                 db_handle=None):
        """Create New Instanace of EmployeeCert"""
        Cert.__init__(self,
                      ct=ct,
                      cert_name=cert_name,
                      cert_org=cert_org,
                      html_class=html_class,
                      db_handle=db_handle)
        if self.ct:
            self.load_cert_db()
        self.eid = employee(eid=eid, db_handle=self.db_handle)
        if self.eid:
            self.eid.load_emp_db()
        self.cid = cid
        self._cert_current = cert_current
        self.cert_date = date(db_handle=self.db_handle)
        self.Menu = Menu('Employee Certification Menu', db_handle=self.db_handle)
    
    def __str__(self):
        return "EmployeeCert: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "EmployeeCert: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    
    def cert_current(self, display=False, pad=10):
        if display: 
            if self._cert_current:
                return "Yes".ljust(pad)
            elif self._cert_current==0:
                return "No".ljust(pad)
            else:
                return "".ljust(pad)
        else:
            return self._cert_current
    
    def get_cert_current(self, options=None):
        cert_current = None
        if len(options[2]):
            cert_current= " ".join(options[2])
        while not cert_current:
            try:
                cert_current = raw_input('Is the certification current <Yes/No> : ').upper() #if cert_current is integer
            except:
                cert_current = None
            if cert_current=="":
                return 0
        if cert_current=='YES':
            cert_current = True
        else:
            cert_current = False
        self.set_cert_current(cert_current)
    
    def load_EmployeeCert_db(self, options=None):
        R = self.db_handle.fetchdata('get_EmployeeCert', [self.cid,])
        for r in R:
            self.set_cert_current(r[1])
        
    def menu(self, options=None):
        M = self.Menu
        M.add_item('Current', 'Current <yes/no> - set current status of certification', self.get_cert_current)
        M.menu_display = self.print_menu
        M.Menu()
        
    def print_menu(self):
        print("""
    cid:          %s
    ct:           %s
    Title:        %s
    Organization: %s
    Issue Date:   %s
    Current: %s""" % (self.cid,
                      self.ct,
                      self.cert_name(),
                      self.cert_org(),
                      self.cert_date.date(True),
                      self.cert_current()))
        
    def print_self(self):
        print("""    %s %s %s %s""" % (self.cid,
                                 self.cert_current()))
    
    def set_cert_current(self, cert_current=None):
        if cert_current!=None:
            self._cert_current = cert_current
            
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : EmployeeCert
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
        


if __name__ == "__main__":
    from login import Login
    L = Login(login='halc')
    L.Login()
    
    N = EmployeeCert(db_handle=L.db_handle, cid=1)
    N.load_Cert_db()
    N.print_menu()
    #N.menu()
    #N.About()