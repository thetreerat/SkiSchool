# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from menu import Menu
from certtemplate import Cert

class  CertTemplates(object):
    """CertTemplates"""
    Cert.index = 1
    Cert.object = 2
    Cert.id = 3

    def __init__(self, db_handle=None):
        """Create New Instanace of CertTemplates"""
        self.set_db_handle(db_handle=db_handle)
        self.Templates = []
        self.Menu = Menu('', db_handle=self.db_handle)
            
    def __str__(self):
        return "CertTemplates: db: %s" % (self.db_handle.owner)
        
    def __repr__(self):
        return "CertTemplates: db: %s, pythonID: %s" % (self.db_handle.owner, id(self))
    
    def __len__(self):
        return len(self.Templates)

    def add_template(self, options):
        CT = Cert(db_handle=self.db_handle)
        CT.menu()
        
    def append(self, Template):
        self.Templates.append(Template)
        self.sort()
        
    def checkID(self, ct, return_type=Cert.object):
        i = 0
        for o in self.Templates:
            if o.ct==ct:
                if return_type==Cert.index:
                    return i
                elif return_type==Cert.object:
                    return o
            i += 1
        return None
    
    def clear(self):
        self.Templates = []
    
    def delete_template(self, options=None):
        if options[1]:
            ct = options[1]
        else:
            try:
                ct = int(raw_input('Enter Certification ID (ct): '))
            except:
                return 0
        r = self.db_handle.fetchdata('delete_cert_template', [ct])
        
    def edit_template(self, options=None):
        if options[1]:
            ct=options[1]
        else:
            try:
                ct = int(raw('Enter Certification ID (ct): '))                         
            except:
                return 0
        CT = self.checkID(ct)
        CT.menu()
        
    def get_certs(self):
        R = self.db_handle.fetchdata('list_cert_templates',[])
        for r in R:
            C = Cert(db_handle=self.db_handle,
                     ct=r[0],
                     cert_name=r[1],
                     cert_org=r[2],
                     html_class=r[3])
            self.append(C)
    
    def menu(self, options=None):
        M = self.Menu
        M.menu_display = self.print_menu
        M.add_item('Add', 'ADD - Add a new Certification Templpate', self.add_template)
        M.add_item('Edit', 'EDIT <ct> - Edit a Certification Template', self.edit_template)
        M.add_item('Delete', 'Delete <ct> - Delete a Certification Template', self.delete_template)
        M.Menu()
                
    def print_menu(self):
        self.clear()
        self.get_certs()
        print("""
    ct    Certification Title                   Issuer        html
    ----- ------------------------------------- ------------- ---------------""")
        self.print_list()
        print("""    ------------------------------------------------------------------
    Count: %s""" % (len(self)))
            
    def print_list(self):
        for c in self.Templates:
            c.print_self()
        
    def sort(self):
        self.Templates = sorted(self.Templates, key=self.sort_key_name)
    
    def sort_key_name(self, i):
        return i.cert_name()
    
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : CertTemplates
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(onwer='CertTemplates')
        self.db_handle = db_handle
        
        


if __name__ == "__main__":
    from login import Login
    L = Login(login='halc')
    L.Login()
    N = CertTemplates(db_handle=L.db_handle)
    #N.print_menu()
    N.menu()
    #N.About()