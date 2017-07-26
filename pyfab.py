#!/usr/bin/env python

"""pyfab.py: GUI for holographic optical trapping."""

from pyqtgraph.Qt import QtWidgets
from pyfabMainWindow import pyfabMainWindow
import sys

class pyfab(QtWidgets.QApplication):

    def __init__(self, parent=None): 
        super(pyfab, self).__init__(sys.argv)
        #implement main window
        self.mainWindow = pyfabMainWindow()
        #set hologram to slm
        self.setToSlm(self.mainWindow.slm)
        #get signal from mainWindow upon close to close event loop
        self.mainWindow.sigClosed.connect(self.cleanup)
        #event loop
        if sys.platform != 'linux2':
            self.exec_()
        
    def setToSlm(self, slm):
        if slm.desktop.screenCount() == 2:
            slm.windowHandle().setScreen(self.screens()[1])
            slm.showFullScreen()
      
    def cleanup(self):
        self.mainWindow.fabscreen.camera.close()
        self.closeAllWindows()
        self.exit()
        
if __name__ == '__main__':
    import sys
    app = pyfab()
    