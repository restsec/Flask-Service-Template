# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 09:46:12 2018

"""

import collections
import time, datetime
import logging
import hashlib
import decimal
from db.connection import PostgresDbHelper
import services.services as serv


SQL_STMT_REF_BY_CARG_VIG = """
        	SELECT pc.id_plano_carreira, cp.de_classe, cp.de_nivel_padrao, s.vr_subsidio
		        FROM folha.foltb006_subsidio s
	        INNER JOIN folha.foltb004_plano_carreira pc
		        on s.id_plano_carreira = pc.id_plano_carreira
	        INNER JOIN folha.foltb003_classe_x_padrao cp
		        on pc.id_classe_x_padrao = cp.id_classe_x_padrao
	        WHERE pc.id_cargo = {} and s.id_vigencia = {}
	        ORDER BY cp.de_classe, cp.de_nivel_padrao
            """
            
# get all remuneracao from database, using the PostgresDbHelper object
def get_remuneracao_vigente(conn, id_cargo, vigencia):
    # Convert query to row arrays
    d = {}
    d = collections.OrderedDict()
    cargo = {}
    cargo['id'] = id_cargo
    d['cargo'] = cargo
    d['vigencia'] = vigencia
    refs = []
    rows_ref = conn.retrieve(SQL_STMT_REF_BY_CARG_VIG.format(id_cargo, vigencia['id']))
    for row_ref in rows_ref:
        ref = collections.OrderedDict()
        ref['id'] = row_ref[0]
        ref['classe'] = row_ref[1]
        ref['padrao'] = row_ref[2]
        vlr = decimal.Decimal(row_ref[3])
        ref['valor'] = str(vlr)
        refs.append(ref)
    d['valores'] = refs
    d['uri'] = "/cargo/{}".format(id_cargo)
    return d

