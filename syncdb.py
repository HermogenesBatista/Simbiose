# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import *
from models.Model import *

__author__ = 'Administrador'

if __name__ == '__main__':
    print(datetime.now())
    typeDB = 'users'

    cluster = ConectCassandra('test')
    es = ConnectElasticsearch('test')

    query = cluster.create_query(table=typeDB)
    cluster.exect(consulta=query)
    cluster.print_results(cluster.result)

    es.get_dados(type=typeDB)

    print(datetime.now())
