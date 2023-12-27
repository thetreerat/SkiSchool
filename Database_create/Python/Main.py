#!/usr/bin/env python
# Author: Harold Clark
# Copyright Harold Clark 2019

#from instructor import intructor
from database import database
from instructor import instructors
from location import Location
from locations import Locations
from jacket import jacket
from jacket import jackets
from menu import Menu
from private import private
from private import privates
from shift import shifts
from shifttemplates import ShiftTemplates
from availability import availablities
from extradays import ExtraDays
from extradaystemplate import ExtraDaysTemplate
from season import Season
from login import Login
from trainings import Trainings
from cert import certs
from candidates import Candidates
from certtemplates import CertTemplates

#from jacket import jacket_histories
#from jacket import jacket_history
        
    
def print_this(dump=None):
    raw_input('This is a test! ')

def admin_menu(options=None):
    db_handle = options[3]
    T = ExtraDays(db_handle=db_handle)
    S = Season(db_handle=db_handle)
    C = CertTemplates(db_handle=db_handle)
    Admin = Menu('Admin Main Menu', db_handle=db_handle)
    Admin.menu_display = Admin.print_help
    Admin.add_item('Season', 'Add new season', S.menu)
    Admin.add_item('Extra', 'EXTRA - Manage current Season extra Days', T.menu)
    Admin.add_item('Certification', 'CERTIFICATION - Manage Certifcation templates', C.menu)
    
    
    Admin.Menu()

def candidate_menu(options=None):
    C = Candidates(db_handle=options[3])
    C.menu()

def certifcation_menu(options=None):
    C = certs(db_handle=options[3], list_type='Cert')
    C.menu()    
    
def jackets_menu(options=None):    
    db_handle = options[3]
    Jackets = Menu('Jacket Main Menu', db_handle=db_handle)
    Jackets.menu_display = Jackets.print_help
    Jackets.add_item('New', 'Add new jacket series', jackets_new_menu)
    Jackets.add_item('Find', 'FIND - advance find menu', print_this)
    Jackets.add_item('CheckIn', 'Check In a jacket', print_this)
    Jackets.Menu()
        
def jackets_new_menu(dump=None):
    new_jackets = jackets()
    new_jackets.new_jackets_menu()    

def location_menu(options=None):
    L = Locations(db_handle=options[3])
    L.get_locaitons_available_db()
    L.menu()
        
def instructor_menu(answer=None):
    try:       
        db_handle=answer[3]
    except:
        db_handle = database('main.py - instructor_menu')
    I = instructors(db_handle=db_handle)    
    I.menu()
       
def private_menu(options=None):
    #print(options[3])
    try:
        db_handle = options[3]
    except:
        db_handle = database(owner='main.py Private_menu')
    P = privates(db_handle=db_handle)
    find_help = """FIND DATE <DATE> - Find private lessons on date.
                    - FIND CUSTOMER <Firstname> <LastName> - Find private lessons for customer Name
                    - FIND INSTRUCTOR <Firstname> <Lastname> - find private lessons assigned to instructor
                    - FIND - advanced find options menu"""
    private = Menu('Private Lesson Main Menu', db_handle=db_handle)
    private.menu_display = private.print_help
    private.add_item('New', 'NEW - Create a new private lesson', private_new_menu)
    private.add_item('Cancel', 'CANCEL # - Cancel private lesson at line #', print_this)
    private.add_item('Find', find_help, P.find_privates)
    private.add_item('Publish', 'PUBLISH <DATE> - Create HTML Page for Date, and post on website', print_this)
    private.add_item('Edit', 'EDIT # - Edit a private lesson', print_this)
    private.Menu()

def private_new_menu(options=None):
    print(options[3])
    P = private(db_handle=options[3])
    private_new = Menu('Add New Private Menu', db_handle=options[3])
    private_new.menu_display = P.PrivateMenu
    private_new.add_item('Contact', 'CONTACT <firstname> <lastname> <relationship> - Enter contact person information for private lesson', P.set_contact)
    private_new.add_item('Student', 'STUDENT <Firstname> <Lastname> - Name of person taking the lesson', P.set_student)
    private_new.add_item('Phone', 'PHONE <#> - Set contact phone number', P.set_phone)
    private_new.add_item('Type', 'TYPE <A/D> - set lesson type as assigned or Demand', P.set_type)
    private_new.add_item('Age', 'AGE <#> - Enter the students age', P.set_age)
    private_new.add_item('Time', 'TIME <starttime> <endtime> - Enter start and stop times', P.set_time)
    private_new.add_item('Start', 'START <DATE> - Enter start time', P.start_time.set_time)
    private_new.add_item('End', 'END <DATE> - Enter end time', P.end_time.set_time)
    private_new.add_item('Discipline', 'DISCIPLINE <SKI/SB/TELE>- Set the disapline', P.set_discipline)
    private_new.add_item('Date', 'DATE <MM/DD/YYYY> - set date of the lesson', P.shift_date.get_date)
    private_new.add_item('Load', 'LOAD - Save private to database', P.load_private)
    private_new.add_item('List', 'LIST - List instructors', P.set_instructor)
    private_new.add_item('Find', 'FIND <firstname> <lastname> - find instrutors by name', P.find_instructor)
    private_new.add_item('Skill', 'SKILL <1-9> or SKILL <Yellow,Yellow+,green,blue> - Skill level of the student', P.set_skill)
    private_new.Menu()
      
def schedule_menu(options=None):
    S = shifts(db_handle=options[3])
    T = ShiftTemplates(db_handle=options[3])
    A = availablities(db_handle=options[3])
    
    
    schedule = Menu('Schedule Menu')
    schedule.menu_display = schedule.print_help
    schedule.add_item('Templates', 'View/mange Templates for a day', T.menu)
    schedule.add_item('Day', 'View all shfits for a date', S.menu_date)
    schedule.add_item('Off', 'View Doys off requests', print_this)
    schedule.add_item('Privates', 'view privates for the Week', print_this)
    schedule.add_item('availability', 'list availability for a day of the week', A.menu_dow)
    schedule.Menu()

def training_menu(options=None):
    T = Trainings(db_handle=options[3])
    T.menu()
    
if __name__ == "__main__":
    L = Login(login='halc')
    L.Login()
    #ski_db = database(owner='main.py - __main__')
    
    Main = Menu('Main Menu', db_handle=L.db_handle)
    Main.menu_display = Main.print_help    
    Main.add_item('Instructors', 'Manage instructors', instructor_menu)
    Main.add_item('Jackets', 'Manage jackets', jackets_menu)
    Main.add_item('Lockers', 'Manage lockers and offices', location_menu)
    Main.add_item('Certs', 'Manage Certifications', certifcation_menu)
    Main.add_item('Schedule', 'Manage Schedules', schedule_menu)
    Main.add_item('Private', 'Manage Private Schedule', private_menu)
    Main.add_item('Setup', 'Setup functions', admin_menu)
    Main.add_item('Training', 'Manage Training Logs', training_menu)
    Main.add_item('Candidates', 'Manage Candidates', candidate_menu)
    Main.Menu()
