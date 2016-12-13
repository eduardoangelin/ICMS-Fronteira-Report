# coding=utf-8
import pandas
import csv
import codecs
from br.com.autonorte.anp.util.Constantes import Constantes


def readCSV(filename, delimiter=Constantes.delimiter):
	with codecs.open(filename, 'r', encoding='latin1') as csvfile:
		freader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
		
		for row in freader:
			data = ', '.join(row)
			print (data)


def readCSV2PandasDF(filename, delimiter=Constantes.delimiter):
	data = pandas.read_csv(filename, delimiter=delimiter, encoding='latin1', dtype=str)
	return data

def convertPandasDF2Matrix(df): # returning a numpy (nd)array
	ndArray = df.as_matrix()
	ndArray = ndArray.T # transpose, other matrix operations also supports
	return ndArray

def splitFile(path, number_lines):
	with open(path) as f:
		content = f.readlines();
	
	splited = content
	listFiles = []
	actualFile = []
	for i in splited:
		if len(actualFile) > number_lines:
			listFiles += [actualFile]
			actualFile = []
		actualFile += [i]

		
	count = 1
	out = ""
	for i in listFiles:
		out = "\n".join(i)

		filebyPoint = path.split(".")
		if (len(filebyPoint) == 2):
			outputFile = filebyPoint[0]+"_Part"+str(count)+"."+filebyPoint[1]
		else:
			outputFile = path+str(count)
		
		with open(outputFile,'w') as f:
			print(outputFile)
			f.write(out)
			f.close()

		out = ""
		count+=1

def writePandasDF2CSV(filename, df, delimiter=";"):
	df.to_csv(filename, delimiter=delimiter, encoding='cp1252')


def writeFile(filename, content):
	f = open(filename, "w")
	f.write(content)
	f.close()
	
def writeCSV(filename, rowsReport):
	csvfile = open(filename+'.csv', 'wb')
	#writer = csv.writer(csvfile)
	for row in rowsReport:
		csvfile.write(row+"\n")
		#writer.writerow(row)
	csvfile.close()
