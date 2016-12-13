# -*- coding: UTF-8 -*-
'''
Created on 13 de mar de 2016

@author: Angelin
'''
from br.com.autonorte.anp.Importer import CSV
import pandas as pd
import sys
from br.com.autonorte.anp.util.Util import Util
from br.com.autonorte.anp.util.Constantes import Constantes

class SefazReports(object):
	'''
    classdocs
    '''
	def __init__(self):
		pass
	
	def myInit(self, filenameANL, filenameSefaz):
		self.filenameANL = filenameANL
		self.filenameSefaz = filenameSefaz
		self.dfANL = CSV.readCSV2PandasDF(filenameANL)
		self.dfSEFAZ = CSV.readCSV2PandasDF(filenameSefaz)
		
		self.dfANL['CNPJ'] = self.dfANL['CNPJ'].apply(lambda x: x if pd.isnull(x) is True else str(x).replace(".", "").replace("-", "").replace("/", ""))
		self.dfSEFAZ['CNPJ EMITENTE'] = self.dfSEFAZ['CNPJ EMITENTE'].apply(lambda x: x if pd.isnull(x) is True else str(x).replace(".", "").replace("-", "").replace("/", ""))
		self.dfANL['NUMERONF'] = self.dfANL['NUMERONF'].apply(lambda x: x if pd.isnull(x) is True else str(int(str(x))))
		self.dfSEFAZ['NOTA FISCAL'] = self.dfSEFAZ['NOTA FISCAL'].apply(lambda x: x if pd.isnull(x) is True else str(int(str(x))))
	
	def geraModelo(self):
		vHeaderSefaz = ['REGISTRO DE NOTA', 'DATA PASSAGEM', 'NOTA FISCAL', 'UF', 'VALOR DA NF', 'ICMS DEVIDO', 'CNPJ EMITENTE']
		vHeaderSefaz = Util().formatString(vHeaderSefaz)
		linesSefaz = ";".join(vHeaderSefaz)+"\n"
		
		vHeaderANL = ['EMISSAO', 'RECBTO', 'NUMERO', 'SERIE', 'VALOR', 'RAZSOCIAL', 'CNPJ', 'UF', 'NCM', 'GRUPOTRIB', 'PRDFORNEC']
		vHeaderANL = Util().formatString(vHeaderANL)
		linesANL = ";".join(vHeaderANL)+"\n"
		
		CSV.writeFile(Constantes.directory+ur"\Modelo_SEFAZ.csv", linesSefaz)
		CSV.writeFile(Constantes.directory+ur"\Modelo_ANL.csv", linesANL)
		
	
	def checkFailsCases(self):
		filesOK = True
		
		if True in list(pd.isnull(self.dfANL['NCM'])):
			print "Arquivo {0} possui campos vazios na coluna NCM".format(self.filenameANL)
			filesOK = False
		if True in list(pd.isnull(self.dfANL['GRUPOTRIB'])):
			print "Arquivo {0} possui campos vazios na coluna GRUPOTRIB".format(self.filenameANL)
			filesOK = False
		
		return filesOK

	def rules(self, row):
		try:
			row['CNPJ'] = Util().cnpjFormat(row['CNPJ'])
			row['CNPJ EMITENTE'] = Util().cnpjFormat(row['CNPJ EMITENTE'])
			
			if (pd.isnull(row['NOTA FISCAL']) is True):
				vConfronto = 'NAO ENCONTRADO NA SEFAZ'
			else:
				vConfronto = 'OK'
			
			if (pd.isnull(row['NUMERONF']) is True):
				vAnalise = 'NAO ENCONTRADO NO ANL'
				vConfronto = 'NAO ENCONTRADO NO ANL'
			elif (str(row['UF_x'])=='PE'): 
				vAnalise = 'PE - ICMS FRONT NAO INCIDE'
			elif (str(row['ESPECIE'])=='CTE'): 
				vAnalise = 'CTE - ICMS FRONT NAO INCIDE'
			elif (str(row['ESPECIE'])=='NFEE'): 
				vAnalise = 'ENERGIA - ICMS FRONT NAO INCIDE'
			elif (str(row['ESPECIE'])=='NFST'): 
				vAnalise = 'TELEFONE - ICMS FRONT NAO INCIDE'
			elif (str(row['TIP_EMISS'])=='EMISSAO PROPRIA'): 
				vAnalise = 'EMITIDO ANL - ANULACAO OPERACAO'
			elif (pd.isnull(row['NCM']) is True or pd.isnull(row['GRUPOTRIB']) is True):
				vAnalise = 'SEM NCM OU GRUPOTRIB'
			elif (int(row['GRUPOTRIB'])==800): 
				vAnalise = 'SERVIÇO – ICMS FRONTEIRA NÃO INCIDE'
			else:
				if (pd.isnull(row['ICMS DEVIDO']) is True):
					vICMSDevido = ''
				else:
					vICMSDevido = str(row['ICMS DEVIDO'])
				
				vGrupoTrib = int(row['GRUPOTRIB'])
				row['CHAVENFE'] = " "+str(row['CHAVENFE'])
				if (vICMSDevido.strip()=='' or vICMSDevido.strip()=='0' or vICMSDevido.strip()=='-'):
					if (str(row['NCM'][0:4])=='3820' or str(row['NCM'])[0:4]=='3819' or vGrupoTrib==315):
						vAnalise = 'ICMS DEVIDO - SEFAZ N CALCULOU'
					elif (vGrupoTrib==660 or vGrupoTrib==680):
						vAnalise = 'VALIDAR GRUPO - ICMS DEVIDO P/FERRAMENTAS'
					elif (vGrupoTrib>=1 and vGrupoTrib <= 53):
						vAnalise = 'AUTO PECAS - OK S/COBRANCA'
					elif (vGrupoTrib>=100 and vGrupoTrib <= 150):
						vAnalise = 'LUBRIF - OK S/COBRANCA'
					elif (vGrupoTrib>=200 and vGrupoTrib <= 250):
						vAnalise = 'PNEUS - OK S/COBRANCA'
					elif (vGrupoTrib>=700 and vGrupoTrib <= 900):
						vAnalise = 'DIF. ALIQ (DAE 57-2) - SEFAZ N CALCULOU'
					else:
						vAnalise = "NAO FOI POSSIVEL DEFINIR UMA REGRA"
				else:
					if (str(row['NCM'][0:4])=='3820' or str(row['NCM'])[0:4]=='3819' or vGrupoTrib==315):
						vAnalise = 'ICMS DEVIDO - VALIDAR'
					elif (vGrupoTrib==660 or vGrupoTrib==680):
						vAnalise = 'VALIDAR GRUPO - ICMS DEVIDO P/FERRAMENTAS'
					elif (vGrupoTrib>=1 and vGrupoTrib <= 53):
						vAnalise = 'AUTO PECAS - CONTESTAR'
					elif (vGrupoTrib>=100 and vGrupoTrib <= 150):
						vAnalise = 'LUBRIF - CONTESTAR'
					elif (vGrupoTrib>=200 and vGrupoTrib <= 250):
						vAnalise = 'PNEUS - CONTESTAR'
					elif (vGrupoTrib>=700 and vGrupoTrib <= 900):
						vAnalise = 'DIF. ALIQ (DAE 57-2) - VALIDAR'
					else:
						vAnalise = "NAO FOI POSSIVEL DEFINIR UMA REGRA"
		except Exception as e:
			print (str(e))
			vAnalise = "OCORREU UM ERRO NA ANALISE DO REGISTRO: "+str(e)
			vConfronto = ''
		
		return (vConfronto, vAnalise)

	def report_ANL(self, filenameANL, filenameSefaz):
		self.myInit(filenameANL, filenameSefaz)
		result = pd.merge(self.dfANL, self.dfSEFAZ, left_on=['CNPJ', 'NUMERONF'], right_on=['CNPJ EMITENTE', 'NOTA FISCAL'], how='outer')
		#colSefaz = ['REGISTRO DE NOTA', 'NOTA FISCAL', 'DATA PASSAGEM', 'UF', 'VALOR DA NF', 'ICMS DEVIDO', 'CNPJ EMITENTE']
		#colANL = ['EMISSAO', 'RECBTO', 'NUMERO', 'SERIE', 'VALOR', 'RAZSOCIAL', 'CNPJ', 'UF', 'NCM', 'GRUPOTRIB', 'PRDFORNEC']
		#result = result[['b', 'c']]
		vHeader = ['Confronto Sefaz ANL', 'Status Analisado']+list(result.columns.values)
		vHeader = Util().formatString(vHeader)
		lines = ";".join(vHeader)+"\n"
		rowCount = int(len(result.index))
		rowMod = rowCount/10
		processCount = 0
		#if (self.checkFailsCases()):
		if (True):
			for index, row in result.iterrows():
				if (index%rowMod == 0 and index > 0):
					processCount += 10
					print ("processado {}% de {}".format(processCount, rowCount))
				
				(vConfronto, vAnalise) = self.rules(row)
				
				strRows = Util().formatString(list(row.values))
				#for i in row:
				#	try:
				#		strRows += [str(i)]
				#	except:	
				#		strRows += [str(i.encode("UTF-8"))]
				
				line = ";".join([vConfronto, vAnalise]+strRows)
				lines += line+"\n"
		else:
			lines = None
		return lines
			