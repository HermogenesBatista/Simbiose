# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from models.Model import ConectCassandra

__author__ = 'Administrador'

if __name__ == "__main__":
    bd = 'test'
    cluster = ConectCassandra(bd)
    cluster.session.execute('''CREATE KEYSPACE IF NOT EXISTS '''+cluster.keyspace+'''
    WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3};''')
    cluster.conect()

    cluster.session.execute('''CREATE TABLE IF NOT EXISTS users(
                            id uuid,
                            date timestamp,
                            user_name varchar,
                            gender varchar,
                            birth_year bigint,
                            PRIMARY KEY(id, date));
                        ''')

