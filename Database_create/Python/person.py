# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database
from datetime import datetime
from date import date
from date import DOB

class  person(object):
    """person object"""
    def __init__(self,
                 firstname=None,
                 lastname=None,
                 suffix=None,
                 nickname=None,
                 dob=None,
                 sex=None,
                 db_handle=None):
        """Create New Instanace of person"""
        self.set_db_handle(db_handle)
        self._firstname = firstname
        self._lastname = lastname
        self._suffix = suffix
        self._nickname = nickname
        self.DOB = DOB(DOB=dob, db_handle=self.db_handle)
        self.sex = sex
       
    def __str__(self):
        return "PERSON - Name: %s, DOB: %s, db: %s" % (self.name(True), self._DOB.date(), self.db_handle.owner)

    def age(self, adult=False):
        return self.DOB.age(adult)
    
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
                
    def print_self(self, count=None):
        if count==None:
            count = '    '
        else:
            count = '    %s ' % count
        if self._suffix:
            line = """%s%s %s %s""" % (count, self._firstname, self._lastname, self._suffix)
        else:
            line = """%s%s %s""" % (count, self._firstname, self._lastname)
        print(line)
        
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='person.py - person object')
        self.db_handle = db_handle
            
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
    P = person(firstname='Harold', lastname='Clark', DOB='12/25/1969')
    print(P)    