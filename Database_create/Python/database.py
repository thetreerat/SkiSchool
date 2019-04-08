# Author: Harold Clark
# Copyright Harold Clark 2019
#
import sys
import os
import psycopg2

class database(object):
    """ """
    def __init__(self, user='postgres', host='127.0.0.1', port='5432', database='skischool', password=None):
        """ """
        self.cur = None
        self.password = password
        self.user = user
        self.host = host
        self.port = port
        self.database = database
        
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
    
    def call_ski_proc(self, proc, params):
        self.connect()
        self.cur.callproc(proc, [params, ])
        results = self.cur.fetchall()
        self.close()
        
        return results
    
    def close(self):
        """commit data and cloase the database connection"""
        self.db.commit()
        self.cur.close()
        self.db.close()
        