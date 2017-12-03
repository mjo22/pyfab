#!/usr/bin/env python

"""pyfab_run.py: Application that implements GUI holographic optical trapping."""

from pyqtgraph.Qt import QtGui
from pyfab import pyfab
import sys

class pyfab_run(QtGui.QApplication):
	
    '''
    Initializes pyfab_run, the application, and pyfab, the GUI. Also handles the signal thrown by QPyfab that it has closed.
    Dependecies: pyqtgraph=0.10, ipython=2
    Commands for usage: 
		1) ipython
		2) from pyfab_run import pyfab_run
		3) pyfab_run()
    '''
    def __init__(self, parent=None): 
        super(pyfab_run,self).__init__(sys.argv)
        self.pyfab = pyfab()
        self.pyfab.sigClosed.connect(self.cleanup)
    
    '''
    Closes out of pyfab by shutting down the camera, closing widgets, exiting pyfab
    '''
    def cleanup(self):
        self.closeAllWindows()
        self.exit()
        
if __name__ == '__main__':
    app = pyfab_run()
    sys.exit(app.exec_())
