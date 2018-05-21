# -*- coding: utf-8 -*-

import json
import db.db as db
import db.connection as connection
import services.services as serv

# web service API remuneracao

def get_request(id , validators): 
    """
    get_remuneracao_vigente
    /api/get/<int:id>/ methods=['GET']
    """
    #Validation
    for validation in validators:
        result = validation()
        if result != True:
            return result
            
    # Route Logic
    v, resp = serv.get_service_id(id)
    if resp == 200:
        dados = db.get_remuneracao_vigente(connection.Connection , id, v)
    if resp == 404:
        return "NOT FOUND!", 404
    elif resp == 500:
        return "Dependent service had an internal error", 500
    else:
        return json.dumps(dados), {'Content-Type': 'application/json; charset=utf-8'}
        