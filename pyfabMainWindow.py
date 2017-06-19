from pyqtgraph.Qt import QtGui, QtCore
from traps import QTrappingPattern
from QFabGraphicsView import QFabGraphicsView
from QSLM import QSLM
from CGH import CGH
import sys
        
class pyfabMainWindow(QtGui.QMainWindow):
    
    sigClosed = QtCore.pyqtSignal()
    
    def __init__(self):
        super(pyfabMainWindow, self).__init__()
        self.setUpGui()
        self.setUpFab()
    
    def setUpFab(self):
        self.fabscreen = QFabGraphicsView(size=(640,480), gray=True, mirrored=False)
        self.setCentralWidget(self.fabscreen)
        self.pattern = QTrappingPattern(self.fabscreen)
        self.slm = QSLM()
        self.slm.show()
        self.pattern.pipeline = CGH(self.slm)
        self.show()
    
    def setUpGui(self):
        #set geometry, window appearance
        self.setGeometry(640,480,960,720)
        self.setWindowTitle("Pyfab")
        #set menu bar
        mainMenu = self.menuBar()
        mainMenu.addMenu('&Calibrate')
        self.show()
         
    def closeEvent(self, event):
        result = QtGui.QMessageBox.question(self,
                      "Confirm quit",
                      "Are you sure you want to quit?",
                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:
            event.accept()
            self.fabscreen.camera.close()
            self.sigClosed.emit()
        else:
            event.ignore()
        
if __name__ == '__main__':
    main()   

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    controller = pyfabController()
    sys.exit(app.exec_())