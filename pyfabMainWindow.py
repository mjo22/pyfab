from pyqtgraph.Qt import QtGui, QtCore
from traps import QTrappingPattern
from QFabGraphicsView import QFabGraphicsView
from QSLM import QSLM
from CGH import CGH
from QCGH import QCGH
import sys
        
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
        '''
        To set up GUI: create a QHBoxLayout object and add to it a QTabWidget and Fabscreen. Change dimensions to make this work. Then make 
        the BoxLayout the central widget of the QMainWindow. Add calibration as a tab. Then have a dot menu where you have the option to 
        calibrate as sliders or as the QTableView.
        '''
        #set geometry, window appearance
        self.setGeometry(640,480,1440,720)
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
        
        self.layout.setStretch(0,1)
        self.layout.setStretch(1,1)
        
        #implement layout
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)
        
        
        
        #QActions
        exit = QtGui.QAction('&Exit', self)        
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        exit.triggered.connect(self.close)
        '''
        cal = QtGui.QAction('&Calibrate',self)
        cal.setShortcut('Ctrl+C')
        cal.triggered.connect(self.cgh.show)
        mainMenu.addAction(cal)
        '''
        #Add QActions to menubar
        mainMenu = self.menuBar()
        file = mainMenu.addMenu('File')
        file.addAction(exit)
        
        self.show()
         
    def closeEvent(self, event):
        result = QtGui.QMessageBox.question(self,
                      "Confirm quit",
                      "Are you sure you want to quit?",
                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:
            event.accept()
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