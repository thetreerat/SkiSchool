# Author: Harold Clark
# Copyright Harold Clark 2019
#
import sys
import os
from database import database
from datetime import datetime

class cert(object):
    """Cert Object """
    def __init__(self, ct=None, cert_name=None, cert_org=None):
        self.cid = None
        self.ct = ct
        self.cert_date = None
        self.cert_current = True
        self.cert_name = cert_name
        self.cert_org = cert_org
        self.html_class = None
        self.update = False
        self.min_eq = []
        
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
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('add_employee_cert', [eid, self.ct, self.cert_current, self.cert_date.strftime('%m/%d/%y')])
        ski_db.close()
    
    def load_cert_db(self):
        if ct!=None:
            ski_db = database
            #result = ski_db.call_ski_proc('get_cert', [self.ct])
            #for r in result:
            #    self.cert_org = r[1]
            #    self.cert_name = r[2]
                
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
    """Cert List Object"""
    def __init__(self, eid=None, list_type=None):
        
        """init Cert List Object"""
        self.clist = []
        self.eid = eid
        self.list_type = list_type

    def add(self, item_index=None, options=None):
        """add new cert to list"""
        if self.list_type=='Employee':
            
        pass
                
    def checkID(self, ID):
        """check to list for ID"""
        for i in self.slist:
            if i.cid==ID:
                return i
        return None

    def answer_split(self, answer):
        count = 0
        Item_index=False
        Main = False
        Action = False
        options = []
        answer = list(answer.split())
        while len(answer)==0:
            a = answer.pop(0)
            test = a.upper()
            if test in ['ADD', 'AD', 'A']:
                Action = 'ADD'
            elif test in ['CERT', 'CER', 'CE', 'C']:
                Main = 'CERT'
            elif test in ['DELETE', 'DELET', 'DELE', 'DEL', 'DE','D']:
                Action = 'DELETE'            
            elif test in ['EDIT', 'EDI', 'ED']:
                Action = 'EDIT'
            elif test in ['EXIT','EXI','EX']:
                Action = 'EXIT'
            elif test=='E':
                if Main=='CERT':
                    Action='EDIT'
                elif count<1:
                    Action = 'E'
                else:
                    options.append(a)
            else:
                try:
                    Item_index = int(a)
                except:
                    options.append(a)
            count += 1
        return (main,Action, item_index, options)
    
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
    
    def menu(self):
        """Menu for editing certs"""
        run = True
        while run:
            os.system('clear')
            self.print_certs()
            self.print_menu()
            (main,Action, item_index, options) = self.answer_split(raw_input('Enter selection: '))            
            while Action:
                if Action=='EXIT':
                    sys.exit(1)
                elif Action=='EDIT':
                    if self.list_type=='CERT':
                        self.clist[Item_index].edit()
                    break
                
                elif Action=='E':
                    (main,Action, item_index, options) = self.answer_split(raw_input('EXIT or EDIT #'))

                elif Action=='ADD':
                    a = cert()
                    self.add(answer)
                    break
                                
                elif answer[0] in ['RETURN','RETUR','RETU','RET','RE','R']:
                    run=False
                    break
                else:
                    print("""Lost in space!!!""")
                    print(answer)
                    dump = raw_input('ready?')
                    break


    
    def print_menu(self):
        print("""    add, edit, return, exit, help
    --------------------------------------------------------
              """)
    
    def print_title(self):
        if self.list_type=='Employee':
            title = ''
        elif self.list_type=='EditEmp':
            title = ''
        elif self.list_type=='cert':
            title = """    Certs matching search ...%s
"""
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

    def get_employee_certs_db(self):
        if self.eid!=None:
            ski_db = database()
            ski_db.connect()
            ski_db.cur.callproc('get_employee_certs', [eid,])
            result = ski_db.cur.fetchall()
            for r in result:
                c = cert()
                c.cid = r[0]
                c.ct = r[1]
                c.cert_date = r[4]
                c.cert_current = r[5]
                c.cert_name = r[2]
                c.cert_org = r[3]
                self.clist.append(c)
            ski_db.close()
    
    def find_certs_db(self, organization=None, title=None):
        self.clear()
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('find_certs', [organization, title,])
        result = ski_db.cur.fetchall()
        for r in result:
            c = cert(ct=r[0], cert_name=r[1], cert_org=r[2])
            self.clist.append(c)
        ski_db.close()
        
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
    def __init__(self):
        self.mlist = []
    
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
            
if __name__ == '__main__':
    certs = certs()
    #certs.get_employee_certs_db(15)
    certs.find_certs_db(organization='Bristol', title='%')
    certs.list_type='EditEmp'
    certs.menu()
    #certs.print_certs('find')