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

    while True:
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

            print(len(cassandra_iter))
            print(len(elastic_search))
            count = 0
            i = 0
            sincronizado = []
            for row in cassandra_iter:
                indice = sync.exist_id(row, elastic_search)

                if(indice):
                    try:
                        dt_elastic = sync.transf_datetime(prepare_to_cassandra[1]['date'])

                    except:
                        dt_elastic = sync.transf_datetime(prepare_to_cassandra[indice][1]['date'])

                    #print('ElasticSearch ', prepare_to_cassandra[indice])
                    #print("Cassandra", dados_cassandra[i])
                    #print(dt_elastic, dados_cassandra[i]['date'])

                    verifica = sync.verifica_data(dt_elastic, dados_cassandra[i]['date'])
                    if(verifica == 1):
                        #print('Elastic Menor - Prevalece o Cassandra')
                        es.received_to_cassandra(type=typeDB, dados=dados_cassandra[i])
                    elif(verifica == 3):
                        #print('Cassandra Menor - Prevalece o ElasticSearch')
                        cluster.received_to_elasticsearch(prepare_to_cassandra[indice])
                        #print(prepare_to_cassandra[indice])

                    #else:
                    #   print('Datas Iguais - Mantem')

                    sincronizado.append(row)
                    count += 1

                else:
                    #print('vai inserir no ElasticSearch e remover o índice na listagem dos Dados do Cassandra')
                    es.received_to_cassandra(type=typeDB, dados=dados_cassandra[i])

                i += 1

            i = 0
            for row in elastic_search:
                verificado = sync.exist_id(row, sincronizado)

                if(not verificado):
                    #print(prepare_to_cassandra[i])
                    #print(i)
                    cluster.received_to_elasticsearch(prepare_to_cassandra[i])
                    #print('efetuar insert')

                i += 1

            #print(sincronizado)
            #print(len(elastic_search))
            #print('qut encontrados: ', count)
            #print(prepare_to_cassandra[0])
            #print(len(dados_cassandra))


            #print(sync.exist_id(cassandra_iter[0], elastic_search))
            #print('Cassandra', cassandra_iter)
            #print('ElasticSearch', elastic_search)

            #print(cassandra_iter[0])
            #print(dados_cassandra[0])
            #print(prepare_to_cassandra[0])

        print(datetime.now())

        time.sleep(sync.time)
