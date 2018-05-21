# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017

"""

import psycopg2

Connection = None

class PostgresDbHelper(object):
    _db=None    

    def __init__(self,DatabaseHost, DatabaseName, DatabaseUser, DatabasePassword):
        if not DatabaseHost or not DatabaseName or not DatabaseUser or not DatabasePassword:
            raise Exception("There is no database configuration.")
        self._db = psycopg2.connect(host=DatabaseHost, 
                                    database=DatabaseName, 
                                    user=DatabaseUser, 
                                    password=DatabasePassword)

    def persist(self, sql):
        try:
            cur=self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
        except:
            return False
        return True

    def retrieve(self, sql):
        rs=None
        try:
            cur=self._db.cursor()
            cur.execute(sql)
            rs=cur.fetchall()
        except:
            return None
        return rs

    def close(self):
        self._db.close()
