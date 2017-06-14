#!/usr/bin/env python

"""pyfab.py: GUI for holographic optical trapping."""

from pyqtgraph.Qt import QtGui
from traps import QTrappingPattern
from QFabGraphicsView import QFabGraphicsView
from pyfabController import pyfabController
from QSLM import QSLM
from CGH import CGH
import sys

class pyfab(QtGui.QApplication):

    def __init__(self):
        super(pyfab, self).__init__(sys.argv)
        self.control = pyfabController()
        self.exec_() 
        
if __name__ == '__main__':
    import sys
    app = pyfab()
