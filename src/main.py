from sanic import Sanic
from sanic_cors import CORS
from sanic import response
import argparse
import logging
import json
import os

import db.connection as connection
import controllers.controller as controller
import validators.validators as validators

server_config = {}

WORKERS = os.environ.get('WORKERS') or "8"

def load_configuration(server_config):
    """
    Preenche o parâmetro server_config com variáveis de ambiente pré-determinadas.
    
    A função tenta carregar o valor da variável de ambiente ou, se ela não 
    estiver definida, carrega um valor padrão.

    Por exemplo: o comando os.environ.get('HTTP_PORT', 8080) carrega a variável
    HTTP_PORT ou o valor padrão 8080.

    Referência: https://stackoverflow.com/questions/4906977/how-do-i-access-environment-variables-from-python
    """
    logging.debug("Carregando as variáveis de ambiente")
    server_config["HttpPort"] = os.environ.get('HTTP_PORT', 8080)
    server_config["HttpsPort"] = os.environ.get('HTTPS_PORT', 8443)
    server_config["TLSKeyLocation"] = ""
    server_config["TLSCertLocation"] = ""
    server_config['DatabaseHost'] = os.environ.get('DATABASE_HOST', '10.30.0.10')
    server_config['DatabaseName'] = os.environ.get('DATABASE_NAME', 'folha')
    server_config["DatabasePort"] = os.environ.get('DATABASE_PORT', 5432)
    server_config['DatabaseUser'] = os.environ.get('DATABASE_USER', 'sipac')
    server_config['DatabasePassword'] = os.environ.get(
        'DATABASE_PASSWORD', '1qaz2wsxsipac')
    server_config['serv_folha_master_address'] = os.environ.get(
        'FOLHA_SRV_ADDR', '10.30.0.94:8000')


def print_api_endpoints():
    """Imprime no log todos os endpoints disponibilizados por esta API."""
    logging.info(f"Endpoints do serviço Data Query Proxy:")
    for handler, (rule, router) in app.router.routes_names.items():
        for method in router.methods:
            if method not in ['OPTIONS', 'HEAD']:
                logging.info(f"- {method:6s} {rule}")


# ROUTES
app = Sanic(__name__)
cors = CORS(app, automatic_options=True)


@app.route('/api/get/<int:id>/', methods=['POST', 'OPTIONS'])                   #route registering
def post_request(request, id):
    '''
    get_request route calls controllers.controller.get_request as its logic, with the list of validators
    '''
    resp, cod = controller.post_request(request.json, server_config)
    return response.text(resp, status=cod) 


@app.route('/api/get/<int:id>/', methods=['GET', 'PUT', 'OPTIONS'])                   #route registering
def get_one_or_put(request, id):
    '''
    get_request route calls controllers.controller.get_request as its logic, with the list of validators
    '''
    if request.method == 'GET':
        resp, cod = controller.get_one(id, server_config)
        return response.text(resp, status=cod) 


    elif request.method == 'PUT':
        resp, cod = controller.get_one(id, server_config) 
        return response.text(resp, status=cod) 

# Server Setup
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s,%(msecs)-3d - %(name)-12s - %(levelname)-8s => %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)
    logging.info("Inicializando o serviço de CADASTRO da folha de pagamento")

    load_configuration(server_config)
    connection.configurar(server_config)
    logging.info(f"Configurações do serviço: {server_config}")
        
    if connection.Connection is None:
        logging.fatal("Error connecting to Database")
    
    print_api_endpoints()

    logging.info("Serviço função inicializado e pronto para uso!")

    app.run(host='0.0.0.0', port=int(server_config['HttpPort']), workers=int(WORKERS))
