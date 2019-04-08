# Author: Harold Clark
# Copyright Harold Clark 2019
#
class  Menu(object):
    """New Class"""
    def __init__(self):
        """Create New Instanace of New Class"""
        self.menu_items = []
        self.next_ID = 0

    def add_item(self, display_text):
        i = menu_item(iID=self.NewID(), display_text=display_text)
        self.menu_items.append(i)
    
    def NewID(self):
        """Get ID and increase count"""
        ID = self.next_ID
        self.next_ID += 1
        return ID
    
    def item_count(self):
        return len(self.menu_items)
    
    def print_items(self):
        """ """
        print("    Menu Items list ....")
        for i in self.menu_items:
            i.print_self()
        print('    Totol Count: %s' % (self.item_count()))
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
    def __init__(self, iID=None, display_text=None, help_text=''):
        self.iID = iID
        self.display_text = display_text
        self.help_text = help_text
    
    def print_self(self):
        print("""    ID: %s Item Display: %s""" % (self.iID, self.display_text))
    
if __name__ == "__main__":
    M = Menu()
    M.add_item('Add')
    M.add_item('Edit')
    M.print_items()