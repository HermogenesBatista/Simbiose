# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from models.Model import *
from datetime import *

__author__ = 'Administrador'

if __name__ == '__main__':
    cluster = ConectCassandra('test')

    doc = [
        {
            'id': '4608f1d5-9348-443b-9cb6-0064e5b805b6'
        },
        {

            'user_name': 'Moge Batista',
            'gender': 'M',
            'birth_year': 1989,
            'date': datetime.now().isoformat()

        }
    ]


    r = cluster.create_query(type_query='INSERT', table='users', dados=doc)

    #print(doc[1])
    #z = dict(doc[0].items() + doc[1].items())

    doc[0].update(doc[1])
    z = doc[0]
    #print(doc[0])
    print(r % (z))

    r = cluster.create_query(table='users', dados=doc)

    print(r %(doc[0]))