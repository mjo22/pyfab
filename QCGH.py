from PyQt4 import QtGui, QtCore
from CGH import CGH
import sys
import json

class QCGH(QtGui.QTableWidget, CGH):
    
    '''
    A GUI to set calibration constants. 
    To set:
        From the program- 
            Use the table in the "Calibration" tab.
        From the terminal-
            For values simply use the setters of the constant. 
            For vectors, either use setX, setY, setZ as written in this QCGH class, or call a setter and set equal to a QtGui.QVector3D() 
            object.
    '''
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
        '''
        Loads last saved data and initializes constants as such
        '''
        self.lastSaved = self.getData()
        self.theta = self.lastSaved['theta']
        self.alpha = self.lastSaved['alpha']
        self.qpp = self.lastSaved['qpp']
        self.rc = QtGui.QVector3D(self.lastSaved['rc xc'],self.lastSaved['rc yc'],self.lastSaved['rc zc'])
        self.rs = QtGui.QVector3D(self.lastSaved['rs xc'],self.lastSaved['rs yc'],self.lastSaved['rs zc'])
        self.constantsSaved = True
        
    def saveData(self):
        self.lastSaved = self.getData()
        data = {'qpp': self.qpp, 'alpha': self.alpha, 'theta': self.theta, 'rc xc': self.rc.x(), 'rc yc': self.rc.y(), 'rc zc': self.rc.z(), 'rs xc': self.rs.x(), 'rs yc': self.rs.y(), 'rs zc': self.rs.z()}
        s = json.dumps(data)
        with open("json/calibration.txt", "w") as f:
            f.write(s)
        self.constantsSaved = True
        
    def restoreData(self):
        restore = QtGui.QMessageBox.question(self,
                      "Restore Calibration Settings",
                      "Are you sure you want to restore? Current settings will be lost.",
                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if restore == QtGui.QMessageBox.Yes:
            s = json.dumps(self.lastSaved)
            with open("json/calibration.txt", "w") as f:
                f.write(s)
            self.constantsSaved = True
            self.initializeConstants()
    
    def getData(self):
        f = open("json/calibration.txt", "r")
        s = f.read()
        data = json.loads(s)
        return data
        
    def setUpGui(self):
        #appearance of QCGH
        self.setGeometry(0,0,50,300)
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
                        
    def updateConstant(self):
        '''
        Call when user connects to cellChanged signal called by pyfabMainWindow
        '''
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
                self.setX(self.rc,inputFl,'rc xc')
            elif row == self.labelToRow['rc yc']:
                self.setY(self.rc,inputFl,'rc yc')
            elif row == self.labelToRow['rc zc']:
                self.setZ(self.rc,inputFl,'rc zc')
            elif row == self.labelToRow['rs xc']:
                self.setX(self.rs,inputFl,'rs xc')
            elif row == self.labelToRow['rs yc']:
                self.setY(self.rs,inputFl,'rs yc')
            elif row == self.labelToRow['rs zc']:
                self.setZ(self.rs,inputFl,'rs zc')
        except Exception, e:
            print e
    
    def floatToWidgetItem(self, fl):
        fl = '{0:.2f}'.format(fl)
        return QtGui.QTableWidgetItem(QtCore.QString(fl))
    
    def setWidgetValue(self,key,value):
        '''
        When setting an item to the table, the cellChanged signal must be blocked or else 
        the system will catch it and enter an infinite loop
        '''
        self.blockSignals(True)
        self.setItem(self.labelToRow[key],0,self.floatToWidgetItem(value))
        self.blockSignals(False)
        self.constantsSaved = False
        
    def setX(self,vector,value,key):
        '''
        Used to just change the x value of a QVector3D. Call the setter to change all three 
        components at once.
        '''
        value = self.clamp(value, self.min_dict[key], self.max_dict[key])
        vector.setX(value)
        self.setWidgetValue(key,vector.x())
        
    def setY(self,vector,value,key):
        '''
        Used to just change the x value of a QVector3D. Call the setter to change all three 
        components at once.
        '''
        value = self.clamp(value, self.min_dict[key], self.max_dict[key])
        vector.setY(value)
        self.setWidgetValue(key,vector.y())
        
    def setZ(self,vector,value,key):
        '''
        Used to just change the x value of a QVector3D. Call the setter to change all three 
        components at once.
        '''
        value = self.clamp(value, self.min_dict[key], self.max_dict[key])
        vector.setZ(value)
        self.setWidgetValue(key,vector.z())
        
    def clamp(self, n, mini, maxi):
        return max(min(n, maxi), mini)    
           
    @CGH.qpp.getter
    def qpp(self):
        return self._qpp
    
    @qpp.setter
    def qpp(self, value):
        value = self.clamp(value, self.min_dict['qpp'], self.max_dict['qpp'])
        self._qpp = value
        self.setWidgetValue('qpp',value)
        
    @CGH.alpha.getter
    def alpha(self):
        return self._alpha
    
    @alpha.setter
    def alpha(self, value):
        value = self.clamp(value, self.min_dict['alpha'], self.max_dict['alpha'])
        self._alpha = value
        self.setWidgetValue('alpha',value)
        
    @CGH.theta.getter
    def theta(self):
        return self._theta
    
    @theta.setter
    def theta(self, value):
        value = self.clamp(value, self.min_dict['theta'], self.max_dict['theta'])
        self._theta = value
        self.setWidgetValue('theta',value)
    
    @CGH.rc.getter
    def rc(self):
        return self._rc
    
    @rc.setter
    def rc(self, vector):
        self.setX(vector, self.clamp(vector.x(), self.min_dict['rc xc'], self.max_dict['rc xc']), 'rc xc')
        self.setY(vector, self.clamp(vector.y(), self.min_dict['rc yc'], self.max_dict['rc yc']), 'rc yc')
        self.setZ(vector, self.clamp(vector.z(), self.min_dict['rc zc'], self.max_dict['rc zc']), 'rc zc')
        self._rc = vector
        self.constantsSaved = False
    
    @CGH.rs.getter
    def rs(self):
        return self._rs
    
    @rs.setter
    def rs(self, vector):
        self.setX(vector, self.clamp(vector.x(), self.min_dict['rs xc'], self.max_dict['rs xc']), 'rs xc')
        self.setY(vector, self.clamp(vector.y(), self.min_dict['rs yc'], self.max_dict['rs yc']), 'rs yc')
        self.setZ(vector, self.clamp(vector.z(), self.min_dict['rs zc'], self.max_dict['rs zc']), 'rs zc')
        self._rs = vector
        self.constantsSaved = False
             
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    cgh = QCGH()
    sys.exit(app.exec_())