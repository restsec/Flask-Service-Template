from flask import Flask, request
from flask_cors import cross_origin
from meinheld import server
import controllers.controller as controller
import validators.validators as validators
import argparse
import logging
import json
import os
import db.connection as connection


def load_configuration(config_file):
    '''
    load_configuration reads file with provided path
    '''
    filename = config_file
    if not os.path.isfile(filename):
        logging.error("Database config file is missing")
        # TODO raise exception

    configuration = json.load(open(filename))
    return configuration

def load_defaultconfiguration():
    '''
    load_defaultconfiguration adds default configuration to the server_config structure. This is used for testing purpuses only.
    '''
    server_config = {}
    server_config["Debug"]="True"
    server_config["HttpPort"]=8080
    server_config["HttpsPort"]=8443
    server_config["TLSKeyLocation"]=""
    server_config["TLSCertLocation"]=""
    server_config["DatabaseUser"]="postgres"
    server_config["DatabasePassword"]="database"
    server_config["DatabaseName"]="db"
    server_config["DatabaseHost"]="localhost"
    server_config["DatabasePort"]=5432
    return server_config

# ROUTES
app = Flask(__name__)   #

@app.route('/api/get/<int:id>/', methods=['GET'])                   #route registering
@cross_origin(origins =['*'], methods=['GET', 'HEAD', 'OPTIONS'])   #CORS configuration
def get_request(id):
    '''
    get_request route calls controllers.controller.get_request as its logic, with the list of validators
    '''
    return controller.get_request(id, [validators.validate_suported_mime_type]) # data validation function are parsed as a list

# Server Setup
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='"API Servidor" to provide/handle employee\'s data.')
    parser.add_argument("-c", "--config", 
                        help="Database config file path", metavar="config_file")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--no-ssl", action="store_true", 
                        help='Start server without SSL')
    args = parser.parse_args()

    if args.config:
        logging.info("Using Configuration File")
        logging.debug("Read from File:/n" + args.config)
        server_config = {}
        server_config = load_configuration(args.config)
        
    else:
        logging.info("Using Default Configuration")
        server_config = load_defaultconfiguration()
        logging.debug(server_config)
        
    connection.Connection = connection.PostgresDbHelper(server_config['DatabaseHost'], server_config['DatabaseName'], server_config['DatabaseUser'], server_config['DatabasePassword'])
    if connection.Connection is None:
        logging.fatal("Error connecting to Database")
    server.listen(('0.0.0.0', server_config['HttpPort']))
    server.run(app)
