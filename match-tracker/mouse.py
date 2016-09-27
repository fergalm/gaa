# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:23:05 2015

@author: fergal

$Id$
$URL$
"""

__version__ = "$Id$"
__URL__ = "$URL$"



#from PySide.QtCore import *
#from PySide.QtGui import *
from PySide import QtCore, QtGui, QtUiTools


import sys


class Main(QtGui.QWidget):


    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        layout  = QtGui.QHBoxLayout(self)
        layout.addWidget(QtGui.QLabel("this is the main frame"))

    def mousePressEvent(self, QMouseEvent):
        #print mouse position
        print QMouseEvent.pos()


a = QtGui.QApplication([])
m = Main()
m.show()
sys.exit(a.exec_())