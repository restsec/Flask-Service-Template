# -*- coding: utf-8 -*-
import requests
import json

http_gateway = "http://fastgate-service:8000"
#"http://10.30.0.94:8000"
#"http://172.19.0.3:8000"

def get_by_id(id):
    '''
    get_by_id 
    ''' 
    url = http_gateway + "/api/nome-api/{}".format(id)
    try:
        r = requests.get(url, headers={"X-fastgate-resource" : "nome-api"})
    except:
        return "Could Not Connect to Api", 500

    if r.status_code == 200:
        data = json.loads(r.text)
        return data[0], 200
    elif r.status_code == 404:
        return "Entity Not found", r.status_code
    else:
        return "Entity had an Internal Error", r.status_code
