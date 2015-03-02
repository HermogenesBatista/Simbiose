# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime
__author__ = 'Administrador'

class Sincronizar:

    def __init__(self, time=5):
        self.time = time

    def verifica_data(self, data1, data2):

        if(data1 <= data2):
            return True
        else:
            return False

    def transf_datetime(self, data):
        dt = data.replace('T', ' ')
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f")

        return dt

    def iterable_resources(self, dados):
        try:
            #print(len(dados), dados)
            #print(dados[0]['id'])
            if(len(dados) > 2):
                temp = [str(ids[0]['id']) for ids in dados]
            else:
                temp = [str(dados[0]['id'])]

        except KeyError:
            #print(len(dados), dados)
            if(len(dados) > 2):
                temp = [str(ids['id']) for ids in dados]
            else:
                temp = [str(dados[0]['id'])]

        return temp

    def exist_id(self, search, lista):
        if(search in lista):
            return lista.index(search)
        else:
            return False
