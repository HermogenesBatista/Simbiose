# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from models.Model import ConectCassandra

__author__ = 'Administrador'

if __name__ == "__main__":
    cluster = ConectCassandra('test')
    cluster.session.execute('''CREATE KEYSPACE IF NOT EXISTS '''+cluster.keyspace+'''
    WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3};''')


