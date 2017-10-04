#!/usr/bin/env python

"""pyfab.py: GUI for holographic optical trapping."""

from PyQt4 import QtGui
from pyfabMainWindow import pyfabMainWindow
import sys

class pyfab(QtGui.QApplication):

    def __init__(self, parent=None): 
        super(pyfab,self).__init__(sys.argv)
        #implement main window
        self.win = pyfabMainWindow()
        #get signal from mainWindow upon close to close event loop
        self.win.sigClosed.connect(self.cleanup)
      
    def cleanup(self):
        self.win.fabscreen.camera.close()
        self.closeAllWindows()
        self.exit()
        
if __name__ == '__main__':
    app = pyfab()
