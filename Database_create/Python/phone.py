# Author: Harold Clark
# Copyright Harold Clark 2019
#
from database import database

class phone(object):
    LONG = 1
    SHORT = 2
    def __init__(self, number=None, display='Cell', publish=True, db_handle=None):
        self.db_handle = None
        self._display = display
        self.display_pad = 10
        if number=='' or number==None:
            self._number = None
        else:
			self._number = number
        self.number_pad = 20
        self._publish = None
        self.set_phone(number)
        self.set_publish(publish)
        self.set_db_handle(db_handle)
    
    def display(self, pad=10, divider=':'):
        if self._display==None:
            return ('Phone' + divider).ljust(pad)
        else:
            return (self._display + divider).ljust(pad)
        
    def number(self, number_only=True, pad=15):
        """convert phone number to display value and return"""
        if number_only:
            return self._number
        try: 
            l = len(self._number)
        except:
            return ''
        if l==7:
            phone = """%s-%s""" % (self._number[0:3], self._number[3:7])
        elif l==10:
            phone = """%s-%s-%s""" % (self._number[0:3], self._number[3:6], self._number[-4:])
        else:
            phone = self._number
            
        return phone.ljust(pad)

    def publish(self):
        if self._publish==1:
            return 'True'
        else:
            return 'False'

    def set_db_handle(self, db_handle):
        if db_handle==None:
            db_handle = database(owner='phone.py - phone')
                          
    def set_phone(self, options=None):
        
        if type(options) is list:
            try:
                if options[1]:
                    phone = str(options[1])
                    if len(options[2]) > 0:
                        D = ''
                        for d in options[2]:
                            if D=='':
                                D = d
                            else:
                                D = D + chr(34) + d
                        self._display = D
                elif options[2][0]:
                    phone = options[2][0]
            except:
                phone = raw_input('Enter Phone number: ')
                #self.convert_number_string(phone)
        elif type(options) is int:
            self._number = str(options)
            return
        else:
            phone= options
        self.convert_number_string(phone)
        
        
    def convert_number_string(self, phone):
        if phone==None:
            self._number = phone
        else:
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
    
    def print_self(self, return_type=LONG, pad=10):
        if return_type==LONG:
            print('    %s%s%s' % (self.display.ljust(self.display_pad), self.number().ljust(self.number_pad), self.publish()))
            
class phones(object):
    def __int__(self, db_handle=None):
        self.plist = []
        self.set_db_handle(db_handle)
        self.db_handle = None
    
    def set_db_handle(self, db_handle):
        if db_handle==None:
            self.db_handle = database(onwer='phone.py - phone')
        
if __name__ == '__main__':
    P = phone(number='(585) 512-4786', publish=True)
    print('raw number: %s' % (P._number))
    print('display: %s' % (P.number()))
    print('Publish: %s' % (P.publish()))

    
