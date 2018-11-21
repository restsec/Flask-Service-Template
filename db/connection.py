# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017

"""

import psycopg2
import logging
from pymongo import MongoClient
from pymongo.errors import ConfigurationError

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


class MongoDBHelper(object):
    _db = None

    def __init__(self,
                 database_host,
                 database_name,
                 database_user,
                 database_password):
        if not database_host or \
                not database_name or \
                not database_user or \
                not database_password:
            raise Exception("There is no database configuration.")
        else:
            mongodb_uri = 'mongodb://{}:{}@{}/{}'
            mongodb_uri.format(
                database_user,
                database_password,
                database_host,
                database_name
            )

            self._db = MongoClient(mongodb_uri)

    def persist(self, data, table):
        try:
            db = self._db.get_default_database()
        except ConfigurationError as e:
            logger.error(str(e))
        else:
            collection = db.get_collection(table)
            result = collection.insert_many(data)
            logger.info('Object inserted: {}'.format(
                str(result)
            ))
        return result


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

