# -*- coding: UTF-8 -*-
'''
Created on 13 de mar de 2016

@author: Angelin
'''

from br.com.autonorte.anp.util.Util import Util
from br.com.autonorte.anp.util.Constantes import Constantes
from br.com.autonorte.anp.reports.SefazReport import SefazReports
from br.com.autonorte.anp.Importer import CSV


if __name__ == '__main__':
	Util().checkANPdir()
	
	continueMenu = True
	while (continueMenu):
		print ('\n###################### MENU ######################')
		#print ('1 - Gerar Modelos')
		print ('2 - Analise ICMS Fronteira')
		print ('0 - SAIR')
		choice = str(raw_input('OPCAO: ').replace("\n", ""))
		#choice = '2'
		if (choice == '0'):
			continueMenu = False
		else:
			#if (choice == '1'):
				#SefazReports().geraModelo()
			if (choice == '2'):
				filenameANL = str(raw_input('Planilha CSV ANL: ').replace("\n", ""))
				filenameSefaz = str(raw_input('Planilha CSV SEFAZ: ').replace("\n", ""))
				#filenameSefaz = ur'C:\ANP Report\Extrato Calculadas 102016 - CSV.csv'
				#filenameANL = ur'C:\ANP Report\10_2016_MOV ANL DE 1_10_A_15_11_2016.csv'
				#filenameSefaz = ur'E:\ICMS Fronteira\EXTRATO_SEFAZ_2016_COMP.csv'
				#filenameANL = ur'E:\ICMS Fronteira\ANL_2016_JAN_A_NOV16_ENTRADAS.csv'
				#filenameANL = ur'E:\Python Report\ANL_092016.csv'
				#filenameSefaz = ur'E:\Python Report\Extrato SEFAZ.csv'
				try:
					rowsReport = SefazReports().report_ANL(filenameANL, filenameSefaz)
				except Exception as e:
					print ("Erro Inesperado:\n%s",e)
					rowsReport = None
				
				if (rowsReport is not None):
					CSV.writeFile(Constantes.directory+ur"\Analise_ICMS_Fronteira.csv", rowsReport)
					
			sair = str(raw_input('SAIR DO PROGRAMA(S/N): ').replace("\n", ""))
			if (sair.upper()=="S"):
				continueMenu = False
