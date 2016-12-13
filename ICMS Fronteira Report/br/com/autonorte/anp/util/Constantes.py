# -*- coding: UTF-8 -*-
'''
Created on 13 de mar de 2016

@author: Angelin
'''

class Constantes(object):
    '''
    classdocs
    '''
    TYPE_DATE = 'DATE'
    TYPE_STR = 'STR'
    TYPE_INT = 'INT'
    TYPE_MONEY = 'MONEY'
    TYPE_QUERY = 'QUERY'
    
    directory = "C:\\ANP Report"
    mask = 'x.x.xx.xx.xxx'
    maskFinanceiro = 'x.x.xx.xx.xxx'
    delimiter = ';'
    
    
    def __init__(self, params):
        '''
        Constructor
        '''
        