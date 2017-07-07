from PyQt4 import QtGui, QtCore
from CGH import CGH
import sys

class QCGH(QtGui.QTableWidget, CGH):
    
    #bounds
    max_dict = {'qpp':10,'alpha':360,'theta':360,'rc xc':10, 'rc yc':10,'rc zc':10,'rs xc':10,'rs yc':10,'rs zc':10}
    min_dict = {'qpp':0,'alpha':0,'theta':0,'rc xc':0, 'rc yc':0,'rc zc':0,'rs xc':0,'rs yc':0,'rs zc':0}
    #define correspondence of a label to its row
    labelToRow = {'qpp':0,'alpha':1,'theta':2,'rc xc':3, 'rc yc':4,'rc zc':5,'rs xc':6,'rs yc':7,'rs zc':8}
    
    def __init__(self):
        super(QCGH, self).__init__()
        self.setUpGui()
        self.cellChanged.connect(self.updateConstant)
        
    def initializeConstants(self):
        self.theta = 0.
        self.alpha = 0.
        self.qpp = 0.
        self.rc = QtGui.QVector3D(0.,0.,0.)
        self.rs = QtGui.QVector3D(0.,0.,0.)
        
    def setUpGui(self):
        #appearance of QCGH
        self.setGeometry(200,200,50,300)
        self.aspectRatio = self.size().height() / self.size().width()
        self.setBaseSize(self.size())
        self.setSizeIncrement(1, self.aspectRatio)
        self.setMinimumSize(self.size())
        self.setWindowTitle("Calibration")
        self.setColumnCount(1)
        self.setRowCount(9)
        #fill headers
        labels = ('qpp','alpha','theta','rc xc', 'rc yc','rc zc','rs xc','rs yc','rs zc')
        self.setHorizontalHeaderItem(0,QtGui.QTableWidgetItem(QtCore.QString('')))
        for i in range(len(self.labelToRow.keys())):
            self.setVerticalHeaderItem(i,QtGui.QTableWidgetItem(QtCore.QString(labels[i])))
        #initialize constants after setting up GUI so they're put into table
        self.initializeConstants()
    '''    
    try this: https://stackoverflow.com/questions/452333/how-to-maintain-widgets-aspect-ratio-in-qt
    def resizeEvent(self,event):
        if self.size().height() / self.size().width() != self.h_to_w:
            print 'nay!'
            self.blockSignals(True)
            w = event.oldSize().width() + 1
            h = event.oldSize().height() + 6
            self.setGeometry(self.pos().x(), self.pos().y(), w, h)
            self.blockSignals(False)
        else:
            print 'perf!'
    '''
            
            
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
                self.setX(self.rc,row,inputFl,'rc xc')
            elif row == self.labelToRow['rc yc']:
                self.setY(self.rc,row,inputFl,'rc yc')
            elif row == self.labelToRow['rc zc']:
                self.setZ(self.rc,row,inputFl,'rc zc')
            elif row == self.labelToRow['rs xc']:
                self.setX(self.rs,row,inputFl,'rs xc')
            elif row == self.labelToRow['rs yc']:
                self.setY(self.rs,row,inputFl,'rs yc')
            elif row == self.labelToRow['rs zc']:
                self.setZ(self.rs,row,inputFl,'rs zc')
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
        
    def setX(self,vector,row,value,key):
        '''
        Used to just change the x value of a QVector3D. Call the setter to change all three 
        components at once.
        '''
        value = self.clamp(value, self.min_dict[key], self.max_dict[key])
        vector.setX(value)
        self.setWidgetValue(row,vector.x())
    def setY(self,vector,row,value,key):
        '''
        Used to just change the x value of a QVector3D. Call the setter to change all three 
        components at once.
        '''
        value = self.clamp(value, self.min_dict[key], self.max_dict[key])
        vector.setY(value)
        self.setWidgetValue(row,vector.y())
    def setZ(self,vector,row,value,key):
        '''
        Used to just change the x value of a QVector3D. Call the setter to change all three 
        components at once.
        '''
        value = self.clamp(value, self.min_dict[key], self.max_dict[key])
        vector.setZ(value)
        self.setWidgetValue(row,vector.z())
        
    def clamp(self, n, mini, maxi):
        return max(min(n, maxi), mini)    
           
    @CGH.qpp.getter
    def qpp(self):
        return self._qpp
    
    @qpp.setter
    def qpp(self, value):
        value = self.clamp(value, self.min_dict['qpp'], self.max_dict['qpp'])
        self._qpp = value
        self.setWidgetValue(self.labelToRow['qpp'],value)
        
    @CGH.alpha.getter
    def alpha(self):
        return self._alpha
    
    @alpha.setter
    def alpha(self, value):
        value = self.clamp(value, self.min_dict['alpha'], self.max_dict['alpha'])
        self._alpha = value
        self.setWidgetValue(self.labelToRow['alpha'],value)
        
    @CGH.theta.getter
    def theta(self):
        return self._theta
    
    @theta.setter
    def theta(self, value):
        value = self.clamp(value, self.min_dict['theta'], self.max_dict['theta'])
        self._theta = value
        self.setWidgetValue(self.labelToRow['theta'],value)
    
    @CGH.rc.getter
    def rc(self):
        return self._rc
    
    @rc.setter
    def rc(self, value):
        value.setX(self.clamp(value, self.min_dict['rc xc'], self.max_dict['rc xc']))
        value.setY(self.clamp(value, self.min_dict['rc yc'], self.max_dict['rc yc']))
        value.setZ(self.clamp(value, self.min_dict['rc zc'], self.max_dict['rc zc']))
        self._rc = value 
        self.setWidgetValue(self.labelToRow['rc xc'],self._rc.x())
        self.setWidgetValue(self.labelToRow['rc yc'],self._rc.y())
        self.setWidgetValue(self.labelToRow['rc zc'],self._rc.z())
    
    @CGH.rs.getter
    def rs(self):
        return self._rs
    
    @rs.setter
    def rs(self, value):
        value.setX(self.clamp(value, self.min_dict['rs xc'], self.max_dict['rs xc']))
        value.setY(self.clamp(value, self.min_dict['rs yc'], self.max_dict['rs yc']))
        value.setZ(self.clamp(value, self.min_dict['rs zc'], self.max_dict['rs zc']))
        self._rs = value
        self.setWidgetValue(self.labelToRow['rs xc'],self._rs.x())
        self.setWidgetValue(self.labelToRow['rs yc'],self._rs.y())
        self.setWidgetValue(self.labelToRow['rs zc'],self._rs.z())
             
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    cgh = QCGH()
    sys.exit(app.exec_())