# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from datetime import datetime

class  person(object):
    """person object"""
    def __init__(self,
                 firstname=None,
                 lastname=None,
                 suffix=None,
                 nickname=None,
                 DOB=None,
                 sex=None,
                 db_handle=None):
        """Create New Instanace of person"""
        self._firstname = firstname
        self._lastname = lastname
        self._suffix = suffix
        self._nickname = nickname
        self.set_DOB(DOB, interactive=False)
        self.sex = sex
        self._Age = None
        self.db_handle = db_handle
        self.set_db_handle(db_handle)

    def age(self, adult=False):
        age = int(int((datetime.now() - self._DOB).days) / 365.2425)
            #calubate age from dob
        if adult:
            if age>18:
                age = 'Adult'
        return age
    
    def DOB():
        return self._DOB
    
    def firstname(self):
        return self._firstname
    
    def lastname(self):
        return self._lastname

    def name(self, nickname=False):      
        """return instructor name first name<sp> last name as string"""
        name = ''
        if self._firstname:
            name = self._firstname
        if self._lastname:
            if len(name)>0:
                name = '%s %s' % (name, self._lastname)
            else:
                name = self._lastname
        if self._suffix:
                name = '%s %s' % (name,self._suffix)
        if nickname and self._nickname:
            name = '%s (%s)' % (name, self._nickname)
        return name
                
    def print_self(self):
        if self._suffix:
            print("""    %s %s %s""" % (self._firstname, self._lastname, self._suffix))
        else:
            print("""    %s %s""" % (self._firstname, self._lastname))

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='person.py - person object')
        self.db_handle = db_handle

    def set_DOB(self, DOB=None, interactive=True):
        """set self._DOB as date"""
        try:   
            self._DOB = datetime.strptime(DOB, '%m/%d/%Y')
        except:
            if interactive:
                self._DOB = datetime.strptime(raw_input('Please enter age (MM/DD/YYYY): '), '%m/%d/%Y')
            else:
                self._DOB = datetime.now()
            
    def set_name(self, options=None, nickname=False):
        """Collect name and set"""
        try:
            db_handle = options[3]
            options = options[2]
        except:
            pass
        if not options:
            try:
                options = list(raw_input('Name: ').split())
            except:
                return
        try:
            icount = len(options)
        except:
            icount = 0
        if icount==4:
            self._firstname = options[0]
            self._lastname = options[1]
            self._suffix = options[2]
            self._nickname = options[3]
        elif icount==3:
            self._firstname = options[0]
            self._lastname = options[1]
            self._suffix = options[2]
            #print('Count 3: %s' % (options))
        elif icount==2:
            self._firstname = options[0]
            self._lastname = options[1]
            #print('Count 2: %s' % (options))
        elif icount==1:
            self._firstname = options[0]
            self._lastname = raw_input('Last Name: ')
            self._suffix = raw_input('Suffix (Jr,Sr,III,..): ')
            #print('Count 1: %s' % (options))
        else:
            self._firstname = raw_input('First Name: ')
            self._lastname = raw_input('Last Name: ')
            self._suffix = raw_input('Suffix (Jr,Sr,III,..): ')
        if nickname:
            if self._nickname == None:
                oname = ''
            else:
                oname = self._nickname    
            nname = raw_input('Nickname: (%s)' % (oname))
            if nname!='':
                self._nickname = nname
                
    def About(self):
        print("""Author         : Harold Clark  email address thetreerat@gmail.com
Class          : person
Inputs         : firstname, lastname, suffix, nickname, DOB, sex, db_handle 
Returns        : Person object
Output         : none
methods        : name(), firstname(), lastname(), dob(), age(), print_person(), set_name(), set_dob()
Purpose        : This class is for greate a person object and the supporting functions 

""")


if __name__ == "__main__":
    P = person()
    P.set_name(nickname=True)
    P.set_DOB()
    print('person %s age is %s' % (P.name(nickname=True), P.age()))
    