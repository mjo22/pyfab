#!/usr/bin/env python

"""pyfab.py: Application that implements GUI holographic optical trapping."""

from pyqtgraph.Qt import QtGuigit 
from QPyfab import QPyfab
import sys

class pyfab(QtGui.QApplication):
	
    '''
    Initializes pyfab, the application, and QPyfab, the GUI. Also handles the signal thrown by QPyfab that it has closed.
    Dependecies: pyqtgraph=0.10, ipython=2
    Commands for usage: 
		1) ipython
		2) from pyfab import pyfab
		3) pyfab()
    '''
    def __init__(self, parent=None): 
        super(pyfab,self).__init__(sys.argv)
        self.qfab = QPyfab()
        self.qfab.sigClosed.connect(self.cleanup)
    
    '''
    Closes out of pyfab by shutting down the camera, closing widgets, exiting pyfab
    '''
    def cleanup(self):
        self.closeAllWindows()
        self.exit()
        
if __name__ == '__main__':
    app = pyfab()
    sys.exit(app.exec_())
