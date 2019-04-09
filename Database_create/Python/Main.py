# Author: Harold Clark
# Copyright Harold Clark 2019
#
from menu import Menu
#from instructor import intructor
#from instructor import instructors
from jacket import jacket
from jacket import jackets
#from jacket import jacket_histories
#from jacket import jacket_history


def load_menus(Main, Jackets):
   
    Main.add_item('Instructors', 'Manage instructors', print_this)
    Main.add_item('Jackets', 'Manage jackets', jackets_menu)
    Main.add_item('Lockers', 'Manage lockers and offices', print_this)
    Main.add_item('Certs', 'Manage Certifications', print_this)

    Jackets.add_item('New', 'Add new jacket series', new_jackets)
    Jackets.add_item('List', 'List available jackets', print_this)
    Jackets.add_item('CheckIn', 'Check In a jacket', print_this)

def print_this():
    raw_input('This is a test! ')
    
def new_jackets():
    new_jackets = jackets()
    new_jackets.new_jackets_menu()
        
def main_menu():
    Main.Menu()

def jackets_menu():
    
    Jackets.Menu()
   
if __name__ == "__main__":
    print('Start')
    Main = Menu()
    Main.menu_display = Main.print_help
    New_Jackets = Menu()
    
    Jackets = Menu()
    Jackets.menu_display = Jackets.print_help
    load_menus(Main, Jackets)
    main_menu()
    print('Here')
