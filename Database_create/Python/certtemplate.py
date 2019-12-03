# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu


class  Cert(object):
    """Certification Template Class"""
    def __init__(self,
                 ct=None,
                 cert_name=None,
                 cert_org=None,
                 html_class=None,
                 db_handle=None):
        """Create New Instanace of Cert"""
        self.set_db_handle(db_handle)
        self.ct = ct
        self._cert_name = cert_name
        self._cert_org = cert_org
        self._html_class = html_class
        self.Menu = Menu('Cert Template Menu', db_handle=self.db_handle)
    
    def __str__(self):
        return "Cert: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "Cert: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
        
    def cert_name(self, pad=10):
        if self._cert_name:
            return self._cert_name.ljust(pad)
        else:
            return "".ljust(pad)
    
    def cert_org(self, pad=0):
        if self._cert_org:
            return self._cert_org.ljust(pad)
        else:
            return "".ljust(pad)

    def html_class(self, pad=0):
        if self._html_class:
            return self._html_class.ljust(pad)
        else:
            return "".ljust(pad)

    def get_cert_org(self, options=None):
        org = None
        if len(options[2])>0:
            org = " ".join(options[2])
        while not org:
            try:
                org = raw_input('Enter organization name: ')
            except:
                org = None
            if org=='':
                return 0
        self.set_cert_org(org)
    
    def get_html_class(self, options=None):
        h = None
        if len(options[2])>0:
            h = " ".join(options[2])
        while not h:
            try:
                h = raw_input('Enter HTML Class: ')
            except:
                h = None
            if h=='':
                return 0
        self.set_html_class(h)
        
    def get_cert_name(self, options=None):
        cert_name = None
        if len(options[2])>0:
            cert_name = " ".join(options[2])
        while not cert_name:
            try:
                cert_name = raw_input('Enter Certification Name: ')
            except:
                cert_name = None
            if cert_name=="":
                return 0
        self.set_cert_name(cert_name)
    
    def load_Cert_db(self, options=None):
        R = self.db_handle.fetchdata('get_Cert', [self.ct,])
        for r in R:
            self.set_cert_name(r[1])
            self.set_cert_org(r[2])
            self.set_html_class(r[3])
                   
    def menu(self, options=None):
        M = self.Menu
        M.add_item('Title', 'TITLE <string> - Set certification title.', self.get_cert_name)
        M.add_item('Org', 'ORG <string> - Enter Issuing organization.', self.get_cert_org)
        M.add_item('HTML', 'HTML <string> - Enter html class for Certification, change with care.', self.get_html_class)
        M.menu_display = self.print_menu
        M.Menu()
        
    def print_menu(self):
        print("""
    ct:           %s
    Title:        %s
    Organization: %s
    HTML Class:   %s""" % (self.ct,
                           self.cert_name(),
                           self.cert_org(),
                           self.html_class()))
        
    def print_self(self, i=None):
        if i:
            print("""    %s %s %s """ % (str(i).ljust(6),
                                         self.cert_name(40),
                                 self.cert_org()))
        else:
            print("""%s %s %s """ % (str(self.ct).ljust(6),
                                     self.cert_name(40),
                                     self.cert_org()))
    
    def save_db(self, options=None):
        if self.ct:
            r = self.db_handle.fetchdata('add_cert_template', [self.cert_name,
                                                               self.cert_org,
                                                               self.html_class,])
        pass
        
    def set_cert_name(self, cert_name=None):
        if cert_name:
            self._cert_name = cert_name
    
    def set_cert_org(self, org=None):
        if org:
            self._cert_org = org

    def set_html_class(self, h=None):
        if h:
            self._html_class = h

    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='Cert')
        self.db_handle = db_handle
        
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : Cert
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")
        


if __name__ == "__main__":
    from login import Login
    L = Login(login='halc')
    L.Login()
    C = Cert(db_handle=L.db_handle, ct=3)
    C.load_Cert_db()
    #C.print_menu()
    C.menu()
    #C.About()