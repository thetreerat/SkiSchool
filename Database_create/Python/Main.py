# Author: Harold Clark
# Copyright Harold Clark 2019
#
from menu import Menu
#from instructor import intructor
from instructor import instructors
from jacket import jacket
from jacket import jackets
#from jacket import jacket_histories
#from jacket import jacket_history


def load_menus(Main):
    Main.add_item('Instructors', 'Manage instructors', instructor_menu)
    Main.add_item('Jackets', 'Manage jackets', jackets_menu)
    Main.add_item('Lockers', 'Manage lockers and offices', print_this)
    Main.add_item('Certs', 'Manage Certifications', print_this)
    Main.add_item('Schedule', 'Manage Schedules', schedule_menu)
    Main.add_item('Private', 'Manage Private Schedule', private_menu)


    
    
    
def print_this():
    raw_input('This is a test! ')
    
def jackets_menu():    
    
    Jackets = Menu('Jacket Main Menu')
    Jackets.menu_display = Jackets.print_help
    Jackets.add_item('New', 'Add new jacket series', new_jackets)
    Jackets.add_item('List', 'List available jackets', print_this)
    Jackets.add_item('CheckIn', 'Check In a jacket', print_this)

    Jackets.Menu()

def instructor_menu():
    I = instructors()
    instructor = Menu('Instructor Menu')
    instructor.menu_display = I.print_menu
    instructor.add_item('Add', 'ADD <Firstname> <Lastname> <Suffix> - add a new instructor', I.add_instructor)
    instructor.add_item('Find', 'FIND <Fisrtname> <Lastname> - find matching instructor(s) and display list of them', I.find_name)
    instructor.add_item('Edit', 'Edit # - Open instructor # for editing or veiwing. must be selected from a found list of instructors', I.edit)
    instructor.add_item('Clear', 'Clear - clears the list of found instructors')
    instructor.Menu()
    
def main_menu():
    Main.Menu()

def new_jackets():
    
    new_jackets = jackets()
    new_jackets.new_jackets_menu()
    
def private_menu():
    raw_input('private menu under construction')
   
def schedule_menu():
    schedule = Menu('Schedule Menu')
    schedule.menu_display = schedule.print_help
    schedule.add_item('View', 'Veiw templates for a day', print_this)
    schedule.add_item('Day', 'View shfit for a date', print_this)
    schedule.add_item('Off', 'View Doys off requests', print_this)
    schedule.add_item('Private', 'view privates for the Week', print_this)
    schedule.add_item('availability', 'total availability for a day of the week', print_this)
    schedule.Menu()
   
if __name__ == "__main__":
    
    Main = Menu('Main Menu')
    Main.menu_display = Main.print_help    
    load_menus(Main)
    
    Main.Menu()
