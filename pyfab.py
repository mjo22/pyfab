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
        #event loop
        '''
        NOT WORKING ON UBUNTU 16.04. On Ubuntu 14, you didn't need to run an event loop and could control the program from the terminal
        if sys.platform != 'linux2':
            self.exec_()
        '''
        #self.exec_()
      
    def cleanup(self):
        self.win.fabscreen.camera.close()
        self.closeAllWindows()
        self.exit()
        
if __name__ == '__main__':
    app = pyfab()
