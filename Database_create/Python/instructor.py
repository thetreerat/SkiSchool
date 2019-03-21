# Author: Harold Clark
# Copyright Harold Clark 2019
#
class person(object):
    def __init__(self):
        self.firstname = None
        self.lastname = None
        self.DOB = None
        self._Age = None
        
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
            if i.instructor_name()==Name:
                return i
        return None
    
    def list_instructors(self):
        """Print list of instructors"""
        if len(self.ilist)>0:
            for i in self.ilist:
                i.print_instructor()
        else:
            print("""No instructors in list!!""")
    
    def get_name(self, eid, return_type='INDEX'):
        """return index or name from eid"""
        index = 0
        for i in self.ilist:
            #print("""%s - %s""" % (index, i.eid))
            if int(i.eid)==int(eid):
                break
            index+=1
        rt=return_type.upper()
        if rt=='INDEX':
            return index
        elif rt=='NAME':
            return self.ilist[index].instructor_name()
        
