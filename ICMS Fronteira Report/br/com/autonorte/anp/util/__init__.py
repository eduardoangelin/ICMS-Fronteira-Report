
from br.com.autonorte.anp.util.Constantes import Constantes

def applyMask(cod_cta, mask):
    result = ''
    cod_cta = str(cod_cta).replace('.', '')
    countMask = 0
    for i in range(len(cod_cta)):
        while(mask[countMask] =='.'):
            result += '.'
            countMask += 1
        result += cod_cta[i]
        countMask += 1
    return result

def applyNivel(cod_cta):
    result = str(len(cod_cta.split('.')))
    return result

def getCOD_CTA_SUP(cod_cta):
    listcods = cod_cta.split(".")
    del listcods[-1]
    return ".".join(listcods)
    
    
if __name__ == '__main__':
    print (applyMask("11101234", Constantes.mask))
