from rethinkdb import RethinkDB

r = RethinkDB()

DBNAME = 'THATDB'
DBNAME_TABLES = [
    'THATDBTABLE1',
    'THATDBTABLE2'
]

def Connection(RDB_HOST, RDB_PORT):
    return r.connect(host=RDB_HOST, port=RDB_PORT)


def CloseConnection(Connection):
    Connection.close()

def get_document_by_id(DATABASE, TABLE, ID, Connection):
    return r.db(DATABASE).table(TABLE).get(ID).run(Connection)

def delete_document_by_id(DATABASE, TABLE, ID, Connection):
    '''
    deletes and return the number of deletions. Expect 1 or 0
    '''
    return r.db(DATABASE).table(TABLE).get(ID).delete().run(Connection)['deleted']

def insert(DATABASE, TABLE, DATA, Connection):
    return r.db(DATABASE).table(TABLE).insert(DATA).run(Connection)

def update(DATABASE, TABLE, DATA, Connection):
    return r.db(DATABASE).table(TABLE).get(DATA["id"]).update(DATA).run(Connection)

def dbSetup(connection):
    create_db_if_non_existant(DBNAME, connection)
    list(map(lambda e: create_table_if_non_existant(DBNAME, e, connection), DBNAME_TABLES))
    
    print('Database setup completed.')


def create_table_if_non_existant(DATABASE, TABLE, connection):
    if r.db(DATABASE).table_list().contains(TABLE).run(connection):
        return {'tables_created': 0}
    else:
        return r.db(DATABASE).table_create(TABLE).run(connection)


def create_db_if_non_existant(DATABASE, connection):
    # TODO REFACTOR TO contains.do( r.branch) BLOCK
    if r.db_list().contains(DATABASE).run(connection):
        return {'dbs_created': 0}
    else:
        r.db_create(DATABASE).run(connection)
    # r.db_list().contains(DATABASE).do(r.branch(True,{ 'dbs_created': 0 },r.db_create(DATABASE))).run(connection)
