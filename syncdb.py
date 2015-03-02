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

    '''dados = {
        'user_name': 'Layane Rodrigues da Silva',
        'gender': 'F',
        'birth_year': randint(1900, 2015),
        'date': datetime.now()
    }

    doc = [{'id': uuid.UUID('eaf0accf-e960-4176-95a2-112c3ef1812b')}, dados]'''

    #elastic = es.get_dados(typeDB, key=doc[0]['id'])
    elastic = es.get_dados(typeDB)

    #query = cluster.create_query(table=typeDB, dados=doc)

    query = cluster.create_query(table=typeDB)

    cassandra = cluster.exect(query)
    #cassandra = cluster.exect(query, doc[0])

    if(elastic and cassandra):
        dados_cassandra = cluster.result

        prepare_to_cassandra = es.prepare_to_cassandra(es.result)

        cassandra_iter = sync.iterable_resources(dados_cassandra)
        elastic_search = sync.iterable_resources(prepare_to_cassandra)

        for row in elastic_search:
            indice = sync.exist_id(row, cassandra_iter)

            if(indice):
                print(indice)
                '''aqui deveria excluir o indice da listagem dos recursos dentro da lista do cassandra'''

        print(prepare_to_cassandra[0])
        print(dados_cassandra[0])
        try:
            dt_elastic = sync.transf_datetime(prepare_to_cassandra[1]['date'])

        except:
            dt_elastic = sync.transf_datetime(prepare_to_cassandra[0][1]['date'])

        if(sync.verifica_data(dt_elastic, dados_cassandra[0]['date'])):
            print('Elastic Menor - Prevalece o Cassandra')
        else:
            print('Cassandra Menor - Prevalece o ElasticSearch')

        #print(sync.exist_id(cassandra_iter[0], elastic_search))
        #print('Cassandra', cassandra_iter)
        #print('ElasticSearch', elastic_search)

        #print(cassandra_iter[0])
        #print(dados_cassandra[0])
        #print(prepare_to_cassandra[0])

    print(datetime.now())
