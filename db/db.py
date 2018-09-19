# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 09:46:12 2018

"""

import collections
import time, datetime
import logging
import hashlib
import decimal
import psycopg2

from db.connection import PostgresDbHelper
import services.services as serv


SQL_STMT_ONE_ENTITY = """
            SQL FROM DATABASE
            """
SQL_STMT_INSERT = """
            SQL TO INSERT
            """
            
# get single entity from database, using the PostgresDbHelper object
def get_one(codigo, conn):
    try:
        rows = conn.retrieve(SQL_STMT_ONE_ENTITY.format(codigo))
    except psycopg2.DatabaseError as error:
        logging.exception(error)
        logging.exception("Exception while trying to execute statment: {}".format(SQL_STMT_ONE_ENTITY))
        raise 
        
    if not rows:
        return None

    objects_list = []

    for row in rows:
        d = collections.OrderedDict()
        d['codigo'] = row[0]
        d['descricao'] = row[1]
        d['uri'] = 'api/nome-api/{}'.format(row[0])
        objects_list.append(d)

    return objects_list

# insert into rubrica, using the PostgresDbHelper object
def insert(new_object, conn):
    parsed_sql = SQL_STMT_INSERT.format(new_object['codigo'], new_object['descricao'])
    try:
        if conn.persist(parsed_sql):
            return True
    except psycopg2.DatabaseError as error:
        logging.exception(error)
        logging.exception("Exception while trying to execute statement: {}".format(parsed_sql))
        raise 


