# coding=utf-8
import numpy
import pandas
from br.com.dosoftware.anp.util import getCOD_CTA_SUP, applyMask, applyNivel
from br.com.dosoftware.anp.util.Constantes import Constantes
from br.com.dosoftware.anp.util.SQLServer import SQLServer


def convertIND_CTA(ind_cta):
    return str(ind_cta[0])
        
def convertCOD_NAT(cod_nat):
    cod_nat = str(cod_nat)
    if (cod_nat.find('1') != -1):
        return '01'
    if (cod_nat.find('2') != -1):
        return '02'
    if (cod_nat.find('3') != -1):
        return '03'
    if (cod_nat.find('4') != -1):
        return '04'

def convertIND_DC(ind_dc):
    return str(ind_dc[0])

def createPlanoContasDataFrame (dtCSV, dtPlanoContas):
    mask = Constantes.mask
    maxLenCTA = max(map(len, map(str, dtCSV['COD_CTA'])))
    dtPlanoContas['DT_ALT'] = ['2016-01-01' for x in dtCSV['COD_NAT']]
    dtPlanoContas['COD_NAT'] = [convertCOD_NAT(x) for x in dtCSV['COD_NAT']]
    dtPlanoContas['IND_CTA'] = [ (Constantes.ANALITICA if (maxLenCTA == len(x)) else Constantes.SINTETICA) for x in dtCSV['COD_CTA']]
    dtPlanoContas['NIVEL'] = [applyNivel(applyMask(x, mask)) for x in dtCSV['COD_CTA']]
    dtPlanoContas['COD_CTA'] = [applyMask(x, mask) for x in dtCSV['COD_CTA']]
    dtPlanoContas['COD_CTA_SUP'] = [getCOD_CTA_SUP(applyMask(x, mask)) for x in dtCSV['COD_CTA']]
    dtPlanoContas['CTA'] = dtCSV['CTA']
    dtPlanoContas['IND_DC'] = [convertIND_DC(x) for x in dtCSV['IND_DC']]
    return dtPlanoContas

def createCaixaBancoDataFrame (dtCSV, dtCaixaBanco):
    maxLenCTA = max(map(len, map(str, dtCSV['COD_CTA'])))
    for index, row in dtCSV.iterrows():
        cod_cta = applyMask(row['COD_CTA'], Constantes.mask)
        tipo_conta = row['TIPO_CONTA']
        ind_cta = (Constantes.ANALITICA if (maxLenCTA == len(row['COD_CTA'])) else Constantes.SINTETICA) 
        if (tipo_conta == Constantes.CX_BCO and ind_cta == Constantes.ANALITICA):
            newIndex = len(dtCaixaBanco)
            dtCaixaBanco.loc[newIndex, 'IDPLANOCONTAS'] = SQLServer().getIDPlanoContasByCodigo(cod_cta)
            
    return dtCaixaBanco

def createClienteFornecedorDataFrame (dtCSV, dtClienteFornecedor):
    maxLenCTA = max(map(len, map(str, dtCSV['COD_CTA'])))
    for index, row in dtCSV.iterrows():
        cod_cta = applyMask(row['COD_CTA'], Constantes.mask)
        tipo_conta = row['TIPO_CONTA']
        ind_cta = (Constantes.ANALITICA if (maxLenCTA == len(row['COD_CTA'])) else Constantes.SINTETICA) 
        if (tipo_conta == Constantes.CLI_FOR and ind_cta == Constantes.ANALITICA):
            newIndex = len(dtClienteFornecedor)
            dtClienteFornecedor.loc[newIndex, 'IDPLANOCONTAS'] = SQLServer().getIDPlanoContasByCodigo(cod_cta)
            dtClienteFornecedor.loc[newIndex, 'CLIFOR'] = 'F'
            dtClienteFornecedor.loc[newIndex, 'PESSOA'] = Constantes.PESSOA
            
    return dtClienteFornecedor

def createResultadoDataFrame (dtCSV, dtResultado, JurosDesconto):
    maxLenCTA = max(map(len, map(str, dtCSV['COD_CTA'])))
    for index, row in dtCSV.iterrows():
        cod_cta = applyMask(row['COD_CTA'], Constantes.mask)
        tipo_conta = row['TIPO_CONTA']
        ind_cta = (Constantes.ANALITICA if (maxLenCTA == len(row['COD_CTA'])) else Constantes.SINTETICA) 
        if (tipo_conta == JurosDesconto and ind_cta == Constantes.ANALITICA):
            newIndex = len(dtResultado)
            dtResultado.loc[newIndex, 'IDPLANOCONTAS'] = SQLServer().getIDPlanoContasByCodigo(cod_cta)
            
    return dtResultado

def createEmprestimoDataFrame (dtCSV, dtResultado):
    maxLenCTA = max(map(len, map(str, dtCSV['COD_CTA'])))
    for index, row in dtCSV.iterrows():
        cod_cta = applyMask(row['COD_CTA'], Constantes.mask)
        tipo_conta = row['TIPO_CONTA']
        ind_cta = (Constantes.ANALITICA if (maxLenCTA == len(row['COD_CTA'])) else Constantes.SINTETICA) 
        if (tipo_conta == Constantes.RES and ind_cta == Constantes.ANALITICA):
            newIndex = len(dtResultado)
            dtResultado.loc[newIndex, 'IDPLANOCONTAS'] = SQLServer().getIDPlanoContasByCodigo(cod_cta)
            
    return dtResultado

def createInvestimentoDataFrame (dtCSV, dtResultado):
    maxLenCTA = max(map(len, map(str, dtCSV['COD_CTA'])))
    for index, row in dtCSV.iterrows():
        cod_cta = applyMask(row['COD_CTA'], Constantes.mask)
        tipo_conta = row['TIPO_CONTA']
        ind_cta = (Constantes.ANALITICA if (maxLenCTA == len(row['COD_CTA'])) else Constantes.SINTETICA) 
        if (tipo_conta == Constantes.RES and ind_cta == Constantes.ANALITICA):
            newIndex = len(dtResultado)
            dtResultado.loc[newIndex, 'IDPLANOCONTAS'] = SQLServer().getIDPlanoContasByCodigo(cod_cta)
            
    return dtResultado

def createSaldoContaDataFrame (dtCSV, dtSaldoConta):
    maxLenCTA = max(map(len, map(str, dtCSV['COD_CTA'])))
    for index, row in dtCSV.iterrows():
        cod_cta = applyMask(row['COD_CTA'], Constantes.mask)
        ind_cta = (Constantes.ANALITICA if (maxLenCTA == len(row['COD_CTA'])) else Constantes.SINTETICA) 
        if (ind_cta == Constantes.ANALITICA):
            newIndex = len(dtSaldoConta)
            dtSaldoConta.loc[newIndex, 'IDPLANOCONTAS'] = SQLServer().getIDPlanoContasByCodigo(cod_cta)
            dtSaldoConta.loc[newIndex, 'IDCENTROCUSTO'] = None
            dtSaldoConta.loc[newIndex, 'DT_SALDO'] = Constantes.DATA_ALT
            dtSaldoConta.loc[newIndex, 'VL_SALDO'] = 0
        
    return dtSaldoConta
    
def createPlanoContasFinaceiroDataFrame(dtCSV, dtPlanoContasFinaceiro):
    maxLenCTA = max(map(len, map(str, dtCSV['COD_CTA_FIN'])))
    for index, row in dtCSV.iterrows():
        cod_cta = applyMask(row['COD_CTA'], Constantes.mask)
        cod_cta_fin = applyMask(row['COD_CTA_FIN'], Constantes.mask)
        newIndex = len(dtPlanoContasFinaceiro)

        dtPlanoContasFinaceiro.loc[newIndex, 'IDPLANOCONTAS'] = (SQLServer().getIDPlanoContasByCodigo(cod_cta) if (len(cod_cta) == maxLenCTA) else None)
        dtPlanoContasFinaceiro.loc[newIndex, 'IND_CTA'] = (Constantes.ANALITICA  if (len(cod_cta) == maxLenCTA) else Constantes.SINTETICA)
        dtPlanoContasFinaceiro.loc[newIndex, 'NIVEL'] = applyNivel(cod_cta_fin)
        dtPlanoContasFinaceiro.loc[newIndex, 'COD_CTA'] = cod_cta_fin
        dtPlanoContasFinaceiro.loc[newIndex, 'COD_CTA_SUP'] = getCOD_CTA_SUP(cod_cta_fin)
        dtPlanoContasFinaceiro.loc[newIndex, 'CTA'] = row['CTA']
        dtPlanoContasFinaceiro.loc[newIndex, 'TIPO'] = (row['TIPO']  if (len(cod_cta) == maxLenCTA) else None)
        
    return dtPlanoContasFinaceiro

def addMovimentacaoTransitoria(dtCSV, dtPlanoContasFinaceiro):
    maxLenCTA = max(map(len, map(str, dtCSV['COD_CTA_FIN'])))
    newIndex = len(dtPlanoContasFinaceiro)
    #x = (dtPlanoContasFinaceiro['COD_CTA']).tail(1)
    x = dtPlanoContasFinaceiro['COD_CTA'].values[-1]
    numericMV = str(int(x[0])+1)
    print (numericMV)
    dtPlanoContasFinaceiro.loc[newIndex] = [None, Constantes.SINTETICA, '1', numericMV, '', 'MOVIMENTACAO TRANSITORIA', None]
    
    for cod_cta_fin_sin, cta_sintetica, tipo in [((numericMV+'.01'), 'ENTRADAS', Constantes.CXE), ((numericMV+'.02'), 'SAIDAS', Constantes.CXS)]:
        newIndex = len(dtPlanoContasFinaceiro)
        dtPlanoContasFinaceiro.loc[newIndex] = [None, Constantes.SINTETICA, '2', cod_cta_fin_sin, getCOD_CTA_SUP(cod_cta_fin_sin), cta_sintetica, None]
        for index, row in dtCSV.iterrows():
            cod_cta = applyMask(row['COD_CTA'], Constantes.mask)
            cod_cta_fin = applyMask(row['COD_CTA_FIN'], Constantes.mask)
            if (cod_cta_fin[0] == '1' and (int(applyNivel(cod_cta_fin))>2)):
                newIndex = len(dtPlanoContasFinaceiro)
                cod_cta_fin = cod_cta_fin_sin + cod_cta_fin[3:]
                dtPlanoContasFinaceiro.loc[newIndex, 'IDPLANOCONTAS'] = (SQLServer().getIDPlanoContasByCodigo(cod_cta) if (len(cod_cta) == maxLenCTA) else None)
                dtPlanoContasFinaceiro.loc[newIndex, 'IND_CTA'] = (Constantes.ANALITICA  if (len(cod_cta) == maxLenCTA) else Constantes.SINTETICA)
                dtPlanoContasFinaceiro.loc[newIndex, 'NIVEL'] = applyNivel(cod_cta_fin)
                dtPlanoContasFinaceiro.loc[newIndex, 'COD_CTA'] = cod_cta_fin
                dtPlanoContasFinaceiro.loc[newIndex, 'COD_CTA_SUP'] = getCOD_CTA_SUP(cod_cta_fin)
                dtPlanoContasFinaceiro.loc[newIndex, 'CTA'] = row['CTA']
                dtPlanoContasFinaceiro.loc[newIndex, 'TIPO'] = (tipo  if (len(cod_cta) == maxLenCTA) else None)
    return dtPlanoContasFinaceiro
    

def addDisponibilidadeFinal(dtCSV, dtPlanoContasFinaceiro):
    maxLenCTA = max(map(len, map(str, dtCSV['COD_CTA_FIN'])))
    newIndex = len(dtPlanoContasFinaceiro)
    #x = (dtPlanoContasFinaceiro['COD_CTA']).tail(1)
    x = dtPlanoContasFinaceiro['COD_CTA'].values[-1]
    numericMV = str(int(x[0])+1)
    print (numericMV)
    dtPlanoContasFinaceiro.loc[newIndex] = [None, Constantes.SINTETICA, '1', numericMV, '', 'DISPONIBILIDADE FINAL', None]
    cod_cta_fin_sin = numericMV

    for index, row in dtCSV.iterrows():
        cod_cta = applyMask(row['COD_CTA'], Constantes.mask)
        cod_cta_fin = applyMask(row['COD_CTA_FIN'], Constantes.mask)
        if (cod_cta_fin[0] == '1' and (int(applyNivel(cod_cta_fin))>1)):
            newIndex = len(dtPlanoContasFinaceiro)
            cod_cta_fin = cod_cta_fin_sin + cod_cta_fin[1:]
            dtPlanoContasFinaceiro.loc[newIndex, 'IDPLANOCONTAS'] = (SQLServer().getIDPlanoContasByCodigo(cod_cta) if (len(cod_cta) == maxLenCTA) else None)
            dtPlanoContasFinaceiro.loc[newIndex, 'IND_CTA'] = (Constantes.ANALITICA  if (len(cod_cta) == maxLenCTA) else Constantes.SINTETICA)
            dtPlanoContasFinaceiro.loc[newIndex, 'NIVEL'] = applyNivel(cod_cta_fin)
            dtPlanoContasFinaceiro.loc[newIndex, 'COD_CTA'] = cod_cta_fin
            dtPlanoContasFinaceiro.loc[newIndex, 'COD_CTA_SUP'] = getCOD_CTA_SUP(cod_cta_fin)
            dtPlanoContasFinaceiro.loc[newIndex, 'CTA'] = row['CTA']
            dtPlanoContasFinaceiro.loc[newIndex, 'TIPO'] = (Constantes.CX  if (len(cod_cta) == maxLenCTA) else None)
            
    return dtPlanoContasFinaceiro

def createGeraMovimentoDataFrame (dtCSV, dtGeraMovimento):
    for idx, row in dtCSV.iterrows():
        newIndex = len(dtGeraMovimento)
        dtGeraMovimento.loc[newIndex] = [None for i in range(len(dtGeraMovimento.columns))]
        CONTA_CREDITO = applyMask(row['CONTA_CREDITO'], Constantes.mask)
        CONTA_DEBITO = applyMask(row['CONTA_DEBITO'], Constantes.mask)
        CENTROCUSTO = str(row['CENTROCUSTO'])
        
        dtGeraMovimento.loc[newIndex, 'DATA'] = row['DATA']
        dtGeraMovimento.loc[newIndex, 'DOCUMENTO'] = row['DOCUMENTO']
        dtGeraMovimento.loc[newIndex, 'CONTACREDORA'] = CONTA_CREDITO
        dtGeraMovimento.loc[newIndex, 'CENTROCUSTOCREDOR'] = CENTROCUSTO
        dtGeraMovimento.loc[newIndex, 'CONTADEVEDORA'] = CONTA_DEBITO
        dtGeraMovimento.loc[newIndex, 'CENTROCUSTODEVEDOR'] = CENTROCUSTO
        dtGeraMovimento.loc[newIndex, 'VALOR'] = row['VALOR']
        dtGeraMovimento.loc[newIndex, 'HIST'] = row['HISTORICO']
        dtGeraMovimento.loc[newIndex, 'COMANDO'] = 'I'
                
    return dtGeraMovimento


