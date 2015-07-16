'''
Created on 18/06/2015

@author: Michel Arruda
'''

import os
import sys
import numpy
import random
from PIL import Image
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# Specify image width and height
w, h = 800, 600
# Create window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Fractal")
label = QLabel(window)

def criaImagem():     
	# image size
	imgx = 512
	imgy = 512
	image = Image.new("RGB", (imgx, imgy))

	# drawing area
	xa = -2.0
	xb = 2.0
	ya = -1.5
	yb = 1.5
	maxIt = 255 # max iterations allowed

	# find a good Julia set point using the Mandelbrot set
	while True:
	    cx = random.random() * (xb - xa) + xa
	    cy = random.random() * (yb - ya) + ya
	    c = cx + cy * 1j
	    z = c
	    for i in range(maxIt):
	        if abs(z) > 2.0:
	            break 
	        z = z * z + c
	    if i > 10 and i < 100:
	        break

	# draw the Julia set
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
	logo = os.getcwd() + "\\" + picfile
	pixmap = QPixmap(logo)
	label.setPixmap(pixmap)

    
if __name__ == '__main__':
    # Create widget
    #picfile="julia.pgm"
    picfile="juliaFr.png"
    logo = os.getcwd() + "\\" + picfile
    print logo
    if os.path.isfile(logo):
        pixmap = QPixmap(logo)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        window.resize(pixmap.width(),pixmap.height()+100)

        labelFuncao = QLabel(window)
        labelFuncao.setText("f = a + i*b")
        labelFuncao.move(0, h)

        editA = QLineEdit(window)
        editA.move(0, h+25)

        editB = QLineEdit(window)
        editB.move(200, h+25) 

        # Add a button
        btn = QPushButton('Gerar', window)

        btn.clicked.connect(criaImagem)
        btn.resize(btn.sizeHint())
        btn.move(400, h+25) 

        # Draw window
        window.show()
        app.exec_()
    else:
        
        print "I expected to find a png picture called julia.png in "+ os.getcwd()

    pass