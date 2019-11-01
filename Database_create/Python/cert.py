# Author: Harold Clark
# Copyright Harold Clark 2019
#
import sys
import os
from database import database
from skitime import SkiTime
from date import date
from menu import Menu
from datetime import datetime

class cert(object):
    """Cert Object """
    def __init__(self, ct=None, cert_name=None, cert_org=None, db_handle=None):
        self.cid = None
        self.ct = ct
        self.cert_date = None
        self.cert_current = True
        self.cert_name = cert_name
        self.cert_org = cert_org
        self.html_class = None
        self.update = False
        self.min_eq = []
        if db_handle==None:
            print('New database handle created at __init__ cert')
            db_handle = database()
        self.db_handle = db_handle
        
    def Bool_test(self, item, print_return):
        if print_return=='Print':
            if item==1:
                item = 'Yes'
            else:
                item= 'No'
        return item
            
    def edit(self):
        run = True
        while run:
            os.system('clear')
            self.print_cert(print_return='Long')
            self.print_edit_selection()
            answer = raw_input('Enter Selection: ').upper()
            while answer:
                if answer in ['EXIT']:
                    if self.update: self.update_cert_db()
                    sys.exit(1)
                elif answer in ['ORG']:
                    self.cert_org = raw_input('Enter name of Organization (%s): ' % (self.cert_org))
                    self.update = True
                    break
                elif answer in ['NAME']:
                    self.cert_name = raw_input('Enter Certificatoin Name: ')
                    self.update = True
                    break
                elif answer in ['RETURN']:
                    run = False
                    if self.update: self.update_cert_db()
                    break
                elif answer in ['REVERT']:
                    #need to reload data from database
                    self.update = False
                    break
                else:
                    print(self.ct)
                    dump = raw_input('Lost in space, %s not valid' % answer)
                    break
        
    def add_new(self):
        self.cert_name = raw_input('Enter Cert Name: ')
        self.cert_org = raw_input('Eneter Cert Org: ')
        cert_min = raw_input('Are there any certifications equivalent to this one (yes/no) ')
        if cert_min=='YES':
            pass
            #need to make update eq
        
            
        dump = raw_input('add new - ready?')
        pass
    
    def assign_cert(self, eid):
        result = self.db_handle.fetchdata('add_employee_cert', [eid, self.ct, self.cert_current, self.cert_date.strftime('%m/%d/%y')])
    
    def load_cert_db(self):
        if self.ct!=None:
            result = self.db_handle.fetchdata('get_cert', [self.ct])
            for r in result:
                self.cert_org = r[2]
                self.cert_name = r[1]
                
    def pad(self, item, length):
        
        if item==None:
            item = ''
            for l in range(length):
                item = item + chr(32)
        else:
            length = length - len(item)
            for l in range(length):
                item = item + chr(32)
        return item
        
    def print_cert(self, print_return='Print', count=None):
        """Print or return cert object in printable string form"""
        if print_return=='find':
            print( """    %s %s %s""" %(count.ljust(6),self.cert_name.ljust(40),self.cert_org ))
         
        elif print_return=='Long':
            print("""    CT                         - %s
    Certification Name         - %s
    Certificatoin Organization - %s""" % (self.ct,
                                  self.cert_name,
                                  self.cert_org))
            
        else:
            if self.cert_date==None:
                cert_date = ''
            else:
                cert_date = self.cert_date.strftime("%m/%d/%y")
            status = self.Bool_test(self.cert_current, print_return)
            cert = """    %s %s     %s """ % (self.cert_name.ljust(24), cert_date.ljust(9), status)
            if print_return=='Print':
                print(cert)
            else:
                return cert

    def print_edit_selection(self):
        if self.update:
            save = "Save and "
        else:
            save = ''
        print("""
    -----------------------------------------------
    ORG    - Certification Organization
    NAME   - Certification Name
    EXIT   - %sExit to System Prompt
    RETURN - %sReturn to Previous 
    REVERT - Revert to Database Values
    -----------------------------------------------""" % (save, save))
                
    def update_cert_db(self):
        pass
    
class certs(object):
    cert.index = 1
    cert.object = 2
    cert.cid = 3
    cert.title = 4

    """Cert List Object"""
    def __init__(self, eid=None, list_type=None, db_handle=None):        
        """init Cert List Object"""
        self.set_db_handle(db_handle)
        self.clist = []
        self.eid = eid
        self.list_type = list_type
        
    def add(self, item_index=False, options=None):
        """add new cert to list"""
        if self.list_type in ['Employee','EditEmp']:
            if self.eid!=None:
                if not item_index:
                    item_index = self.get_item_index()
                cdate = now.strftime('%d/%m%Y')
                adate = raw_input('Enter Date of Certification (%s)' % (cdate))
                if adate=='':
                    adate = cdate
                self.alist[item_index].cert_date = adate
                acurrent = raw_input('Is Certification current (YES/NO)?').upper()
                if acurrent[0]=='Y':
                    self.alist[item_index].cert_current = True
                else:
                    self.alist[item_index].cert_current = False
            
                self.alist[item_index].assign_cert(self.eid)
                
    def checkID(self, ID):
        """check to list for ID"""
        for i in self.slist:
            if i.cid==ID:
                return i
        return None

    def edit_cert(options=None):
        """edit a cert"""
        print(options)
        #self.clist[Item_index].edit()


    def get_item_index(self):
        run = True
        while run: 
            try:
                run = False
                Item_index = int(raw_input('Enter line number: '))
            except:
                print('Invalid line number')
                run = True
        return Item_index
    
    def menu(self, options=None):
        """Menu for editing certs"""
        m = Menu('Manage employee Certification Menu', db_handle=self.db_handle)
        m.menu_display = self.print_certs
        if self.list_type=='Cert':
            m.add_item('Add', 'ADD - Add a new cert to the availabile list of certs', m.print_new) # self.add_cert(options=None)
            m.add_item('EDIT', '', m.print_new) # self.edit_item(options=None)
        elif self.list_type in ['Employee', 'EditEmp']:
            m.add_item('ADD', 'ADD <#> or ADD <title> - add a cert by ct(cert template id) or add a cert by title.', m.print_new)
            m.add_item('Delete', 'DELETE <#> or DELETE <title> - delete cert by index(0-X) or title.', m.print_new)
            m.add_item('Find', 'Find a cert in database', m.print_new)
        m.Menu()
        
    def print_title(self):
        if self.list_type=='Employee':
            title = ''
        elif self.list_type=='EditEmp':
            title = ''
        elif self.list_type=='cert':
            title = """    Certs matching search ...%s
"""
        else:
            title = ''
        return title

    def print_certs(self):
        """print cert list"""
        count = 0
        title = self.print_title()
        if self.list_type=='Employee':
            print("""    Cert Title               Cert Date          Current
    ------------------------ ------------- ----------""")
            for c in self.clist:
                c.print_cert()
            print("""    ------------------------------------------------------""")
        
        elif self.list_type in ['cert', 'EditEmp']:
            print("""%s    line Cert Title               Organization
    ---- ------------------------ -------------------""" % (title))
            for c in self.clist:
                c.print_cert(print_return='find', count=str(count))
                count += 1
                
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='cert.py - set_db_handle')
        self.db_handle = db_handle
        
    def get_employee_certs_db(self):
        if self.eid!=None:
            result = self.db_handle.fetchdata('get_employee_certs', [self.eid,])
            for r in result:
                c = cert(db_handle=self.db_handle)
                c.cid = r[0]
                c.ct = r[1]
                c.cert_date = r[4]
                c.cert_current = r[5]
                c.cert_name = r[2]
                c.cert_org = r[3]
                self.clist.append(c)
    
    def find_certs_db(self, organization=None, title=None):
        self.clear()
        result = self.db_handle.fetchdata('find_certs', [organization, title,])
        for r in result:
            c = cert(ct=r[0], cert_name=r[1], cert_org=r[2], db_handle=self.db_handle)
            self.clist.append(c)
        
    def clear(self):
        self.clist = []

    
class cert_min(object):
    """class object for cert equivalents"""
    def __init__(self, cmid=None,ct=None, ct_min_equal=None, title=None, min_equal_title=None):
        """init of cert_min"""
        self.cmid = cmid
        self.ct = ct
        self.ct_min_equal = ct_min_equal
        self.title = title
        self.min_equal_title = min_equal_title
    
    def print_cert_min(self):
        if self.ct==self.ct_min_equal:
            print("""    %s - %s """ % (self.ct, self.title))
        else:
            print("""        %s - %s""" % (self.ct_min_equal, self.min_equal_title))

class cert_mins(object):
    def __init__(self, db_handle=None):
        self.mlist = []
        if db_handle==None:
            print('New database handle created at __init__ cert_min')
            db_handle = database()
        self.db_handle = db_handle
    
    def checkID(self, ID):
        """ check list for CMID and return that cert_min object"""
        for i in self.mlist:
            if i.cmid==ID:
                return i
        return None
    
    def print_list(self):
        """Print list of min certs """
        for m in self.mlist:
            m.print_min_cert()
    """ """
    

class cert_search(object):
    def __init__(self,
                 ct=None,
                 cid=None,
                 title=None,
                 org=None,
                 cmid=None):
        """init a serach object for certs"""
        self.ct = ct
        self.cid = cid
        self.title=title
        self.org = org
        self.cmid = cmid
        
if __name__ == '__main__':
    certs = certs(list_type='Employee', eid=15)
    certs.get_employee_certs_db()
    certs.menu()
