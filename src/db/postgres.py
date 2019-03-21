# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017

"""

import psycopg2
import logging
import collections


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




Connection = None
logger = logging.getLogger(__name__)


class PostgresDbHelper(object):
    _db = None

    def __init__(self, DatabaseHost, DatabaseName, DatabaseUser, DatabasePassword):
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
            # cur.close()
        except Exception as e:
            logger.error(f"Rollingback transation because: {e}")
            self._db.rollback()
            raise
        else:
            logger.debug(f"Commiting transation into database")
            self._db.commit()
        return True

    def retrieve(self, sql):
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            rs = cur.fetchall()
        except Exception as e:
            logger.error(f"Error on retrieving data from database: {e}")
            raise
        else:
            return rs

    def close(self):
        self._db.close()

    def is_connection_alive(self, DatabaseHost, DatabaseName, DatabaseUser, DatabasePassword):
        if self._db.closed:
            if not DatabaseHost or not DatabaseName or not DatabaseUser or not DatabasePassword:
                    raise Exception("There is no database configuration.")
            try:
                self._db = psycopg2.connect(host=DatabaseHost, database=DatabaseName, user=DatabaseUser, password=DatabasePassword)
            except psycopg2.DatabaseError as error:
                print(error)
                logging.error(error)
                return False
            if self._db.closed: 
                return False
            else:
                return True
        else: 
            return True


def configurar(parametros):
    global Connection
    Connection = PostgresDbHelper(
        parametros['DatabaseHost'],
        parametros['DatabaseName'],
        parametros['DatabaseUser'],
        parametros['DatabasePassword']
    )
    if Connection is None:
        logging.fatal("Error connecting to Database")
