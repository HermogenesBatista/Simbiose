# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from models.Model import ConectCassandra, ConnectElasticsearch
import uuid
from random import *
from datetime import *

__author__ = 'Administrador'

class Users:

    def __init__(self, user_name='', gender='', birth_year='', session_token=''):
        self.user_name = user_name
        self.gender = gender
        self.birth_year = birth_year
        self.session_token = session_token


if __name__ == '__main__':
    '''cluster = ConectCassandra('test')
    condicao = ("Arthur",)
    query = "SELECT * FROM users WHERE gender=? "

    users = Users('Moge', 'M')

    cluster.exect(consulta=query, user=users)
    cluster.print_results(cluster.result)'''

    typeDB = 'users'

    es = ConnectElasticsearch('test')

    names = ['Moge', 'Layane', 'Arthur', 'Cristiano', 'Cesar', 'Coruripe', 'Flamengo', 'Branquinha', 'Mainha', 'Thiago', 'Renato']
    last_name = ['Batista', 'Xavier', 'Rodrigues', 'Moreira', 'Alves', 'Xum', 'Mezacaza', 'Minerva', 'Zambi', 'Souza', 'Loyota']
    sexo = ['M', 'F']


    for i in range(1000):

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
        es.insert_dados(type=typeDB, values=dados, key=id)


    #es.get_dados(type=typeDB)