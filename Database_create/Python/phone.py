# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database

class phone(object):
    def __init__(self, number=None, display='Cell', publish=True, db_handle=None):
        self._number = None
        self.db_handle = None
        self._publish = None
        self.display = display
        self.set_phone(number)
        self.set_publish(publish)
        self.set_db_handle(db_handle)
            
    def number(self, number_only=True):
        """convert phone number to display value and return"""
        
        l = len(self._number)
        if l==7:
            phone = """%s-%s""" % (self._number[0:3], self._number[3:7])
        elif l==10:
            phone = """%s-%s-%s""" % (self._number[0:3], self._number[3:6], self._number[-4:])
        else:
            phone = self._number
            
        return phone

    def publish(self):
        if self._publish==1:
            return 'True'
        else:
            return 'False'
              
    def set_phone(self, options=None):
        if type(options) is list:
            try:
                db_handle = options[3]
                if options[1]:
                    phone = options[1]
                elif options[2][0]:
                    phone = options[2][0]
            except:
                if len(options)>0:
                    phone = options[0]
                else:
                    phone = raw_input('Enter Phone number: ')
        elif type(options) is int:
            self._number = options
            return
        else:
            phone= options
        I = ['-', '(', ')', ' ']
        number = phone
        for i in I:
            phone = number
            number = ''
            start=0
            current=start
            p=start
            while True:
                current = phone.find(i, start)
                if current == -1:
                    number = number + phone[start:]
                    break
                else:
                    number = number + phone[start:current]
                    start= current +1
                            
        self._number = number
    
    def set_publish(self, data):
        try:
            data.upper()
        except:
            pass
        
        if data in [0, 'FALSE', False, None]:
            self._publish = 0
        elif data in [1,'TRUE',True]:
            self._publish = 1
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='phone.py - phone')
            
      
class phones(object):
    def __int__(self, db_handle=None):
        self.plist = []
        self.set_db_handle(db_handle)
        self.db_handle = None
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            s
if __name__ == '__main__':
    P = phone(number='(585) 512-4786', publish=True)
    print('raw number: %s' % (P._number))
    print('display: %s' % (P.number()))
    print('Publish: %s' % (P.publish()))

    
