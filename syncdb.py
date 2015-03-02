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

    try:
        tempo = int(input('Entre com o tempo em segundos \n(Obs: "ENTER" ou valor incorreto (não numérico) para 5 segundos de intervalo): '))
    except:
        tempo = 5

    sync = Sincronizar(tempo)

    while True:
        elastic = es.get_dados(typeDB)

        query = cluster.create_query(table=typeDB)

        cassandra = cluster.exect(query)

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
                #existencia do ID no resultado do Elasticsearch
                indice = sync.exist_id(row, elastic_search)

                if(indice):
                    try:
                        dt_elastic = sync.transf_datetime(prepare_to_cassandra[1]['date'])

                    except:
                        dt_elastic = sync.transf_datetime(prepare_to_cassandra[indice][1]['date'])

                    verifica = sync.verifica_data(dt_elastic, dados_cassandra[i]['date'])
                    if(verifica == 1):
                        # Data Elastic Menor - Prevalece o Cassandra
                        es.received_to_cassandra(type=typeDB, dados=dados_cassandra[i])
                    elif(verifica == 3):
                        # Data Cassandra Menor - Prevalece o ElasticSearch
                        cluster.received_to_elasticsearch(prepare_to_cassandra[indice])

                    #verifica = 2 equivale a data igual, não sendo necessario atualizar nada

                    #Ids já verificados na inspeção do Cassandra to Elasticsearch
                    sincronizado.append(row)
                    count += 1

                else:
                    es.received_to_cassandra(type=typeDB, dados=dados_cassandra[i])

                i += 1

            i = 0
            for row in elastic_search:
                #verificacao do ID ja verificado no Elasticsearch, ignorando essas ocorrencias
                verificado = sync.exist_id(row, sincronizado)

                if(not verificado):
                    cluster.received_to_elasticsearch(prepare_to_cassandra[i])

                i += 1

        elif(cassandra and not elastic):
            dados_cassandra = cluster.result
            cassandra_iter = sync.iterable_resources(dados_cassandra)
            i = 0
            for row in cassandra_iter:
                es.received_to_cassandra(type=typeDB, dados=dados_cassandra[i])

                i += 1

        elif(not cassandra and elastic):
            prepare_to_cassandra = es.prepare_to_cassandra(es.result)

            elastic_search = sync.iterable_resources(prepare_to_cassandra)

            i = 0
            for row in elastic_search:
                cluster.received_to_elasticsearch(prepare_to_cassandra[i])

                i += 1
        else:
            print('Ambos os bancos estão vazios! Não há dados para Sincronizar')

        print(datetime.now())

        time.sleep(sync.time)
