from pyqtgraph.Qt import QtGui, QtCore
from traps import QTrappingPattern
from QFabGraphicsView import QFabGraphicsView
from QSLM import QSLM
from CGH import CGH
from QCGH import QCGH
import sys
import json
        
class pyfabMainWindow(QtGui.QMainWindow):
    
    sigClosed = QtCore.pyqtSignal()
    
    def __init__(self):
        super(pyfabMainWindow, self).__init__()
        self.setUpFab()
        self.setUpGui()
     
    def setUpFab(self):
        self.fabscreen = QFabGraphicsView(size=(640,480), gray=True, mirrored=False)
        self.pattern = QTrappingPattern(self.fabscreen)
        self.slm = QSLM()
        self.slm.show()
        self.pattern.pipeline = CGH(self.slm)
        self.cgh = QCGH()
        self.show()
        
    def setUpGui(self):
        #set geometry, window appearance
        self.setGeometry(200,250,1440,720)
        self.aspectRatio = self.size().height() / self.size().width()
        self.setBaseSize(self.size())
        self.setSizeIncrement(1, self.aspectRatio)
        self.setMinimumSize(self.size())
        self.setWindowTitle("Pyfab")
        self.setWindowIcon(QtGui.QIcon('icon/pyqtlogo.png'))
        
        #define widgets
        self.window = QtGui.QWidget()
        self.layout = QtGui.QHBoxLayout()
        self.tabs = QtGui.QTabWidget()
        #add tabs
        self.tabs.addTab(self.cgh, QtCore.QString('Calibration'))
        #create layout
        self.layout.addWidget(self.fabscreen)
        self.layout.addWidget(self.tabs)
        #set proportionality of fabscreen vs tabs
        self.layout.setStretch(0,2)
        self.layout.setStretch(1,1)
        #implement layout
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

        #QActions
        exit = QtGui.QAction('&Exit', self)        
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        exit.triggered.connect(self.close)
        saveCalibration = QtGui.QAction('&Save', self)
        saveCalibration.setShortcut('Ctrl+S')
        saveCalibration.setStatusTip('Save calibration settings')
        saveCalibration.triggered.connect(self.cgh.saveData)
        restoreCalibration = QtGui.QAction('&Restore', self)
        restoreCalibration.setShortcut('Ctrl+R')
        restoreCalibration.setStatusTip('Restore calibration settings')
        restoreCalibration.triggered.connect(self.cgh.restoreData)
        
        #Add QActions to menubar
        mainMenu = self.menuBar()
        file = mainMenu.addMenu('File')
        file.addAction(exit)
        file.addAction(saveCalibration)
        file.addAction(restoreCalibration)
        
        self.show()
         
    def closeEvent(self, event):
        result = QtGui.QMessageBox.question(self,
                      "Confirm quit",
                      "Are you sure you want to quit?",
                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:
            if self.cgh.constantsSaved == False:
                savePrompt = QtGui.QMessageBox.question(self,
                      "Save calibration constants",
                      "Do you want to save your calibration?",
                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if savePrompt == QtGui.QMessageBox.Yes:
                    self.cgh.saveData()
            event.accept()
            self.sigClosed.emit()
        else:
            event.ignore()
            
        
if __name__ == '__main__':
    main()   

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = pyfabMainWindow()
    sys.exit(app.exec_())