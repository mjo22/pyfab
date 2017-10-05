from pyqtgraph.Qt import QtGui, QtCore
from traps import QTrappingPattern
from QFabGraphicsView import QFabGraphicsView
from QSLM import QSLM
from CGH import CGH
from QCGH import QCGH
import sys
import json

"""QPyfab: GUI for holographic optical trapping"""
        
class QPyfab(QtGui.QMainWindow):
    
    sigClosed = QtCore.pyqtSignal()   #Signal that will emited after closing QPyfab. Is handled by pyfab class    

    '''
    Initalizes fabscreen and all gui functionality
    '''
    def __init__(self):
        super(QPyfab, self).__init__()
        self.initFab()
        self.initGui()

    '''
    Initialize fabscreen and pass it to the trapping pattern. Then set CGH pipeline and give it an slm.
    '''
    def initFab(self):
        self.fabscreen = QFabGraphicsView(size=(640,480), gray=True, mirrored=False)
        self.pattern = QTrappingPattern(self.fabscreen)
        self.slm = QSLM()
        self.pattern.pipeline = QCGH(slm=self.slm)
        self.show()
    '''
    Initializes all QMainWindow GUI functionality. See inline comments for specifics.
    '''
    def initGui(self):
        #set geometry, window appearance
        desktop = QtGui.QDesktopWidget()
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
        
        #define widgets
        self.window = QtGui.QWidget()
        self.layout = QtGui.QHBoxLayout()
        self.tabs = QtGui.QTabWidget()
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
        exit = QtGui.QAction('&Exit', self)        
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        exit.triggered.connect(self.close)
        saveCalibration = QtGui.QAction('&Save', self)
        saveCalibration.setShortcut('Ctrl+S')
        saveCalibration.setStatusTip('Save calibration settings')
        saveCalibration.triggered.connect(self.pattern.pipeline.saveData)
        restoreCalibration = QtGui.QAction('&Restore', self)
        restoreCalibration.setShortcut('Ctrl+R')
        restoreCalibration.setStatusTip('Restore calibration settings')
        restoreCalibration.triggered.connect(self.pattern.pipeline.restoreData)
        #Add QActions to menubar
        toolMenu = QtGui.QMenuBar()
        toolMenu.setNativeMenuBar(False)
        self.setMenuBar(toolMenu)
        file = toolMenu.addMenu('File')
        file.addAction(exit)
        file.addAction(saveCalibration)
        file.addAction(restoreCalibration)
        self.show()

    '''
    Close event triggered by exiting QPyfab. Prompts the user to make sure they meant to exit, and asks if they want to save calibration settings if they have not done so.
    '''
    def closeEvent(self, event):
        result = QtGui.QMessageBox.question(self,
                      "Confirm quit",
                      "Are you sure you want to quit?",
                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:
            if self.pattern.pipeline.constantsSaved == False:
                savePrompt = QtGui.QMessageBox.question(self,
                      "Save",
                      "Do you want to save your calibration settings?",
                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if savePrompt == QtGui.QMessageBox.Yes:
                    self.pattern.pipeline.saveData()
            event.accept()
            self.sigClosed.emit()
        else:
            event.ignore()
            
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = pyfabMainWindow()
    sys.exit(app.exec_())
