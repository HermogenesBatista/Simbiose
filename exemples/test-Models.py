# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import uuid
from cassandra.cluster import Cluster


__author__ = 'Administrador'

class Aluno:

    def __init__(self, user_name='', gender='', birth_year=''):
        self.id = uuid.uuid4()
        self.user_name = user_name
        self.gender = gender
        self.birth_year = birth_year


if __name__ == "__main__":
    clust = Cluster()
    clust.connect()
    clust.session.set_keyspace('test')

    usr = Aluno('Layane', 'F', 1996)
    session.exect(consulta=query, user=users)
    session.print_results(session.result)