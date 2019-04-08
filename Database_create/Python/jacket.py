# Author: Harold Clark
# Copyright Harold Clark 2019
#
import psycopg2
import sys
import os
from database import database

class jacket_history(object):
    def __init__(self, history=None, in_out=None, name=None, update_user=None, eid=None):
        self.history_date = history
        self.in_out = in_out
        self.name = name
        self.update_user = update_user
        self.eid = eid


    def print_history(self):
        """Print history object"""
        print("""    %s  %s %s %s""" % (self.history_date,
                                        self.in_out.ljust(6, chr(32)),
                                        self.name.ljust(63, chr(32)),
                                        self.update_user.ljust(30, chr(32))
                                       )
             )
    
class jacket_histories(object):
    """Class for list of Jacket History"""
    def __init__(self, jid=None):
        self.jid = jid
        self.hlist = []
        self.get_history()
            
    def get_history(self):
        """Load hitrory for jacket from db"""
        self.clear()
        if self.jid!=None:
            ski_db = database()
            ski_db.connect()
            ski_db.cur.callproc('get_jacket_history',[self.jid,])
            result = ski_db.cur.fetchall()
            for r in result:
                h = jacket_history(r[0], r[1], r[2] + ' ' + r[3], r[4], r[5])
                self.hlist.append(h)
            ski_db.close()
                
            
    def print_history(self):
        """Print the jacket history"""
        print("""    Date        Event  Employee Name                                                  Clerk
    ----------- -----  -------------------------------------------------------------- --------------""")
        for h in self.hlist:
            h.print_history()
        print("""    ------------------------------------------------------------------------------------------------""")
    def clear(self):
        """Clear history list"""
        self.hlist = []
            
class jacket(object):
    """Jacket class"""
    def __init__(self, jid=None, jacket_type=None, jacket_size=None, jacket_number=None, eid=None, lid=None, jacket_condition=None):
        """init of a jacket"""
        self.jid = jid
        self.jacket_type = jacket_type
        self.jacket_size = jacket_size
        self.jacket_number = jacket_number
        self.assigned_eid = eid
        self.assigned_name = None
        self.eid_returning = None
        self.lid = lid
        self.location = None
        self.jacket_condition = jacket_condition
        self.cot = None
        if jid!=None:
            self.history = jacket_histories(jid)
        else:
            self.history = None
    
    def check_in_db(self):
        """Call check in database function for a jacket"""
        self.eid_returning = raw_input("""Is %s returning (1 - Yes, 2 - Maybe, 3 - No): """ % (self.assigned_name))
        if self.eid_returning==1:
            self.lid = 5
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('check_in_jacket', [self.jid, self.eid_returning, self.lid,])
        result = ski_db.cur.fetchall()
        ski_db.close()
        self.assigned_eid=42
        self.assigned_name = 'Unassigned Jacket'
        

    def check_out_db(self, eid=None):
        """Update database with new assigned employee"""
        if self.jid==None:
            self.jid = raw_input('Jacket Database ID: ')
        if eid==None:
            eid = raw_input('Employee id: ')
        location_name = 'Locker'
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('check_out_jacket', [eid, self.jid, location_name,])
        result = ski_db.cur.fetchall()
        ski_db.close()
        self.assigned_eid = eid
        self.assigned_name = ''
        
    def get_jackat_db(self):
        """Get jacket data from database"""
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('get_jacket', [self.jid,])
        result = ski_db.cur.fetchall()
        result = result[0]
        self.jacket_type = result[1]
        self.jacket_size = result[3]
        self.jacket_number = result[2]
        self.assigned_eid = result[4]
        self.assigned_name = result[5] + " " + result[6]
        self.cot = result[7]
        self.jacket_condition = result[8]
        self.lid = result[9]
        self.location = result[10]
        ski_db.close()
        
    def get_jacket_history_db(self):
        """get jacket history from database"""
        if self.history==None:
            self.history = jacket_histories(self.jid)
        else:
            self.history.clear()
            self.history.jid = self.jid
            self.history.get_histroy()
        
        
        
    def pad(self,item, length):
        if item==None:
            item = ''
            for l in range(length):
                item = item + chr(32)
        else:
            length = length - len(item)
            for l in range(length):
                item = item + chr(32)
        return item
        
        
    def print_jacket(self, return_type='Long'):
        if return_type=='Long':
            print("""Jacket ID:     %s
Jacket Type:   %s
Jacket Size:   %s
Jacket Number: %s
Assigned EID:  %s
Assigned Name: %s
Location ID:   %s
Condition:     %s""" % (self.jid,
                        self.jacket_type,
                        self.jacket_size,
                        self.jacket_number,
                        self.assigned_eid,
                        self.assigned_name,
                        self.lid,
                        self.jacket_condition))
            if self.history!=None:
                self.history.print_history()
        elif return_type=='Short':
            print("""    %s %s %s %s %s %s""" % (self.pad(str(self.jid),9),
                                          self.pad(self.jacket_type,33),
                                          self.pad(self.jacket_size, 11),
                                          self.pad(self.jacket_number,13),
                                          self.pad(self.location,13),
                                          self.pad(self.jacket_condition, 15)))
                                          
        
    def print_menu(self):
        os.system('clear')
        self.print_jacket()
        self.history.print_history()
        if self.assigned_eid in [42,45]:
            in_out = '    CHECKOUT  - Check Out Jacket'
        else:
            in_out = '    CHECKIN   - Check in Jacket'
        print("""
    ---------   --------------------------------------
    LOCATION  - Change Location of Jacket
%s
    CONDITION - Change Jacket Condition
    DAMAGED   - Mark Jacket as Damaged, Out of Service
    REPAIR    - Mark Jacket Out For Repair
    FIXED     - Mark Jacket Repaired
    RETURN    - Return to prevouse menu
    EXIT      - Exit to the system Prompt 
    ---------   --------------------------------------""" % (in_out))
        
    def jacket_menu(self):
        """Run jacket Menu till user is done"""
        run = True
        if self.jid!=None:
            self.get_jackat_db()
            self.get_jacket_history_db()
        while run:
            self.print_menu()
            answer = raw_input('Please enter Selection: ').upper()
            answer = list(answer.split())
            while answer:
                if answer[0] in ['RETURN','RETUR','RETU','RET','RE' ]:
                    run = False
                    break
                elif answer[0] in ['LOCATION','LOCATIO','LOCATI','LOCAT','LOCA','LOC','LO','L']:
                    print('LOCATION')
                    dump = raw_input('ready?')
                    break
                elif answer[0] in ['CONDITION','CONDITIO','CONDITI','CONDIT','CONDI','COND','CON','CO' ]:
                    print('Condition')
                    dump = raw_input('ready?')
                    break
                elif answer[0] in ['DAMAGED','DAMAGE','DAMAG','DAMA','DAM','DA','D']:
                    print('DAMAGED')
                    dump = raw_input('ready?')
                    break
                elif answer[0] in ['REPAIR','REPAI','REPA','REP','RE']:
                    print('REPAIR')
                    dump = raw_input('ready?')
                    break
                elif answer[0] in ['FIXED','FIXE','FIX','FI','F']:
                    print('FIXED')
                    dump = raw_input('ready?')
                    break
                elif answer[0] in ['CHECKOUT','CHECKOU','CHECKO', 'OUT']:
                    self.check_out_db()
                    self.get_jacket_history_db()
                    break
                elif answer[0] in ['CHECKIN','CHECKI','IN']:
                    self.check_in_db()
                    self.get_jacket_history_db()
                    
                    break
                elif answer[0] in ['EXIT', 'EXI','EX','E']:
                    sys.exit(1)
                else:
                    print("""Lost in space!!!""")
                    print(answer)
                    dump = raw_input('ready?')
                    break

class NewJacket(object):
    "jacket class for loading new groups of jackets"
    def __init__(self):
        self.jid = None
        self.jacket_type = None
        self.jacket_size = None
        self.jacket_start_number = None
        self.jacket_end_number = None
    
    def print_pad(self, item, length):
        length = length - len(item)
        pad = ''
        for l in range(length):
            pad = pad + chr(32)
        return pad
    
    
    def print_jacket(self, list_for='New'):
    
        print("""%s%s %s%s  %s%s %s%s %s """ % (self.jid, self.print_pad(str(self.jid), 7),
                                            self.jacket_type, self.print_pad(self.jacket_type,29),
                                            self.jacket_size, self.print_pad(self.jacket_size, 11),
                                            self.jacket_start_number, self.print_pad(self.jacket_start_number, 19),
                                            self.jacket_end_number))

class jackets(object):
    """Class for a list of jackets"""
    def __init__(self):
        """init of list of jackets"""
        self.jlist = []
        self.count = 0

    def add_jackets_db(self):
        ski_db = database()
        ski_db.connect()
        for line in self.jlist:
            for jacket_number in range(int(line.jacket_start_number), int(line.jacket_end_number) + 1):
                ski_db.cur.callproc('add_jacket', [line.jacket_type, str(jacket_number), line.jacket_size, ])
                result = ski_db.cur.fetchall()
        ski_db.close()
        return True
        
    def add_jacket_group(self):
        """collect info for a jacket group"""
        self.count += 1
        #j = jacket()
        j = NewJacket()
        j.jid = self.count
        j.jacket_type = raw_input('Jacket Type: ')
        j.jacket_size = raw_input('Jacket Size: ')
        j.jacket_start_number = raw_input('Jacket Start Number: ')
        j.jacket_end_number = raw_input('Jacket End Number: ')
        self.jlist.append(j)

    def checkID(self, jid):
        try:
            jid = int(jid)
            for i in self.jlist:
                if i.jid==jid:
                    return i
            return None
        except:
            return None
        
     
    def clear(self):
        self.jlist = []
    
    def get_employee_jackets_db(self, eid):
        """ """
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('get_employee_jackets', [eid,])
        result = ski_db.cur.fetchall()
        for r in result:
            j = jacket()
            j.jid = r[0]
            j.jacket_type = r[1]
            j.jacket_number = r[2]
            j.jacket_size = r[3]
            j.assigned_eid = r[4]
            j.lid = r[5]
            j.location = r[6]
            j.cot = r[7]
            j.jacket_condition = r[8]
            self.jlist.append(j)
        ski_db.close()

    def get_jacket(self, jacket_size, jacket_type, jacket_number):
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('', [])
        result = ski_db.cur.fetchall()
        for r in result:
            j = jacket(jid=r[0],
                       jacket_type=r[1],
                       jacket_size=r[2],
                       jacket_number=r[3],
                       eid=r[4],
                       lid=r[5],
                       jacket_condition=r[6])
    
    def get_jackets_for_size(self, size):
        """get jackets for a size"""
        ski_db = database()
        ski_db.connect()
        ski_db.cur.callproc('list_available_jacket', [size,])
        result = ski_db.cur.fetchall()
        for r in result:
            j = jacket(jid=r[0])
            j.jacket_type = r[1]
            j.jacket_number = r[2]
            j.jacket_size = r[3]
            j.jacket_condition = r[4]
            j.lid = r[5]
            j.location = r[6]
            self.jlist.append(j)
            
        ski_db.close()
        
    def new_jackets_menu(self):
        """Run menu to add New jackets"""
        while True:
            self.print_menu()
            answer = raw_input('Please enter a selection: ').upper()
            answer = list(answer.split())
            while answer:
                if answer[0] in ['EXIT', 'EXI', 'EX', 'E', 'QUIT', 'QUI', 'QU', 'Q']:
                    sys.exit(1)
                elif answer[0] in ['ADD', 'AD', 'A']:
                    J.add_jacket_group()
                    break
                elif answer[0] in ['EDIT', 'EDI','ED','E']:
                    if len(answer)==1:
                        answer.append(raw_input("""Enter item number: """))
                    print("""Edit jacket group: %s""" % (answer[1]))
                    dump = raw_input('ready?')
                    break
                elif answer[0] in ['LOAD', 'LOA', 'LO', 'L']:
                    J.add_jackets_db()
                    break
                else:
                    print("""Lost in space!!!""")
                    dump = raw_input('ready?')
                    break
            
        
    def print_list(self, list_for='New'):
        if list_for=='New':
            print("""Line ID Jacket Type                    Jacket Size Jacket Start Number Jacket End Number """)
            print("""------- ------------------------------ ----------- ------------------- ----------------- """)
        else:
            print("""
    Jacket ID Jacket Type                       Jacket Size Jacket Number Location     Condition
    --------- --------------------------------- ----------- ------------- ------------ -----------""")

        if len(self.jlist)>0: 
            for j in self.jlist:
                j.print_jacket(list_for)
        
        else:
            print(len(self.jlist))

        
        print("""    ----------------------------------------------------------------------------------------------
              """)

                
    def print_menu(self, call_from='New'):
        os.system('clear')
        self.print_list(call_from)
        print("""    ----------------------------------------------------
     ADD       - Add New Group
     EDIT #    - Edit a Group
     LOAD      - Load Entered Data into Table
     EXIT      - Quit or Exit program""")
            
            
if __name__ == '__main__':
    J = jackets()
    #J.new_jackets_menu()
    size = raw_input('enter size (XXS,XS,S,M,L,XL,XXL): ').upper()
    J.get_jackets_for_size(size)
    print(len(J.jlist))
    #J.print_list('Size')
    J.print_menu('Short')
    #J.get_employee_jackets_db(15)
    #for j in J.jlist:
    #    j.print_jacket(return_type='Short')
    #os.system('clear')
    #J.print_list('Short')
    #jid = raw_input('Select Jacket ID to Checkout: ')
    #jacket = J.checkID(jid)
    
    #jacket.print_jacket('Long')
    #jacket.check_out_db(eid=15)