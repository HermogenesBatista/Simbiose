# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from models.Model import *
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
