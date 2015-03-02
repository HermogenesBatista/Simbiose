# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from cassandra.cluster import Cluster
from cassandra.query import dict_factory

from elasticsearch import Elasticsearch
import uuid

__author__ = 'Administrador'

class ConectCassandra:

    keyspace = None

    def __init__(self, keyspace):
        self.clust = Cluster()
        self.session = self.clust.connect()
        self.keyspace = keyspace

        self.conect()

    def conect(self):
        self.session.set_keyspace(self.keyspace)
        self.session.row_factory = dict_factory

    def exect(self, consulta, user=''):
        if user:
            self.result = self.session.execute(consulta, user)

        else:
            self.result = self.session.execute(consulta)

        if(self.result):
            return True

        return False

    def create_query(self, type_query='SELECT', table='', dados=''):

        values = " "
        if(type_query == 'SELECT'):
            query = type_query+' * FROM '+table+" "

            if(dados):
                values += " WHERE "
                cont = 0
                for key in dados[0].keys():
                    if(cont > 0):
                        values +=" AND "
                    values += key+' = %('+key+')s '

                    cont += 1

                query += values

        if(type_query == 'INSERT'):
            query = type_query+' INTO '+table+" ("

            if(dados):

                values += " VALUES("
                cont = 0

                key = dados[0].keys()

                query += key[0]
                values += '%('+key[0]+')s '

                cont += 1

                for key in dados[1].keys():

                    if(cont > 0):
                        query += ', '+key
                        values +=", %("+key+")s "
                    else:
                        query += key
                        values += '%('+key+')s '

                    cont += 1

                values += ')'
                query += ')'+values

        return query

    def print_results(self, resultado):
        for row in resultado:
            for key, values in row.iteritems():
                print key, values

    def received_to_elasticsearch(self, dados):
        r = self.create_query(type_query='INSERT', table='users', dados=dados)
        dados[0].update(dados[1])
        z = dados[0]
        self.exect(r, z)


class ConnectElasticsearch:
    retorno = ''
    result = ''

    def __init__(self, index):
        self.conn = Elasticsearch()
        self.index = index

    def insert_dados(self, type, values, key=uuid.uuid4()):
        self.result = self.conn.index(index=self.index, doc_type=type,  id=key, body=values)
        return self.result['created']

    def get_dados(self, type, values='', key='', sizes=1000):
        if not values and not key:
            self.result = self.conn.search(index=self.index, doc_type=type, size=sizes, body={'query': {'match_all': {}}})

            if(self.result['hits']['total'] > 0):
                return True
            return False

        elif(key):
            self.result = self.conn.get(index=self.index, doc_type=type, id=key, ignore=404)

            return self.result['found']

    def prepare_to_cassandra(self, row={}):
        if(row):
            try:
                doc = [{'id': row['_id']}, row['_source']]

            except:
                doc = [[{'id': r['_id']}, r['_source']] for r in self.result['hits']['hits']]

        else:
            try:
                doc = [{'id': self.result['_id']}, self.result['_source']]

            except:

                doc = [[{'id': r['_id']}, r['_source']] for r in self.result['hits']['hits']]

        self.retorno = doc

        return self.retorno
