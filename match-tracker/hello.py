# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 09:59:40 2015

@author: fergal

$Id$
$URL$
"""

__version__ = "$Id$"
__URL__ = "$URL$"


# Import PySide classes
import sys

from PySide import QtCore, QtGui, QtUiTools
import datetime

def loadUiWidget(uifilename, parent=None):
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui


class FieldOfPlay(QtGui.QWidget):
    def __init__(self, parent=None, uiFile="pitch.ui"):
        super(FieldOfPlay, self).__init__(parent)

        self.startTime = datetime.time.now()

        self.setMinimumSize(410, 530)
        self.setMaximumSize(410, 530)
        self.eventList = []


    def mousePressEvent(self, event):
#        super(FieldOfPlay, self).mousePressEvent(event)
        print "In mousePress"
        x_window = event.x()
        y_window = event.y()

        eventTime = (datetime.time.now() - self.startTime)/60.

        x,y = self.getFieldPosition(x_window, y_window)
#        print x,y

        gameEventType = SelectGameEventDialog.getIncidentType()
        team, number = SelectPlayerDialog.getPlayer()

#        print team, number
#        print "%s by %s at (%.3f %.3f)" %(gameEventType, number, x, y)
#        print "%s by %s at (%.3f %.3f)" %(gameEventType, 5, x, y)
        event = (eventTime, x, y, gameEventType, team, number)
        print event
        self.eventList.append(event)


    def getFieldPosition(self, x_window,y_window):
        """@TODO Map normalised coords to some distorted map that
        emphasises the region near goal
        """
        geom = self.geometry()
        height_window = geom.height()
        width_window = geom.width()

        x_norm = x_window / float(width_window)
        y_norm = y_window / float(height_window)

        return x_norm, y_norm


    def display(self):
        pass

class SelectPlayerDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(SelectPlayerDialog, self).__init__(parent)

        self.team1 = "Us"
        self.team2 = "Them"

        #Set Defaults:
        self.teamSelection = self.team1
        self.playerSelection = "1"

        self.initUi()

    @staticmethod
    def getPlayer(parent=None):
        dialog = SelectPlayerDialog(parent)
        dialog.exec_()
        return dialog.getResult()


    def getResult(self):
        return self.teamSelection, self.playerSelection


    def initUi(self):
        #@TODO. I should pass names of teams to this dialog
        buttonBox = QtGui.QHBoxLayout()
        b = QtGui.QPushButton(self.team1)
        b.clicked.connect(self.setTeam)
        b.checkable = True
        b.checked = True
        buttonBox.addWidget(b)

        b = QtGui.QPushButton(self.team2)
        b.clicked.connect(self.setTeam)
        b.checkable = True
        buttonBox.addWidget(b)

        grid = QtGui.QGridLayout()
        nCols = 5
        maxPlayer = 30
        for i in range(maxPlayer):
            row = int(i/float(nCols))
            col = i - (row*nCols)
            button = QtGui.QPushButton("%i" %(i+1))
            button.clicked.connect(self.setPlayer)
            grid.addWidget(button, row, col )

        layout = QtGui.QVBoxLayout()
        layout.addLayout(buttonBox)
        layout.addLayout(grid)
        self.setLayout(layout)

        self.setWindowModality(QtCore.Qt.WindowModal)

    @QtCore.Slot()
    def setTeam(self):
        self.teamSelection = self.sender().text()
        #Clicked button should also get highlighted somehow


    @QtCore.Slot()
    def setPlayer(self):
        self.playerSelection = self.sender().text()
        self.close()


class SelectGameEventDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(SelectGameEventDialog, self).__init__(parent)

        #@TODO Read this from a file
        self.actionList = "Goal Point Wide FreeWon FreeLost HopBall Red Yellow Black OwnKickOutWon OwnKickOutLost TheirKickOutWon TheirKickoutLost".split()

        self.initForm()
        self.show()

    @staticmethod
    def getIncidentType(parent=None):
        dialog = SelectGameEventDialog(parent)
        dialog.exec_()
        value = dialog.value
#        print "Get Incident type says %s" %(value)
        return value


    def initForm(self):

        nCols = 3
        grid = QtGui.QGridLayout()
        for i in range(len(self.actionList)):
            row = int(i/float(nCols))
            col = i - (row*nCols)
            button = QtGui.QPushButton(self.actionList[i])
            button.clicked.connect(self.returnSignal)
            grid.addWidget(button, row, col )

        self.setLayout(grid)
        #Pause excecution of main window while asking for input
        self.setWindowModality(QtCore.Qt.WindowModal)

    @QtCore.Slot()
    def returnSignal(self, signal=None):
        value = self.sender().text()
        print "Button %s pushed" %(value)
        self.value = value
        self.close()




def main():
    app = QtGui.QApplication(sys.argv)
    # Create a Label and show it
#    label = QtGui.QLabel("Hello World")

#    mainWindow = IncidentSelector()
    mainWindow = FieldOfPlay()
    mainWindow.show()

    # Enter Qt application main loop
    app.exec_()
    sys.exit()


if __name__ == "__main__":
    main()
