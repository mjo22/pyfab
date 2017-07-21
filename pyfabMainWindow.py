from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
from traps import QTrappingPattern
from QFabGraphicsView import QFabGraphicsView
from QSLM import QSLM
from CGH import CGH
from QCGH import QCGH
import sys
import json
        
class pyfabMainWindow(QtWidgets.QMainWindow):
    
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
        self.pattern.pipeline = QCGH(self.slm)
        self.show()
        
    def setUpGui(self):
        #set geometry, window appearance
        desktop = QtWidgets.QDesktopWidget()
        width = desktop.screenGeometry().width()
        minWidth = int(width / 1.5)
        maxWidth = width
        aspectRatio = 2
        self.setGeometry(minWidth/4, minWidth/5, minWidth, minWidth/aspectRatio)
        self.setBaseSize(self.size())
        self.setSizeIncrement(1, aspectRatio)
        self.setMinimumSize(QtCore.QSize(minWidth, minWidth/aspectRatio))
        self.setMaximumSize(QtCore.QSize(maxWidth, maxWidth/aspectRatio))
        self.setWindowTitle("Pyfab")
        self.setWindowIcon(QtGui.QIcon('icon/pyqtlogo.png'))
        
        #define widgets
        self.window = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout()
        self.tabs = QtWidgets.QTabWidget()
        #add tabs
        self.tabs.addTab(self.pattern.pipeline, 'Calibration')
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
        exit = QtWidgets.QAction('&Exit', self)        
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        exit.triggered.connect(self.close)
        saveCalibration = QtWidgets.QAction('&Save', self)
        saveCalibration.setShortcut('Ctrl+S')
        saveCalibration.setStatusTip('Save calibration settings')
        saveCalibration.triggered.connect(self.pattern.pipeline.saveData)
        restoreCalibration = QtWidgets.QAction('&Restore', self)
        restoreCalibration.setShortcut('Ctrl+R')
        restoreCalibration.setStatusTip('Restore calibration settings')
        restoreCalibration.triggered.connect(self.pattern.pipeline.restoreData)
        #Add QActions to menubar
        mainMenu = self.menuBar()
        file = mainMenu.addMenu('File')
        file.addAction(exit)
        file.addAction(saveCalibration)
        file.addAction(restoreCalibration)
        
        self.show()
         
    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self,
                      "Confirm quit",
                      "Are you sure you want to quit?",
                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            if self.pattern.pipeline.constantsSaved == False:
                savePrompt = QtWidgets.QMessageBox.question(self,
                      "Save",
                      "Do you want to save your calibration settings?",
                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if savePrompt == QtWidgets.QMessageBox.Yes:
                    self.pattern.pipeline.saveData()
            event.accept()
            self.sigClosed.emit()
        else:
            event.ignore()
            
        
if __name__ == '__main__':
    main()   

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = pyfabMainWindow()
    sys.exit(app.exec_())