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


    def conect(self):
        self.session.set_keyspace(self.keyspace)
        self.session.row_factory = dict_factory


    def exect(self, consulta, user=''):

        self.conect()

        if user:
            prepared = self.session.prepare(consulta)
            self.consul = prepared.bind([user.gender])
            self.result = self.session.execute(self.consul)
            print(self.result)
        else:
            self.result = self.session.execute(consulta)

        return self.result


    def create_query(self, type_query='SELECT', table='', dados={}):

        values = " "
        if(type_query == 'SELECT'):
            query = type_query+' * FROM '+table+" "

            if(dados):
                values += " WHERE "
                cont = 0
                for key, values in dados.iteritems():
                    if(cont > 0):
                        values +=" AND "
                    values += key+' = '

    def print_results(self, resultado):
        for row in resultado:
            for key, values in row.iteritems():
                print key, values


class ConnectElasticsearch:

    def __init__(self, index):
        self.conn = Elasticsearch()
        self.index = index

    def insert_dados(self, type, values, key=uuid.uuid4()):
        self.result = self.conn.index(index=self.index, doc_type=type,  id=key, body=values)
        #print self.result['created']

    def get_dados(self, type, values='', key=''):
        if(not values):
            self.result = self.conn.search(index=self.index, doc_type=type, body={'query': {'match_all': {}}})
            print(self.result['hits'])
            print(self.result['hits']['total'])

        else:

            if(id):
                self.result = self.conn.get(index=self.index, doc_type=type, id=key)
                print(self.result['hits']['total'])
                print(self.result['hits'])

            else:
                self.result = self.conn.search()
                print(self.result['hits'])

        return self.result