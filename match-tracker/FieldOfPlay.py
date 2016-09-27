# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 14:41:01 2015

@author: fergal

$Id$
$URL$

@TODO:
Alpha of points should fade with age.
Add Unknown player option
Adding an event should start timer
"""

__version__ = "$Id$"
__URL__ = "$URL$"




from PySide import QtCore, QtGui
import datetime
import sys


class FieldOfPlay(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        width = 400
        height = 600
        super(FieldOfPlay, self).__init__(0,0, width, height, parent)
        self.eventList = []

        self.startTime = datetime.datetime.now()
        self.drawField()


    def mousePressEvent(self, event):
        print "In mousePress"

        #Get details of event
        eventTime = (datetime.datetime.now() - self.startTime).seconds
        eventTime = "%6i" %(eventTime)
        x = event.scenePos().x()
        y = event.scenePos().y()

        xStr = "%.3f" %(x)
        yStr = "%.3f" %(y)
        gameEventType = SelectGameEventDialog.getIncidentType()
        team, number = SelectPlayerDialog.getPlayer()

        event = (str(eventTime), xStr, yStr, gameEventType, team, number)
        print event
        self.eventList.append(event)

        #@TODO: call a method to redraw?
        colour = QtGui.QColor(240, 24, 24, 255)
        p = QtCore.QRectF(x-5, y-5, 14, 10)
        self.addEllipse(p, brush=colour)


    def drawField(self):
        self.setBackgroundBrush(QtGui.QColor(0, 127, 0, 255))
        length_m = float(2*65 + 10)

        #Draw the goals
        y0 = 0
        y = 14/length_m
        y6 = 6/length_m
        self.drawGoals(y0, y, y6)

        y0 = 1
        y = 1 - 14/length_m
        y6 = 1 - 6/length_m
        self.drawGoals(y0, y, y6)

        #Draw the outfield lines
        y = 14/length_m
        self.drawLine(0, 1, y, y)
        self.drawLine(0, 1, 1-y, 1-y)

        y = 21/length_m
        self.drawLine(0, 1, y, y)
        self.drawLine(0, 1, 1-y, 1-y)

        y = 45/length_m
        self.drawLine(0, 1, y, y)
        self.drawLine(0, 1, 1-y, 1-y)

        y = 65/length_m
        self.drawLine(0, 1, y, y)
        self.drawLine(0, 1, 1-y, 1-y)

        self.drawLine(.45, .55, .5, .5)


    def drawGoals(self, y0, y, y6):
        self.drawLine(.34, .34, y0, y)
        self.drawLine(.64, .64, y0, y)

        self.drawLine(.4, .4, y0, y6)
        self.drawLine(.6, .6, y0, y6)
        self.drawLine(.4, .6, y6, y6)

    def drawLine(self, x0, x1, y0, y1):
        xm0, ym0 = self.transformNormToMouse(x0, y0)
        xm1, ym1 = self.transformNormToMouse(x1, y1)

        colour = QtGui.QColor(255, 255, 255,255)
        self.addLine(QtCore.QLineF(xm0, ym0, xm1, ym1), colour)


    def transformMouseToNorm(self, x, y):
        height_window = self.height()
        width_window = self.width()

        x_norm = x / float(width_window)
        y_norm = y / float(height_window)

        return x_norm, y_norm


    def transformNormToMouse(self, x, y):
        height_window = self.height()
        width_window = self.width()

        x_mouse = x * width_window
        y_mouse = y * height_window

        return x_mouse, y_mouse


    def getEventList(self):
        return self.eventList


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

        button.setText("0")
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
    """
    Usage:
    s = SelectGameEventDialog.getIncidentType()
    iType = s.value
    """

    def __init__(self, parent=None):
        super(SelectGameEventDialog, self).__init__(parent)

        #@TODO Read this from a file
        self.actionList = """GoalScored  GoalConceded
            PointScored PointConceded
            Wide WideConceded   45  45Conceded
            Turnover BallLost
            PassWon PassLost
            OwnKickoutWon  OwnKickoutLost
            ThierKickoutWon TheirKickoutLost
            FreeWon FreeConceded
            RedCard YellowCard BlackCard""".split()

        self.initForm()
        self.show()

    @staticmethod
    def getIncidentType(parent=None):
        dialog = SelectGameEventDialog(parent)
        dialog.exec_()
        value = dialog.value
        return value


    def initForm(self):

        nCols = 4
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
    p = FieldOfPlay()

    win = QtGui.QGraphicsView(p)
    win.show()

    # Enter Qt application main loop
    app.exec_()
    sys.exit()


if __name__ == "__main__":
    main()
