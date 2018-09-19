# -*- coding: utf-8 -*-

import json
import logging

import db.db as db
import db.connection as connection
import services.services as serv

# stores all database configuration
database_config = {}

# web service API remuneracao

def get_one(codigo, validators, config):
    """
    routes_with_codigo_request
   /api/nome-api/{codigo} methods=['GET']
    """
    #Validation
    for validation in validators:
        result = validation()
        if result != True:
            return result

    if not is_connection_alive(config):
        return "Not able to reconnect with database", 500    
     
    try:
        dados = db.get_one(codigo, connection.Connection)
        if not dados: 
            cod = 404
            dados = "Not found"
        else:
            cod = 200
    except Exception as e:
        print(e)
        cod = 500
        dados =  "Internal problem while executing the request" 
    return json.dumps(dados), cod, {'Content-Type': 'application/json; charset=utf-8'} 
        

def post_request(new_objeto, validators, config): 
    """
    post_request
    /api/rubrica/ methods=['PUT']
    """ 
    #Validation
    for validation in validators:
        result = validation()
        if result != True:
            return result

    if not is_connection_alive(config):
        return "Not able to reconnect with database", 500

    m, c = json_validation(new_objeto)
    if c == 200:
        try:
            # TESTE PARA NÃO SOBRESCREVER ENTIDADE QUE JÁ EXISTA
            dados = db.get_one(new_objeto['codigo'], connection.Connection)
            try:
                if not dados:
                    if not exist(new_objeto['subcategoria']):
                        return "Id for subcategoria not in categoria service", 400
                    if db.insert(new_objeto, connection.Connection):
                        dados = "Ok"
                        cod = 201
                    else:
                        dados = "Id for subcategoria not in categoria service"
                        cod = 400
                else:
                    dados = "There is already a rubrica with codigo: /api/rubrica/{}".format(new_objeto['codigo'])
                    cod = 400
            except Exception as e:
                print(e)
                cod = 500
                dados =  "Internal problem while executing the request" 
        except Exception as e:
            print(e)
            cod = 500
            dados =  "Internal problem while executing the request" 

        return dados, cod, {'Location': '/api/rubrica/{}'.format(new_objeto['codigo']) , 'Content_type':"text/plain", 'Charset':"utf-8"}
    else:
        return m, c

def json_validation(objeto):
    data_validation = dict()
    data_validation['required'] = "Validação de itens not null"
    data_validation['size'] = "Checagem de tamanho dos campos"
    data_validation['regex'] = "Regex para verificação de strings, int, data, etc."
    msg = ";\n".join(list(str(v) for k, v in data_validation.items() if v))
    if msg:
        return "Bad request.\n{}.".format(msg), 400
    else:
        return None, 200

def is_connection_alive(server_config):
    try:
        logging.debug("Trying connection")
        if connection.Connection.is_connection_alive(server_config['DatabaseHost'], server_config['DatabaseName'], server_config['DatabaseUser'], server_config['DatabasePassword']):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

#Função para testar se entidade externa (pertence a outra api) existe
def exist(codigo):
    try:
        m, cod = serv.get_by_id(codigo)
        if cod == 200:
            return True
        else:
            return False
    except Exception as error:
        logging.exception(error)
        logging.exception("Exception while trying to get subcategoria from api subcategoria: {}".format(codigo))
        raise 
