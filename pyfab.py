#!/usr/bin/env python

"""pyfab.py: Application that implements GUI holographic optical trapping."""

from pyqtgraph.Qt import QtGui
from QPyfab import QPyfab
import sys

class pyfab(QtGui.QApplication):
	
    '''
    Initializes pyfab, the application, and QPyfab, the GUI. Also handles the signal thrown by QPyfab that it has closed.
    NOTE: When using the IPython kernel with pyqtgraph 0.10 and IPython 2.4.1, the PyQt event loop exec_() is not necessary to run the program and therefore a pyfab() instance can be manipulated from the command line.
    pyfab will not run with the commands "python pyfab.py" or "ipython pyfab.py" with this implementation.
    '''
    def __init__(self, parent=None): 
        super(pyfab,self).__init__(sys.argv)
        self.qfab = QPyfab()
        self.qfab.sigClosed.connect(self.cleanup)	#connects to cleanup method when qfab is closed
    
    '''
    Closes out of pyfab by shutting down the camera, closing widgets, exiting pyfab
    '''
    def cleanup(self):
        self.qfab.fabscreen.camera.close()
        self.closeAllWindows()
        self.exit()
        
if __name__ == '__main__':
    app = pyfab()
