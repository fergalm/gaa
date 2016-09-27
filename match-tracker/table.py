# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 14:41:01 2015

@author: fergal

$Id$
$URL$
"""

__version__ = "$Id$"
__URL__ = "$URL$"




from PySide import QtCore, QtGui
import sys


class EventTable(QtGui.QTableWidget):
    def __init__(self, parent=None):
        nRows = 10
        nCols = 4
        super(EventTable, self).__init__(nRows, nCols, parent)

        hdrList = "Time Event Team Player".split()
        self.setHorizontalHeaderLabels(hdrList)
        for i in range(nRows):
            for j in range(nCols):
                text = "(%i, %i)" %(i, j)
                item = QtGui.QTableWidgetItem(text)
                self.setItem(i,j, item)


def main():
    app = QtGui.QApplication(sys.argv)
    p = EventTable()
    p.show()

#    win = QtGui.QGraphicsView(p)
#    win.show()

    # Enter Qt application main loop
    app.exec_()
    sys.exit()


if __name__ == "__main__":
    main()
