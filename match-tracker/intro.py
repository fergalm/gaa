# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 16:38:10 2016

@author: fergal

$Id$
$URL$
"""

__version__ = "$Id$"
__URL__ = "$URL$"



from PySide import QtCore, QtGui
import sys

import PlayView

class IntroScreen(QtGui.QWidget):
    def __init__(self):
        super(IntroScreen, self).__init__()

        layout = QtGui.QVBoxLayout(self)

        lab1 = QtGui.QLabel("Team 1")
        layout.addWidget(lab1)
        self.input1 = QtGui.QLineEdit("Team1")
        layout.addWidget(self.input1)

        lab2 = QtGui.QLabel("Team 2")
        layout.addWidget(lab2)
        self.input2 = QtGui.QLineEdit("Team2")
        layout.addWidget(self.input2)

        lab3 = QtGui.QLabel("Location")
        layout.addWidget(lab3)
        self.inputLoc = QtGui.QLineEdit("")
        layout.addWidget(self.inputLoc)

        lab4 = QtGui.QLabel("Competition")
        layout.addWidget(lab4)
        self.inputCompetition = QtGui.QLineEdit("")
        layout.addWidget(self.inputCompetition)

        buttonLayout = QtGui.QHBoxLayout()
        self.half1Button = QtGui.QPushButton("Start 1st Half")
        self.half1Button.clicked.connect(self.startHalf)
        buttonLayout.addWidget(self.half1Button)

        self.half2Button = QtGui.QPushButton("Start 2nd Half")
        self.half2Button.setEnabled(False)
        self.half2Button.clicked.connect(self.startHalf)
        buttonLayout.addWidget(self.half2Button)

        quitButton = QtGui.QPushButton("Quit")
        quitButton.clicked.connect(self.close)
        buttonLayout.addWidget(quitButton)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    @QtCore.Slot()
    def startHalf(self):
        caller = self.sender().text()

        if caller == "Start 1st Half":
            self.half1Button.setEnabled(False)
            self.half2Button.setEnabled(True)

            pv = PlayView.PlayView(self.input1.text(), self.input2.text(), \
                self.inputLoc.text(), self.inputCompetition.text(), 1)
            pv.setWindowModality(QtCore.Qt.WindowModal)
            pv.setVisible(True)
        else:
            self.half2Button.setEnabled(False)
            pv = PlayView.PlayView(self.input1.text(), self.input2.text(), \
                self.inputLoc.text(), self.inputCompetition.text(), 2)


        print " %s Button pushed" %(caller)

def main():
    app = QtGui.QApplication(sys.argv)
    p = IntroScreen()
    p.show()

    # Enter Qt application main loop
    app.exec_()
    sys.exit()


if __name__ == "__main__":
    main()
