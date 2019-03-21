from pymongo import MongoClient
from pymongo.errors import ConfigurationError
import json


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
            mongodb_uri = 'mongodb://'
            if database_user and database_password:
                mongodb_uri += '{}:{}@{}'.format(
                    database_name,
                    database_password,
                    database_host
                )
            else:
                mongodb_uri += database_host
            
            if database_name:
                mongodb_uri += '/{}'.format(database_name)

            self._db = MongoClient(mongodb_uri)

    @staticmethod
    def verify_input(document):
        if type(document) is str:
            document = json.loads(document)
        elif type(document) is dict:
            pass
        else:
            return None
        return document

    def default_database(self, schema=None):
        try:
            if schema:
                default = self._db.get_database(schema)
            else:
                default = self._db.get_database()
        except ConfigurationError as e:
            logger.error(str(e))
        else:
            return default

    def persist(self, query, table, schema=None):
        try:
            db = self.default_database(schema)
            query = self.verify_input(query)
            if query:
                pass
            else:
                raise Exception("Unknown data type: {}".format(
                    type(query)
                ))
        except ConfigurationError as e:
            logger.error(str(e))
        except ValueError as e:
            logger.error(str(e))
        except Exception as e:
            logger.error(str(e))
        else:
            collection = db.get_collection(table)
            result = collection.insert_many(query)
            if result:
                logger.info('Object(s) inserted: {}'.format(
                    str(result)
                ))
                return result
            else:
                logger.error('Object(s) couldn\'t be inserted for '
                             'the query: {}'.format(
                                str(query)
                                ))
                return None

    def search_one(self, query, table, schema=None):
        try:
            db = self.default_database(schema)
            query = self.verify_input(query)
            if query:
                pass
            else:
                raise Exception("Unknown data type: {}".format(
                    type(query)
                ))
        except ConfigurationError as e:
            logger.error(str(e))
        except ValueError as e:
            logger.error(str(e))
        except Exception as e:
            logger.error(str(e))
        else:
            collection = db.get_collection(table)
            result = collection.find_one(query)
            if result:
                logger.info('Object(s) found: {}'.format(
                    str(result)
                ))
                return result
            else:
                logger.error('Object(s) not found for query: {}'.format(
                    str(query)
                ))
                return None

    def search(self, query, table, schema=None):
        try:
            db = self.default_database(schema)
            query = self.verify_input(query)
            if query:
                pass
            else:
                raise Exception("Unknown data type: {}".format(
                    type(query)
                ))
        except ConfigurationError as e:
            logger.error(str(e))
        except ValueError as e:
            logger.error(str(e))
        except Exception as e:
            logger.error(str(e))
        else:
            collection = db.get_collection(table)
            result = collection.find(query)
            if result:
                logger.info('Object(s) found: {}'.format(
                    str(result)
                ))
                return result
            else:
                logger.error('Object(s) not found for query: {}'.format(
                    str(query)
                ))
                return None

    def delete(self, query, table, schema=None):
        try:
            db = self.default_database(schema)
            query = self.verify_input(query)
            if query:
                pass
            else:
                raise Exception("Unknown data type: {}".format(
                    type(query)
                ))
        except ConfigurationError as e:
            logger.error(str(e))
        except ValueError as e:
            logger.error(str(e))
        except Exception as e:
            logger.error(str(e))
        else:
            collection = db.get_collection(table)
            result = collection.delete_many(query)
            if result:
                logger.info('Object(s) deleted: {}'.format(
                    str(result)
                ))
                return result
            else:
                logger.error('Object(s) not found for query to '
                             'delete: {}'.format(
                                str(query)
                             ))
                return None

    def update(self, query, update, table, schema=None):
        try:
            db = self.default_database(schema)

            query = self.verify_input(query)
            if query:
                pass
            else:
                raise Exception("Unknown data type: {}".format(
                    type(query)
                ))

            update = self.verify_input(update)
            if update:
                pass
            else:
                raise Exception("Unknown data type: {}".format(
                    type(update)
                ))
        except ConfigurationError as e:
            logger.error(str(e))
        except ValueError as e:
            logger.error(str(e))
        except Exception as e:
            logger.error(str(e))
        else:
            collection = db.get_collection(table)
            result = collection.update_many(query, update)
            if result:
                logger.info('Object(s) updated: {}'.format(
                    str(result)
                ))
                return result
            else:
                logger.error('Object(s) not found for query to '
                             'update: {}'.format(
                                str(query)
                             ))
                return None

    def close(self):
        self._db.close()

    def is_database_locked(self):
        return self._db.is_locked

    def is_connection_alive(self):
        if self._db is None:
            return False
        else:
            return True

    def count_documents(self, table, schema=None):
        try:
            db = self.default_database(schema)
        except ConfigurationError as e:
            logger.error(str(e))
        else:
            collection = db.get_collection(table)
            result = collection.count_documents({})
            if result:
                logger.info('Number of object(s) found: {}'.format(
                    str(result)
                ))
                return result
            else:
                logger.error('No object was found for the table: {}'.format(
                    str(table)
                ))
                return None

    def get_all(self, table, schema=None):
        try:
            db = self.default_database(schema)
        except ConfigurationError as e:
            logger.error(str(e))
        else:
            collection = db.get_collection(table)
            result = [obj for obj in collection.find({})]
            if result:
                logger.info('Object(s) found: {}'.format(
                    str(result)
                ))
                return result
            else:
                logger.error('No object was found for the table: {}'.format(
                    str(table)
                ))
                return None