'''
Created on 18/06/2015

@author: Michel Arruda e Karine Gomes
'''

import os
import sys
from cStringIO import StringIO
from scipy import misc
from PIL import Image
from PyQt4 import QtGui as pyQtGui

# Specify image width and height
w, h = 400, 400
# Create window
app = pyQtGui.QApplication(sys.argv)
window = pyQtGui.QWidget()
window.setWindowTitle("Fractal")
label = pyQtGui.QLabel(window)
imgx, imgy = 400, 400

def criaImagem():     
	# tamanho da imagem
	image = Image.new("RGB", (imgx, imgy))

	# Pintando na area
	xa = -2.0
	xb = 2.0
	ya = -2.0
	yb = 2.0
	# maximo de iteracoes
	maxIt = 255
	c = complex(float(editA.text()),float(editB.text()))
	
	# Julia Set
	for y in range(imgy):
	    zy = y * (yb - ya) / (imgy - 1)  + ya
	    for x in range(imgx):
	        zx = x * (xb - xa) / (imgx - 1)  + xa
	        z = zx + zy * 1j
	        for i in range(maxIt):
	            if abs(z) > 2.0:
	                break 
	            z = z * z + c
	        image.putpixel((x, y), (i % 32 * 32, i % 16 * 16, i % 8 * 8))

	image.save("juliaFr.png", "PNG")

	picfile="juliaFr.png"
	logo = os.getcwd() + "//" + picfile
	pixmap = pyQtGui.QPixmap(logo)
	label.setPixmap(pixmap)

def preCompressao():
	print "Precompressao..."
	julia = misc.imread("juliaFr.png")
	
	f = open('preCompressao.txt', 'w')
	
	palavra = ''
	for pos_linha in range(len(julia)):
		for pos_coluna in range(len(julia[pos_linha])):
			arrayPixel = julia[pos_linha][pos_coluna]
			for pos_array in range(len(arrayPixel)):				
				palavra = palavra + str(arrayPixel[pos_array]) + "_"
			palavra = palavra[:-1]	
			palavra = palavra + ";"
		palavra = palavra[:-1]
		palavra = palavra + "-"		
		f.write(palavra)	
	
	return palavra

def comprime():
	
	descomprimido = preCompressao()
	
	print "Comprime..."
	fileCompressao = open('compressao.txt', 'w')
	
    # Constroi o dicionario
	dict_size = 256
	dictionary = dict((chr(i), chr(i)) for i in xrange(dict_size))	
	
	w = ""
	result = []
	for c in descomprimido:
		
	    wc = w + c
	    if wc in dictionary:
	        w = wc
	    else:
	        result.append(dictionary[w])
	        # Insere no dicionario o wc
	        dictionary[wc] = dict_size
	        dict_size += 1
	        w = c
	
	# Saida dos dados de w
	if w:
		result.append(dictionary[w])
	
	for i in range(len(result)):
		fileCompressao.write(str(result[i])+",")
	
	return result

def descomprime():
	print "Descomprime..."
	fileDescomprime = open('descomprime.txt', 'w')
	
	fileCompressao = open('compressao.txt', 'r+')
	comprimido = fileCompressao.readline().split(",")
	
	#Construindo o dicionario
	dict_size = 256
	dictionary = dict((chr(i), chr(i)) for i in xrange(dict_size))
	ascii = dict((chr(i), chr(i)) for i in xrange(dict_size))
	result = StringIO()
	
	w = comprimido.pop(0)
	
	result.write(w)
	for k in comprimido:
		if k != "":
			try:
				if k in ascii.values():				
					if k in dictionary:
						entry = dictionary[k]
					elif k == dict_size:
					    entry = w + w[0]
					else:
					    raise ValueError('Compressao errada k: %s' % k)
					
					result.write(entry)
					
					# Insere w+entry[0] no dicionario
					dictionary[dict_size] = w + entry[0]
					dict_size += 1
					
					w = entry
				else:
					k = int(k)
					if k in dictionary:
						entry = dictionary[k]
					elif k == dict_size:
					    entry = w + w[0]
					else:
					    raise ValueError('Compressao errada k: %s' % k)
					
					result.write(entry)
					
					# Insere w+entry[0] no dicionario
					dictionary[dict_size] = w + entry[0]
					dict_size += 1
					
					w = entry
			except :			
				if k in dictionary:
					entry = dictionary[k]
				elif k == dict_size:
				    entry = w + w[0]
				else:
				    raise ValueError('Compressao errada k: %s' % k)
				
				result.write(entry)
				
				# Insere w+entry[0] no dicionario
				dictionary[dict_size] = w + entry[0]
				dict_size += 1
				
				w = entry
	
	fileDescomprime.write(result.getvalue())
	posdecompressao(result.getvalue())
	
	return 

def posdecompressao(palavra):
	print "Poscomprime..."
	image = Image.new("RGB", (imgx, imgy))

	#seleciona as linhas
	linhas = palavra.split("-")	
	for linha in range(len(linhas)):
		pixels = linhas[linha].split(";")
		for pixel in range(len(pixels)):
			cor = pixels[pixel].split("_")					
			if cor[0]:				
				image.putpixel((pixel,linha), tuple(map(int, cor)))

	image.save("Descomp.png", "PNG")

if __name__ == '__main__':
	picfile="juliaFr.png"
	logo = picfile
	print logo
	if os.path.isfile(logo):
		pixmap = pyQtGui.QPixmap(logo)
		label.setPixmap(pixmap)
		#label.setAlignment(pyQtGui.AlignCenter)
		window.resize(pixmap.width(),pixmap.height()+180)
		
		labelFuncao = pyQtGui.QLabel(window)
		labelFuncao.setText("f = a + i*b")
		labelFuncao.move(0, h)
		
		labelFuncao = pyQtGui.QLabel(window)
		labelFuncao.setText("a:")
		labelFuncao.move(0, h+15)
		
		editA = pyQtGui.QLineEdit(window)
		editA.move(0, h+30)
		editA.setFixedWidth(w)
		
		labelFuncao = pyQtGui.QLabel(window)
		labelFuncao.setText("b:")
		labelFuncao.move(0, h+50)
		
		editB = pyQtGui.QLineEdit(window)
		editB.move(0, h+65)
		editB.setFixedWidth(w)
		
		# Add a button
		btn = pyQtGui.QPushButton('Gerar', window)
		btn.clicked.connect(criaImagem)
		btn.resize(btn.sizeHint())
		btn.setFixedWidth(w)
		btn.move(0, h+23*4)    	
		
		btnComprimir = pyQtGui.QPushButton('Comprimir', window)
		btnComprimir.move(0,h+23*5)
		btnComprimir.resize(btn.sizeHint())
		btnComprimir.setFixedWidth(w)
		btnComprimir.clicked.connect(comprime)
		
		btnDescomprimir = pyQtGui.QPushButton('Descomprir', window)
		btnDescomprimir.move(0,h+23*6)
		btnDescomprimir.resize(btn.sizeHint())
		btnDescomprimir.setFixedWidth(w)
		btnDescomprimir.clicked.connect(descomprime)
		
		window.show()
		app.exec_()
	else:
	    print "Imagem nao encontrada em ",os.getcwd(),"\\",picfile