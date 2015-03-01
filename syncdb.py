# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import *
from random import randint
import time
from models.Model import *
from models.Sync import Sincronizar

__author__ = 'Administrador'

if __name__ == '__main__':
    print(datetime.now())
    typeDB = 'users'

    cluster = ConectCassandra('test')
    es = ConnectElasticsearch('test')
    sync = Sincronizar()

    '''query = cluster.create_query(table=typeDB)
    cluster.exect(consulta=query)
    cluster.print_results(cluster.result)'''

    dados = {
            'user_name': 'Layane Rodrigues da Silva',
            'gender': 'F',
            'birth_year': randint(1900, 2015),
            'date': datetime.now()

        }

    doc = [{'id': uuid.UUID('eaf0accf-e960-4176-95a2-112c3ef1812b')}, dados]

    #elastic = es.get_dados(typeDB, key=doc[0]['id'])
    elastic = es.get_dados(typeDB)

    query = cluster.create_query(table=typeDB, dados=doc)

    l = es.prepare_to_cassandra(elastic)
    r = cluster.exect(query, doc[0])

    #print(r[0]['date'])
    #print(l[0][1]['date'].replace('T', ' '))
    dt = l[0][1]['date'].replace('T', ' ')
    #print(dt)
    dt_elastic = sync.transf_datetime(dt)

    if(sync.verifica_data(dt_elastic, r[0]['date'])):
        print('Elastic Menor')
    else:
        print('Cassandra')

    print(r)

    #r = cluster.create_query(type_query='INSERT', table='users', dados=doc)

    #print(r)
    #doc[0].update(doc[1])
    #z = doc[0]
    #cluster.exect(r, z)

    #res = es.get_dados(type=typeDB, key='eaf0accf-e960-4176-95a2-112c3ef1812b')
    #res = es.get_dados(type=typeDB)

    #retorno = es.prepare_to_cassandra(res)

    print(datetime.now())
