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
	self.cgh = QCGH(slm=self.slm)
        self.pattern.pipeline = self.cgh
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
	#self.tabs.addTab( , "Fabcorder")
	self.tabs.addTab(self.cgh, "CGH")   
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
	#for File
        exit = QtGui.QAction('&Exit', self)        
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        exit.triggered.connect(self.close)
	#for Calibration
        saveCalibration = QtGui.QAction('&Save', self)
        saveCalibration.setShortcut('Ctrl+S')
        saveCalibration.setStatusTip('Save calibration settings')
        saveCalibration.triggered.connect(self.cgh.saveData)
        restoreCalibration = QtGui.QAction('&Restore', self)
        restoreCalibration.setShortcut('Ctrl+R')
        restoreCalibration.setStatusTip('Restore calibration settings')
        restoreCalibration.triggered.connect(self.cgh.restoreData)
	calibrate = QtGui.QAction('&Calibrate', self)
        calibrate.setShortcut('Ctrl+K')
	calibrate.setStatusTip('Calibrate pyfab')
        calibrate.triggered.connect(self.cgh.show)
	#for Traps

        #Add QActions to menubar
        toolbar = QtGui.QMenuBar()
        toolbar.setNativeMenuBar(False)
        self.setMenuBar(toolbar)
        fileMenu = toolbar.addMenu('File')
        fileMenu.addAction(exit)
	calMenu = toolbar.addMenu('Calibration')
	calMenu.addAction(calibrate)
	calMenu.addAction(saveCalibration)
        calMenu.addAction(restoreCalibration)
	trap = toolbar.addMenu('Traps')
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

#class QFabCorder
            
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    qfab = QPyfab()
    sys.exit(app.exec_())
