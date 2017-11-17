from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtGui import QVector3D
from QSLM import QSLM
from CGH import CGH
import sys
import json
import numpy as np

class QCGH(QtGui.QTableWidget, CGH):
    
    '''
    A GUI to set calibration constants. 
    To set:
        From the program- 
            Use the table in the "Calibration" tab.
        From the terminal-
            For values, call setter and set equal to float. 
            For vectors, call setter and set equal to a QVector3D(x, y, z).
    '''
    #bounds
    max_dict = {'qpp':10,'alpha':360,'theta':360,'rc xc':10, 'rc yc':10,'rc zc':10,'rs xc':10,'rs yc':10,'rs zc':10}
    min_dict = {'qpp':0,'alpha':0,'theta':0,'rc xc':0, 'rc yc':0,'rc zc':0,'rs xc':0,'rs yc':0,'rs zc':0}
    #define correspondence of a label to its row
    labelToRow = {'qpp':0,'alpha':1,'theta':2,'rc xc':3, 'rc yc':4,'rc zc':5,'rs xc':6,'rs yc':7,'rs zc':8}
    
    def __init__(self, parent=None, slm=None):
        QtGui.QTableWidget.__init__(self, parent)
        CGH.__init__(self, slm=slm)
        self.setUpGui()
        self.cellChanged.connect(self.updateConstant)
        
    def setUpGui(self):
        #appearance of QCGH
	desktop = QtGui.QDesktopWidget()
        w = desktop.screenGeometry().width()
	h = desktop.screenGeometry().height()
        self.setGeometry(int(w/1.5),h/2,w/20,h/4)
        self.setColumnCount(1)
        self.setRowCount(9)
        #fill headers
        labels = ('qpp','alpha','theta','rc xc', 'rc yc','rc zc','rs xc','rs yc','rs zc')
        self.setHorizontalHeaderItem(0,QtGui.QTableWidgetItem(''))
        for i in range(len(self.labelToRow.keys())):
            self.setVerticalHeaderItem(i,QtGui.QTableWidgetItem(labels[i]))
        #initialize constants after setting up GUI so they're put into table
        self.initializeConstants()
        
    def initializeConstants(self):
        '''
        Loads last saved data and initializes constants as such
        '''
        self.lastSaved = self.getData()
        self.theta = self.lastSaved['theta']
        self.alpha = self.lastSaved['alpha']
        self.qpp = self.lastSaved['qpp']
        self.rc = QVector3D(self.lastSaved['rc xc'],self.lastSaved['rc yc'],self.lastSaved['rc zc'])
        self.rs = QVector3D(self.lastSaved['rs xc'],self.lastSaved['rs yc'],self.lastSaved['rs zc'])
        self.constantsSaved = True
        
    def saveData(self):
        self.lastSaved = self.getData()
        data = {'qpp': self.qpp, 'alpha': self.alpha, 'theta': self.theta, 'rc xc': self.rc.x(), 'rc yc': self.rc.y(), 'rc zc': self.rc.z(), 'rs xc': self.rs.x(), 'rs yc': self.rs.y(), 'rs zc': self.rs.z()}
        s = json.dumps(data)
        with open(".json/calibration.txt", "w") as f:
            f.write(s)
        self.constantsSaved = True
        
    def restoreData(self):
        restore = QtGui.QMessageBox.question(self,
                      "Restore Calibration Settings",
                      "Are you sure you want to restore? Current settings will be lost.",
                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if restore == QtGui.QMessageBox.Yes:
            s = json.dumps(self.lastSaved)
            with open(".json/calibration.txt", "w") as f:
                f.write(s)
            self.constantsSaved = True
            self.initializeConstants()
    
    def getData(self):
        f = open(".json/calibration.txt", "r")
        s = f.read()
        data = json.loads(s)
        return data
                        
    def updateConstant(self):
        '''
        Call when user connects to cellChanged signal called by QPyfab
        '''
        row = self.currentRow()
        try:
            inputFl = float(str(self.currentItem().text()))
        except:
            inputFl = 0.     
        if row == self.labelToRow['qpp']:
            self.qpp = inputFl
        elif row == self.labelToRow['alpha']:
            self.alpha = inputFl
        elif row == self.labelToRow['theta']:
            self.theta = inputFl
        elif row == self.labelToRow['rc xc']:
            self.rc = QVector3D(inputFl, self.rc.y(), self.rc.z())
        elif row == self.labelToRow['rc yc']:
            self.rc = QVector3D(self.rc.x(), inputFl, self.rc.z())
        elif row == self.labelToRow['rc zc']:
            self.rc = QVector3D(self.rc.x(), self.rc.y(), inputFl)
        elif row == self.labelToRow['rs xc']:
            self.rs = QVector3D(inputFl, self.rs.y(), self.rs.z())
        elif row == self.labelToRow['rs yc']:
            self.rs = QVector3D(self.rs.x(), inputFl, self.rs.z())
        elif row == self.labelToRow['rs zc']:
            self.rs = QVector3D(self.rs.x(), self.rs.y(), inputFl)
    
    def floatToWidgetItem(self, fl):
        flStr = '{0:.2f}'.format(fl)
        return QtGui.QTableWidgetItem(flStr)
    
    def setWidgetValue(self,key,value):
        '''
        When setting an item to the table, the cellChanged signal must be blocked or else 
        the system will catch it and enter an infinite loop
        '''
        self.blockSignals(True)
        self.setItem(self.labelToRow[key],0,self.floatToWidgetItem(value))
        self.blockSignals(False)
        self.constantsSaved = False
        
    def setWidgetVector(self, keyX, keyY, keyZ, vector):
        self.setWidgetValue(keyX,vector.x())
        self.setWidgetValue(keyY,vector.y())
        self.setWidgetValue(keyZ,vector.z())
        
    def clamp(self, n, mini, maxi):
        return max(min(n, maxi), mini)    
           
    @CGH.qpp.getter
    def qpp(self):
        return self._qpp
    
    @qpp.setter
    def qpp(self, value):
        value = self.clamp(value, self.min_dict['qpp'], self.max_dict['qpp'])
        self._qpp = value
        self.updateSlmGeometry()
        self.compute()
        self.setWidgetValue('qpp',value)
        
    @CGH.alpha.getter
    def alpha(self):
        return self._alpha
    
    @alpha.setter
    def alpha(self, value):
        value = self.clamp(value, self.min_dict['alpha'], self.max_dict['alpha'])
        self._alpha = value
        self.updateSlmGeometry()
        self.compute()
        self.setWidgetValue('alpha',value)
        
    @CGH.theta.getter
    def theta(self):
        return self._theta
    
    @theta.setter
    def theta(self, value):
        value = self.clamp(value, self.min_dict['theta'], self.max_dict['theta'])
        self._theta = value
        self.updateTransformationMatrix()
        self.compute()
        self.setWidgetValue('theta',value)
    
    @CGH.rc.getter
    def rc(self):
        return self._rc
    
    @rc.setter
    def rc(self, vector):
        if type(vector) == QtCore.QPointF:
            vector = QVector3D(vector)
        self._rc = QVector3D(self.clamp(vector.x(), self.min_dict['rc xc'], self.max_dict['rc xc']), self.clamp(vector.y(), self.min_dict['rc yc'], self.max_dict['rc yc']), self.clamp(vector.z(), self.min_dict['rc zc'], self.max_dict['rc zc']))
        self.updateTransformationMatrix()
        self.compute()
        self.setWidgetVector('rc xc', 'rc yc', 'rc zc', self._rc)
    
    @CGH.rs.getter
    def rs(self):
        return self._rs
    
    @rs.setter
    def rs(self, vector):
        if type(vector) == QtCore.QPointF:
            vector = QVector3D(vector)
        self._rs = QVector3D(self.clamp(vector.x(), self.min_dict['rs xc'], self.max_dict['rs xc']), self.clamp(vector.y(), self.min_dict['rs yc'], self.max_dict['rs yc']), self.clamp(vector.z(), self.min_dict['rs zc'], self.max_dict['rs zc']))
        self.updateSlmGeometry()
        self.compute()
        self.setWidgetVector('rs xc', 'rs yc', 'rs zc', self._rs)
             
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    slm = QSLM()
    cgh = QCGH(slm=slm)
    sys.exit(app.exec_())
