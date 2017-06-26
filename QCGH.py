from PyQt4 import QtGui, QtCore
from CGH import CGH
import sys

class QCGH(QtGui.QTableWidget, CGH):
    def __init__(self):
        super(QCGH, self).__init__()
        #appearance of QCGH
        self.setGeometry(50,50,50,310)
        self.setWindowTitle("Calibration")
        self.setColumnCount(1)
        self.setRowCount(9)
        #fill labels
        labels = [QtGui.QTableWidgetItem(QtCore.QString('qpp')),QtGui.QTableWidgetItem(QtCore.QString('alpha')),QtGui.QTableWidgetItem(QtCore.QString('theta')),QtGui.QTableWidgetItem(QtCore.QString('rc xc')),QtGui.QTableWidgetItem(QtCore.QString('rc yc')),QtGui.QTableWidgetItem(QtCore.QString('rc zc')),QtGui.QTableWidgetItem(QtCore.QString('rs xc')), QtGui.QTableWidgetItem(QtCore.QString('rs yc')), QtGui.QTableWidgetItem(QtCore.QString('rs zc'))]
        for i in range(len(labels)):
            self.setVerticalHeaderItem(i,labels[i])
        self.setHorizontalHeaderItem(0,QtGui.QTableWidgetItem(QtCore.QString('')))
        #initialize constants
        self.theta = 0.
        self.alpha = 0.
        self.qpp = 0.
        self.rc = QtGui.QVector3D(0.,0.,0.)
        self.rs = QtGui.QVector3D(0.,0.,0.)
        #catch signal if user changes signal
        self.cellChanged.connect(self.updateCalConstant)
            
    def updateCalConstant(self):
        '''
        Call when user connects to cellChanged signal called by pyfabMainWindow
        
        To improve: 
        1) Eliminate row dependence. The connection to each constant depends on the row 
        that the cell is in
        2) Fix hard coding of using conditionals for each row. The complication lies 
        with the setters--if you store them in a list/dictionary/tuple you can't set them 
        to a new value by accessing the item and you can't call it as a function from the 
        list/dictionary/tuple
        '''
        #idea: dict linking getters and widget items? could easily b done
        #To do: 
        #1) bound each value
        #2) make code prettier
        
        row = self.currentRow()
        try:
            inputFl = float(str(self.currentItem().text()))
        except:
            inputFl = 0.     
        try:
            if row == 0:
                self.qpp = inputFl
            elif row == 1:
                self.alpha = inputFl
            elif row == 2:
                self.theta = inputFl
            elif row == 3:
                self.setX(self.rc,3,inputFl)
            elif row == 4:
                self.setY(self.rc,4,inputFl)
            elif row == 5:
                self.setZ(self.rc,5,inputFl)
            elif row == 6:
                self.setX(self.rs,6,inputFl)
            elif row == 7:
                self.setY(self.rs,7,inputFl)
            elif row == 8:
                self.setZ(self.rs,8,inputFl)
        except Exception, e:
            print e
    
    def floatToWidgetItem(self, fl):
        fl = '{0:.2f}'.format(fl)
        return QtGui.QTableWidgetItem(QtCore.QString(fl))
    
    def setWidgetValue(self,row,value):
        '''
        When setting an item to the table, the cellChanged signal must be blocked or else 
        the system will catch it and enter an infinite loop
        '''
        self.blockSignals(True)
        self.setItem(row,0,self.floatToWidgetItem(value))
        self.blockSignals(False)
        
    def setX(self,vector,row,value):
        '''
        Used to just change the x value of a QVector3D. Call the setter to change all three 
        components at once.
        '''
        vector.setX(value)
        self.setWidgetValue(row,vector.x())
    def setY(self,vector,row,value):
        '''
        Used to just change the x value of a QVector3D. Call the setter to change all three 
        components at once.
        '''
        vector.setY(value)
        self.setWidgetValue(row,vector.y())
    def setZ(self,vector,row,value):
        '''
        Used to just change the x value of a QVector3D. Call the setter to change all three 
        components at once.
        '''
        self.setWidgetValue(row,vector.z())
        print vector
           
    @CGH.qpp.getter
    def qpp(self):
        return self._qpp
    
    @qpp.setter
    def qpp(self, value):
        self._qpp = value
        self.setWidgetValue(0,value)
        
    @CGH.alpha.getter
    def alpha(self):
        return self._alpha
    
    @alpha.setter
    def alpha(self, value):
        self._alpha = value
        self.setWidgetValue(1,value)
        
    @CGH.theta.getter
    def theta(self):
        return self._theta
    
    @theta.setter
    def theta(self, value):
        self._theta = value
        self.setWidgetValue(2,value)
    
    @CGH.rc.getter
    def rc(self):
        return self._rc
    
    @rc.setter
    def rc(self, value):
        self._rc = value 
        self.setWidgetValue(3,self._rc.x())
        self.setWidgetValue(4,self._rc.y())
        self.setWidgetValue(5,self._rc.z())
    
    @CGH.rs.getter
    def rs(self):
        return self._rs
    
    @rs.setter
    def rs(self, value):
        self._rs = value
        self.setWidgetValue(6,self._rs.x())
        self.setWidgetValue(7,self._rs.y())
        self.setWidgetValue(8,self._rs.z())
             
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    cgh = QCGH()
    sys.exit(app.exec_())