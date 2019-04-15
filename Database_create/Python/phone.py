# Author: Harold Clark
# Copyright Harold Clark 2019
#
class phone(object):
    def __init__(self, number=None, display='Cell', publish=True):
        self._number = number
        self.display = display
        self.publish = publish
        print(self._number)
    
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
    
    def set_phone(self, options=[]):
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
        try:
            test = int(phone)
        except:
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
                        
                    start = current +1    
        self._number = number
            
if __name__ == '__main__':
    P = phone()
    P.set_phone()
    print(P)
    print(P._number)
    print(P.number())

    
