

#Back  [Time] Stop List

from PySide import QtCore, QtGui
import datetime
import FieldOfPlay as fop
import sys


"""

Todo:
I need a home page to enter date, venue, teams, competition
These values should make their way into the save file.

I need to deal with the second half

Make it android friendly.

Ability to use keyboard shortcuts to enter events. (not for android)

New buttons
Goal Scored / Conceded
point scored /conceded
wide by us/ wide by them
45 /
Free
Red
Yellow
Black
Our kick out won/lost
Their kickout won/lost

That's 20 buttons
"""

class PlayView(QtGui.QWidget):
    def __init__(self,  team1="Us", team2="Them", location="Unknown", \
        competition = "Friendly", period=1, parent=None):
        super(PlayView, self).__init__(parent)

        #Setup a time to update the time every second
        self.elapsedTime = 0
        self.timerId = self.startTimer(1000)
        self.isTimerOn = True

        self.saveFilename = "mt-%s-v-%s_%s_%sPeriod%s.csv" %(team1, team2, \
            location, competition, str(period))

        buttonLayout = QtGui.QHBoxLayout()
        b1 = QtGui.QPushButton("Back")
        b1.setEnabled(False)

        b2 = QtGui.QPushButton("Stop")
        b3 = QtGui.QPushButton("List")
        lab = QtGui.QLabel("00:00")
        self.timeLabel = lab
        self.startStopButton = b2
        self.startStopButton.clicked.connect(self.startStopSlot)
        b3.clicked.connect(self.showTable)

        buttonLayout.addWidget(b1)
        buttonLayout.addWidget(b2)
        buttonLayout.addWidget(b3)
        buttonLayout.addWidget(lab)

        teamLayout = QtGui.QHBoxLayout()
        lab1 = QtGui.QLabel(team1)
        lab2 = QtGui.QLabel(team2)
        lab2.setAlignment(QtCore.Qt.AlignRight)
        teamLayout.addWidget(lab1)
        teamLayout.addWidget(lab2)

        self.fieldWidget = fop.FieldOfPlay(self)
        field = QtGui.QGraphicsView(self.fieldWidget)
#        field = fop.FieldOfPlay()



#
        layout = QtGui.QVBoxLayout()
        layout.addLayout(buttonLayout)
        layout.addLayout(teamLayout)
        layout.addWidget(field)
        self.setLayout(layout)

        #DEbugging code
#        self.fieldWidget.eventList.append(tuple("Time x y Event Team Player".split()))
#        self.showTable()


    def save(self):
        fp = open(self.saveFilename, 'w')
        for row in self.fieldWidget.getEventList():
            for r in row:
                fp.write(str(r) + ",")
            fp.write("\n")
        fp.close()


    @QtCore.Slot()
    def startStopSlot(self):
        if self.isTimerOn:
            self.isTimerOn = False
            self.startStopButton.setText("Start")
            self.killTimer(self.timerId)
        else:
            self.isTimerOn = True
            self.startStopButton.setText("Stop")
            self.timerId = self.startTimer(1000)


    def timerEvent(self, timerEvent):
        self.elapsedTime += 1
        minutes = int(self.elapsedTime/60.)
        seconds = self.elapsedTime  - 60*minutes
        text = "%02i:%02i" %(minutes, seconds)
        self.timeLabel.setText(text)

        self.save()

    @QtCore.Slot()
    def showTable(self):
        """
        I need to great a new widget, add the table to it.
        also add some buttons to go back again.
        """

        if len(self.fieldWidget.getEventList()) > 0:
            table = TableView(self.fieldWidget, self)
            table.exec_()
            self.fieldWidget.eventList = table.getEventList()


class TableView(QtGui.QDialog):
    def __init__(self, fieldOfPlay, parent=None):
        super(TableView, self).__init__(parent)

        eventList = fieldOfPlay.getEventList()
        self.eventList = eventList

        #Todo, I should get this from the fieldOfPlay
        hdrList = "Time x y Event Team Player".split()
        nRows = len(eventList)
        nCols = len(eventList[0])
        assert(nCols == len(hdrList))

        table = QtGui.QTableWidget(nRows, nCols)
        table.setHorizontalHeaderLabels(hdrList)
        for i in range(nRows):
            event = eventList[i]
            for j in range(nCols):
                print event[j], type(event[j])
                item = QtGui.QTableWidgetItem(event[j])
                table.setItem(i,j, item)
        self.table = table

        layout = QtGui.QVBoxLayout()
        layout.addWidget(table)

        Bbox = QtGui.QDialogButtonBox
        buttonBox = Bbox(Bbox.Save | Bbox.Cancel)
        buttonBox.accepted.connect(self.save)
        buttonBox.rejected.connect(self.cancel)
        layout.addWidget(buttonBox)
        self.setLayout(layout)


        self.setMinimumHeight(table.height())
        self.setMinimumWidth(table.width())

    @QtCore.Slot()
    def cancel(self):
        self.close()

    @QtCore.Slot()
    def save(self):
        el = []
        nRow = self.table.rowCount()
        nCol = self.table.columnCount()
        for i in range(nRow):
            row = []
            for j in range(nCol):
                row.append( self.table.item(i,j).text())
            el.append(row)

        self.eventList = el
        self.close()

    def getEventList(self):
        return self.eventList

def main():
    app = QtGui.QApplication(sys.argv)
    win = PlayView()
    win.show()

    # Enter Qt application main loop
    app.exec_()
    sys.exit()


if __name__ == "__main__":
    main()

