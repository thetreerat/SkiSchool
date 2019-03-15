# Author: Harold Clark
# Copyright Harold Clark 2019
#
from datetime import datetime
#from datetime import strptime
#from datetime import strttime
class html(object):
    def __init__(self, css=None):
        """init a html page object"""
        self.body = None
        self.page = ''
        self.css = None
        self.setcss(css)
        self.head = None
        self.createHead()
        self.hour = 0
        self.count = 0
        self.filename = None
        self.path = None
        self._date = None
        self.PageTitle = None

    def setcss(self,filename):
        """set css file name"""
        if filename==None:
            self.css = "skischool.css"
        else:
            self.css = filename
        
    def createHead(self):
        """Create a header for html page"""
        self.head = """  <head>
     <link rel="stylesheet" type="text/css" href="%s">
  </head>
""" % (self.css)

    def wrapAsHtml(self):
        """wrap page with <html> tags """
        self.page = """<html>
%s
%s
</html>""" % (self.head, self.body)
     
    def setbody(self, body):
        self.body = """  <body>
%s
  </body>""" % (body)

    def setdate(self, date):
        self._date = datetime.strptime(date, "%m/%d/%y")
    
    def date(self):
        return self._date
    
    def dateDOW(self):
        return self._date.strftime("%A")
    
    def dateHeaderString(self):
        return self._date.strftime("%m/%d/%y")
        
    def datestring(self):
        return self._date.strftime("%y%m%d")
        
    
    def wraptable(self, table):
        finishedTable = """    <table>
%s
    </table>""" % (table)
        return finishedTable
    
    def wraprow(self, cells):
        """Wrap row in <TR> tags"""
        row = """      <tr>
%s
      </tr>""" % (cells)
        return row

    def wrapcell(self, cell, cellclass=None, span=1):
        """wrap cell with <td> tags """
        
        if span!=1:
            tdspan = """ colspan=%s""" % (span)
        else:
            tdspan = ""
        #print("""%s - %s""" % (span, tdspan))
        if cellclass==None:
            cellclass=""
        else:
            cellclass=""" class='%s' """ % (cellclass)
        c = """          <td%s%s>%s</td>""" % (cellclass, tdspan, cell)
        return c
    
    def write_html(self):
        """open filename, write page contents to file"""
        filename = self.path + self.filename
        f = open(filename, "w")
        f.write(self.page)
        f.close()

    def hourcount(self, addcount):
        while addcount > 0:
            self.count+=1
            if (self.count + 1)%4==0:
                self.hour+=1
            addcount-=1
            
        
    def employee_table_row(self,e, cells=30, hour=7):
        """create row for employee shift"""
        self.count = 0
        self.hour = hour
        cshift = e.shifts.pop(0)
        span=1
        cellclass=None
        while self.count < cells:
            self.hourcount(1)
            #print("""%s - %s""" % (cshift.start_time.hour, self.hour))
            if self.count==1:
                row = self.wrapcell(e.firstname())
            elif self.count==2:
                row = """%s
%s""" % (row, self.wrapcell(e.lastname()))
            else:
                #print("""%s - %s""" % (self.hour,self.count))
                if int(cshift.start_time.hour)==self.hour:
                    #cshift.print_shift()
                    cell = cshift.shift_name
                    span = cshift.shift_length_segments()
                    self.hourcount(span-1)
                    if cshift.shift_name[0:7]=='Private':
                        cellclass = 'Private'
                    else:
                        cellclass = cshift.html_class
                    if len(e.shifts)!=0:
                        cshift = e.shifts.pop(0)
                else:
                    span=1
                    cellclass = None
                    cell = ''
                row = """%s
%s""" % (row, self.wrapcell(cell, cellclass, span))
             
        row = self.wraprow(row)
        return row
    
    def shift_table_header(self):
        """create table header row"""        
        cells = 30
        count = 0
        hour = 8
        ampm = 'am'
        while count < cells:
            count+=1
            if count==1:
                row = self.wrapcell('First Name', 'Name')
            elif count==2:
                row = """%s
%s""" % (row, self.wrapcell('Last Name', 'Name'))
            elif count in (3,7,11,15,19,23,27,30):
                if hour == 12:
                    ampm = 'pm'
                if hour == 13:
                    hour = 1
                row = """%s
%s""" % (row, self.wrapcell("""%s %s""" % (hour, ampm),'Time'))
                hour+=1
            else:
                row = """%s
%s""" % (row, self.wrapcell('', 'Time'))
        row = self.wraprow(row)
        return row