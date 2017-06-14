
'''
Main window for pyfab.

'''


from pyqtgraph.Qt import QtGui
from traps import QTrappingPattern
from QFabGraphicsView import QFabGraphicsView
from QSLM import QSLM
from CGH import CGH
import sys

class pyfabController(QtGui.QMainWindow):
    
    def __init__(self):
        super(pyfabController, self).__init__()
        
        self.setGeometry(50,50,500,300)
        self.setWindowTitle("Pyfab")
        self.show()
        
        self.fabscreen = QFabGraphicsView(size=(640,480), gray=True, mirrored=False)
        self.fabscreen.show()
        self.pattern = QTrappingPattern(self.fabscreen)
        self.slm = QSLM()
        self.slm.show()
        self.pattern.pipeline = CGH(self.slm)
        self.fabscreen.sigFSClosed.connect(self.cleanup)
        
    def cleanup(self):
        self.slm.close()
        
    '''    
    def closeEvent(self, event):
        self.fabscreen.closeEvent(fabscreen, event)
        self.slm.close()
    '''   
        
if __name__ == '__main__':
    main()   

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    controller = pyfabController()
    #controller.show()
    sys.exit(app.exec_())
    