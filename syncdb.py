# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import *
import time
from models.Model import *

__author__ = 'Administrador'

if __name__ == '__main__':
    print(datetime.now())
    typeDB = 'users'

    cluster = ConectCassandra('test')
    es = ConnectElasticsearch('test')

    '''query = cluster.create_query(table=typeDB)
    cluster.exect(consulta=query)
    cluster.print_results(cluster.result)'''

    #res = es.get_dados(type=typeDB, key='eaf0accf-e960-4176-95a2-112c3ef1812b')
    res = es.get_dados(type=typeDB)

    retorno = es.prepare_to_cassandra(res)

    print(datetime.now())
