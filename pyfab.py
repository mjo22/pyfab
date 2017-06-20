#!/usr/bin/env python

"""pyfab.py: GUI for holographic optical trapping."""

from pyqtgraph.Qt import QtGui
from pyfabMainWindow import pyfabMainWindow
import sys

class pyfab(QtGui.QApplication):

    def __init__(self, parent=None): 
        super(pyfab, self).__init__(sys.argv)
        #implement main window
        self.control = pyfabMainWindow()
        #get signal from controller upon close to close event loop
        self.control.sigClosed.connect(self.cleanup)
        #event loop
        self.exec_()
      
    def cleanup(self):
        self.control.fabscreen.camera.close()
        self.closeAllWindows()
        self.exit()
        
if __name__ == '__main__':
    import sys
    app = pyfab()
    