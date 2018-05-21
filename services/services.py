# -*- coding: utf-8 -*-
import requests
import json

def get_service_id(id):
    '''
    get_vigencia_by_id 
    ''' 
    url = "http://url/api/get_id/{}".format(id)
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.text)
        return data[0], 200
    elif r.status_code == 404:
        return "Not found", r.status_code
    else:
        return "Internal Server Error", r.status_code

