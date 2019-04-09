# Author: Harold Clark
# Copyright Harold Clark 2019
#
import os
import sys

class  Menu(object):
    """New Class"""
    def __init__(self):
        """Create New Instanace of New Class"""
        self.menu_items = []
        self.next_ID = 0
        self.command_display = 1
        self.menu_display = None
        self.menu_run = True
        self.used_items = []
        self.add_item('Exit', 'Exit to system prompt.', self.exit_now())
        self.add_item('Return', 'Return to previous menu.', self.return_now())
        self.add_item('Help', 'Help Menu', self.help())

    def add_item(self, display_text, help_text=None, menu_command=None):
        i = menu_item(iID=self.NewID(),
                      display_text=display_text,
                      help_text=help_text,
                      menu_command=menu_command)
        i.make_item_match()
        
        self.menu_items.append(i)
        
    def exit_now(self):
        sys.exit(1)
        
    def return_now(self):
        self.menu_run = False
    

            
    

    def item_count(self):
        return len(self.menu_items)
 
    def help(self):
        self.print_help()
        raw_input('Ready? ')
        
        
    def Menu(self):
        run = True
        while self.menu_run:
            os.system('clear')
            self.menu_display()
            self.print_command_list()
            action, item_index, options  = self.split_command(raw_input('Enter Command: '))
            while action:
                if action in ['HELP', '?', 'MAN']:
                    self.help()
                    break
                else:
                    not_hit = True
                    for i in self.menu_items:
                        if action==i.display_text.upper():
                            i.menu_command()
                            not_hit = False
                            break
                    if not_hit:
                        raw_input('%s is invalid. ready?' % (action))
                        break
                    break
                    
    def NewID(self):
        """Get ID and increase count"""
        ID = self.next_ID
        self.next_ID += 1
        return ID
    
    def print_items(self):
        """ """
        print("    Menu Items list ....")
        for i in self.menu_items:
            i.print_self()
        print('    Totol Count: %s' % (self.item_count()))
    
    def print_command_list(self):
        """print list of commands"""
        if self.command_display==1:
            commands = '    '
            comma = ''
            for c in self.menu_items:
                commands = """%s%s%s""" % (commands, comma, c.display_text)
                comma = ', '
            print("""%s""" % (commands))
            
    def print_help(self):
        os.system('clear')
        print('      Menu help ...')
        print('    --------------------------------------------------------------------------------------')
        for i in self.menu_items:
            i.print_help()
        print('    --------------------------------------------------------------------------------------')
        
    def split_command(self, command):
        item_index = False
        options = []
        action = None
        command = list(command.split())
        if len(command)>0:
            action = command.pop(0).upper()
            while len(command)>0:
                c = commnad.pop(0)
                try:
                    item_index = self.int(c)
                except:
                    options.append(c)
        return (action, item_index, options)
        
    def About(self):
        print("""Author         : Harold Clark  email address harold.clark@openscg.com
Class          : New Class
Inputs         : None
Returns        : None
Output         : None
Purpose        : This Class is a temlplete file

""")



class menu_item(object):
    """Menu item class object"""
    def __init__(self, iID=None, display_text=None, help_text='', menu_command=None):
        self.iID = iID
        self.display_text = display_text
        self.help_text = help_text
        self.menu_command = menu_command
        self.item_match = []
    
    def make_item_match_list(self):
        new_i = self.display_text.upper()
        self.item_match = [new_i]
        count = len(new_i)
        while count>1:
            new_i = new_i[:-1]
            self.item_match.append(new_i)
            count -= 1
            
    def print_self(self):
        print("""    ID: %s Item Display: %s""" % (self.iID, self.display_text))
    
    def print_help(self):
        print("""    %s - %s """ % (self.display_text.upper().ljust(15), self.help_text.ljust(60)))
 

    
if __name__ == "__main__":
    M = Menu()
    M.add_item('Add', 'Add <NAME> <ORG> as a new Cert to database')
    M.add_item('Edit', 'Edit <#> Cert and commit to database')
    M.print_items()
    M.Menu()
    test()
    