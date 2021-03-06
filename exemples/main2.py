# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from models.Model import *
from random import randrange, choice, randint
from datetime import *

__author__ = 'Administrador'

if __name__ == '__main__':
    print(datetime.now())
    typeDB = 'users'

    cluster = ConectCassandra('test')
    es = ConnectElasticsearch('test')

    '''
    doc = [
        {
            'id': uuid.uuid4()
        },
        {

            'user_name': 'Moge Batista',
            'gender': 'M',
            'birth_year': 1989,
            'date': datetime.now()

        }
    ]'''

    names = ['Moge', 'Layane', 'Arthur', 'Cristiano', 'Cesar', 'Coruripe', 'Flamengo', 'Branquinha', 'Mainha', 'Thiago', 'Renato', 'Marin', 'Joaquim', 'Juca']
    last_name = ['Batista', 'Xavier', 'Rodrigues', 'Moreira', 'Alves', 'Xum', 'Mezacaza', 'Minerva', 'Zambi', 'Souza', 'Loyota', 'Toshiba', "Brastemp", "Topadao"]
    sexo = ['M', 'F']

    arq = open('doc.txt', 'w')


    for i in range(150):
        id = uuid.uuid4()

        if randrange(0, 2) == 1:
            t = names

        else:
            t = last_name

        user_name = choice(names)+' '+choice(last_name)+' '+choice(t)

        dados = {
            'user_name': user_name,
            'gender': choice(sexo),
            'birth_year': randint(1900, 2015),
            'date': datetime.now()

        }

        doc = [{'id': id}, dados]

        if randint(0, 1) == 1:
            es.insert_dados(type=typeDB, values=dados, key=id)

            if randint(0, 1) == 1:
                r = cluster.create_query(type_query='INSERT', table='users', dados=doc)
                doc[0].update(doc[1])
                z = doc[0]
                cluster.exect(r, z)

                arq.write(str(id)+" \r"+dados['user_name'])

        else:
            if randint(0, 1) == 1:
                es.insert_dados(type=typeDB, values=dados, key=id)
                arq.write(str(id)+" \r"+dados['user_name'])


            r = cluster.create_query(type_query='INSERT', table='users', dados=doc)
            doc[0].update(doc[1])
            z = doc[0]
            cluster.exect(r, z)


    #print(doc[0])
    #print r % z
    #r = cluster.create_query(table='users', dados=doc)
    #cluster.exect(r, doc[0])

    arq.close()

    print(datetime.now())