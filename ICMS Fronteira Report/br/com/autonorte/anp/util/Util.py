# -*- coding: UTF-8 -*-
'''
Created on 13 de mar de 2016

@author: Angelin
'''
import os
import pandas as pd
from br.com.autonorte.anp.util.Constantes import Constantes

class Util(object):
	'''
	classdocs
	'''

	def __init__(self):
		'''
		Constructor
		'''

	def getDictConnection(self):
		pass
	
	def cnpjFormat(self, cnpj):
		try:
			if (pd.isnull(cnpj) is True):
				return cnpj
			else:
				result = "00000000000000"+str(cnpj)
		except:
			result = "00000000000000"+str(int(cnpj))
		
		result = "{}.{}.{}/{}-{}".format(result[-14:-12], result[-12:-9], result[-9:-6], result[-6:-2], result[-2:])
		return result
	
	def checkANPdir(self):
		directory = Constantes.directory
		if not os.path.exists(directory):
			os.makedirs(directory)
	
	def formatString(self, vlist):
		strRows = []
		for i in vlist:
					try:
						strRows += [str(i)]
					except:	
						strRows += [str(i.encode("UTF-8"))]
		return strRows