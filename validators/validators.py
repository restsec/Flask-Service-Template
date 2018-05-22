# -*- coding: utf-8 -*-
from flask import request
'''
All busines and framework validation should go in here, and be parsed to the controller routes as first class citizen in the route definition (main.py)
'''

def validate_suported_mime_type():
    '''
    validate_suported_mime_type checks if media type header is application/json
    '''
    if 'Accept' in request.headers:
        test = ['*/*', 'application/json']
        hds = []
        hds = request.headers['Accept'].split(",")
        for hd in hds:
            if hd in test:
                return True
        return "Unsupported Media Type", 415
    else:
        return "Unsupported Media Type", 415
