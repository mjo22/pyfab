from PyQt4 import QtGui, QtCore
from CGH import CGH
import sys

class QCGH(QtGui.QTableWidget, CGH):
    def __init__(self):
        super(QCGH, self).__init__()
        self.setUpGui()
        self.initializeConstants()
        self.cellChanged.connect(self.updateConstant)
        
    def initializeConstants(self):
        self.theta = 0.
        self.alpha = 0.
        self.qpp = 0.
        self.rc = QtGui.QVector3D(0.,0.,0.)
        self.rs = QtGui.QVector3D(0.,0.,0.)
        
    def setUpGui(self):
        #appearance of QCGH
        self.setGeometry(50,50,50,310)
        self.setWindowTitle("Calibration")
        self.setColumnCount(1)
        self.setRowCount(9)
        #define correspondence of a label to its row
        self.labelToRow = {'qpp':0,'alpha':1,'theta':2,'rc xc':3, 'rc yc':4,'rc zc':5,'rs xc':6,'rs yc':7,'rs zc':8}
        #fill headers
        labels = ('qpp','alpha','theta','rc xc', 'rc yc','rc zc','rs xc','rs yc','rs zc')
        self.setHorizontalHeaderItem(0,QtGui.QTableWidgetItem(QtCore.QString('')))
        for i in range(len(self.labelToRow.keys())):
            self.setVerticalHeaderItem(i,QtGui.QTableWidgetItem(QtCore.QString(labels[i])))
            
    def updateConstant(self):
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
            if row == self.labelToRow['qpp']:
                self.qpp = inputFl
            elif row == self.labelToRow['alpha']:
                self.alpha = inputFl
            elif row == self.labelToRow['theta']:
                self.theta = inputFl
            elif row == self.labelToRow['rc xc']:
                self.setX(self.rc,3,inputFl)
            elif row == self.labelToRow['rc yc']:
                self.setY(self.rc,4,inputFl)
            elif row == self.labelToRow['rc zc']:
                self.setZ(self.rc,5,inputFl)
            elif row == self.labelToRow['rs xc']:
                self.setX(self.rs,6,inputFl)
            elif row == self.labelToRow['rs yc']:
                self.setY(self.rs,7,inputFl)
            elif row == self.labelToRow['rs zc']:
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
        vector.setZ(value)
        self.setWidgetValue(row,vector.z())
           
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