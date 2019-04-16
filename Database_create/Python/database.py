# Author: Harold Clark
# Copyright Harold Clark 2019
#
import sys
import os
import psycopg2

class database(object):
    """ """
    def __init__(self, user='postgres', host='127.0.0.1', port='5432', database='skischool', password=None, owner='Unknown'):
        """ """
        self.cur = None
        self.password = password
        self.user = user
        self.host = host
        self.port = port
        self.database = database
        self.db = None
        self.owner = owner
        print('Database object created for %s' % (self.owner))
        
    def __del__(self):
        if self.db!=None:
            if self.db.closed==0:
                self.close()
        print('Database close for owner: %s' % (self.owner))
        
    def connect(self):
        """ """
        if self.password==None:
            self.db = psycopg2.connect(user=self.user,
                                       port=self.port,
                                       host=self.host,
                                       database=self.database)
        else:
            self.db = psycopg2.connect(user=self.user,
                                       port=self.port,
                                       host=self.host,
                                       database=self.database,
                                       password=self.password)
        self.cur = self.db.cursor()
        
    
    def fetchdata(self, proc, params):
        if self.cur==None:
            self.connect()
        self.cur.callproc(proc, params)
        results = self.cur.fetchall()
        self.db.commit()
        return results
    
    def fetchdata(self, proc, params):
        if self.cur==None:
            self.connect()
        self.cur.callproc(proc, params)
        results = self.cur.fetchall()
        self.db.commit()
        return results
    
    def call_ski_proc(self, proc, params):
        self.connect()
        
        self.cur.callproc(proc, params)
        results = self.cur.fetchall()
        self.close()
        
        return results
    
    def close(self):
        """commit data and cloase the database connection"""
        self.db.commit()
        self.cur.close()
        self.db.close()
        print('Close database connnect for owner %s' % (self.owner))

 