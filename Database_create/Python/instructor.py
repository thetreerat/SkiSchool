# Author: Harold Clark
# Copyright Harold Clark 2019
#
class instructor(object):
    def __init__(self):
        """Init a instructor object"""
        self.firstname = None
        self.lastname = None
        self.eid = None
    
    def print_instructor(self):
        """Print instructor object"""
        print """%s - %s %s""" % (self.eid, self.firstname, self.lastname)
        
    def instructor_name(self):
        """return instructor name first name<sp> last name as string"""
        return """%s %s""" % (self.firstname, self.lastname)
    
    
class instructors(object):
    def __init__(self):
        """init a set of instructors"""
        self.ilist = []
    
    def add_instructor(self, i):
        """Add instructor to instructors list """
        if self.checkName(i.instructor_name)==None:
            self.ilist.append(i)
        
    def checkID(self, eid):
        for i in self.ilist:
            if i.eid==eid:
                return i
        return None
    
    def checkName(self, Name):
        for i in self.ilist:
            if i.instructor_name(self)==Name:
                return i
        return None
    
    def list_instructors(self):
        """Print list of instructors"""
        for i in self.ilist:
            i.print_instructor()

