from PyQt4 import QtGui, QtCore
from CGH import CGH
import sys

class QCGH(QtGui.QTableWidget, CGH):
    def __init__(self):
        super(QCGH, self).__init__()
        #appearance of QCGH
        self.setGeometry(50,50,550,150)
        self.setWindowTitle("Calibration")
        self.setColumnCount(5)
        self.setRowCount(3)
        #initialize constants
        self.theta = 0.
        self.alpha = 0.
        self.qpp = 0.
        self.rc = QtGui.QVector3D(0.,0.,0.)
        self.rs = QtGui.QVector3D(0.,0.,0.)
        #fill out table
        self.setVerticalHeaderItem(0, QtGui.QTableWidgetItem(QtCore.QString("xc")))
        self.setVerticalHeaderItem(1, QtGui.QTableWidgetItem(QtCore.QString("yc")))
        self.setVerticalHeaderItem(2, QtGui.QTableWidgetItem(QtCore.QString("zc")))
        prop = [QtGui.QTableWidgetItem(QtCore.QString('qpp')),QtGui.QTableWidgetItem(QtCore.QString('alpha')),QtGui.QTableWidgetItem(QtCore.QString('theta')),QtGui.QTableWidgetItem(QtCore.QString('rc')),QtGui.QTableWidgetItem(QtCore.QString('rs'))]
        for i in range(len(prop)):
            self.setHorizontalHeaderItem(i,prop[i])
        self.updateTable()
        #link table to cgh
        
        #link cgh to table
    def updateTable(self):
        values = range(5)
        values[0] = self.qpp
        values[1] = self.alpha
        values[2] = self.theta
        values[3] = self.rc
        values[4] = self.rs
        for i in range(5):
            if type(values[i]) is not float:
                self.setItem(0,i,QtGui.QTableWidgetItem(QtCore.QString(str(values[i].x()))))
                self.setItem(1,i,QtGui.QTableWidgetItem(QtCore.QString(str(values[i].y()))))
                self.setItem(2,i,QtGui.QTableWidgetItem(QtCore.QString(str(values[i].z()))))
            else:
                values[i] = QtGui.QTableWidgetItem(QtCore.QString(str(values[i])))
                self.setItem(0,i,values[i])
                
    
    @CGH.theta.getter
    def theta(self):
        return self._theta
    
    @theta.setter
    def theta(self, value):
        self._theta = value
        
    @CGH.qpp.getter
    def qpp(self):
        return self._qpp
    
    @qpp.setter
    def qpp(self, value):
        self._qpp = value
        
    @CGH.alpha.getter
    def alpha(self):
        return self._alpha
    
    @alpha.setter
    def alpha(self, value):
        self._alpha = value
        
    @CGH.rs.getter
    def rs(self):
        return self._rs
    
    @rs.setter
    def rs(self, value):
        self._rs = value
        
    @CGH.rc.getter
    def rc(self):
        return self._rc
    
    @rc.setter
    def rc(self, value):
        self._rc = value
        
    def formatAsQStr(self, const):
        pass
    
    def QStrToQVect(self):
        pass
    
    def getX(self, vect):
        pass
    
    def getY(self, vect):
        pass
    
    def getZ(self, vect):
        pass
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    cgh = QCGH()
    sys.exit(app.exec_())