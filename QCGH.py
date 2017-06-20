from PyQt4 import QtGui
from CGH import CGH
import sys

class QCGH(QtGui.QTableWidget, CGH):
    def __init__(self):
        super(QCGH, self).__init__()
        self.setGeometry(50,50,250,250)
        self.setWindowTitle("Calibration")
        self.setColumnCount(10)
        self.setRowCount(6)
        #self.update
  

    '''    
    def update():
        pass
    '''
        
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    cgh = QCGH()
    sys.exit(app.exec_())