#!/usr/bin/env python

"""pyfab.py: Application that implements GUI holographic optical trapping.
   Dependecies: pyqtgraph=0.10, ipython=2
   Commands for usage: 
		1) ipython
		2) from pyfab import pyfab
		3) pyfab()
"""
from pyqtgraph.Qt import QtGui, QtCore
from traps import QTrappingPattern, QTrapWidget
from QFabGraphicsView import QFabGraphicsView
from QSLM import QSLM
try:
    from cudaCGH import cudaCGH
except ImportError:
    from CGH import CGH
from QCGH import QCGH
from QFabDVR import QFabDVR
from QFabVideo import QFabVideo
from QFabFilter import QFabFilter
import sys
import io
import datetime
import os


class pyfab(QtGui.QMainWindow):

    def __init__(self, size=(640, 480)):
        self.app = QtGui.QApplication(sys.argv)
        super(pyfab, self).__init__()
        self.init_hardware(size)
        self.init_ui()
        self.init_configuration()

    def init_hardware(self, size):
        # video screen
        self.fabscreen = QFabGraphicsView(size=size, gray=True)
        self.video = QFabVideo(self.fabscreen.video)
        self.filters = QFabFilter(self.fabscreen.video)
        # DVR
        self.dvr = QFabDVR(source=self.fabscreen.video)
        self.dvr.recording.connect(self.handleRecording)
        # spatial light modulator
        self.slm = QSLM()
        # computation pipeline for the trapping pattern
        try:
            self.cgh = cudaCGH(self.slm)
        except NameError:
            self.cgh = CGH(self.slm)
        self.pattern = QTrappingPattern(self.fabscreen)
        self.pattern.pipeline = self.cgh

    def init_ui(self):
        self.setWindowTitle("Pyfab")
        #geometry
        desktop = QtGui.QDesktopWidget()
        w = desktop.screenGeometry().width()
        h = desktop.screenGeometry().height()
        r = w/h
        self.setGeometry(w/4, w/5, w/2, h/2)
        #set layout
        wpyfab = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        layout.addWidget(self.fabscreen)
        wpyfab.setLayout(layout)
        #menu bar
        self.menu = QtGui.QMenuBar()
        self.calibrationMenu()
        self.setMenuBar(self.menu)
        #tabs
        tabs = QtGui.QTabWidget()
        tabs.addTab(self.controlTab(), 'Controls')
        tabs.addTab(self.trapTab(), 'Traps')
        layout.addWidget(tabs)
        layout.setStretch(0,2)
        layout.setStretch(1,1)
        #tabs.setFixedSize(tabs.size())
        layout.setAlignment(tabs, QtCore.Qt.AlignTop)
        wpyfab.setLayout(layout)
        self.setCentralWidget(wpyfab)
        
        
        self.show()
        
    def calibrationMenu(self):
        calMenu = self.menu.addMenu('Calibration')
        self._save = QtGui.QAction('&Save', self)
        self.save = self._save
        calMenu.addAction(self.save)
        self._restore = QtGui.QAction('&Restore', self)
        self.restore = self._restore
        calMenu.addAction(self._restore)

    def controlTab(self):
        wcontrols = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setSpacing(1)
        layout.addWidget(self.dvr)
        layout.addWidget(self.video)
        layout.addWidget(self.filters)
        layout.addWidget(QCGH(self.cgh))
        wcontrols.setLayout(layout)
        return wcontrols

    def trapTab(self):
        wtraps = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setSpacing(1)
        layout.addWidget(QTrapWidget(self.pattern))
        wtraps.setLayout(layout)
        return wtraps

    def handleRecording(self, recording):
        self.video.enabled = not recording

    def init_configuration(self):
        sz = self.fabscreen.video.device.size
        self.cgh.rc = (sz.width() / 2, sz.height() / 2, 0.)
        sz = self.slm.size()
        self.cgh.rs = (sz.width() / 2, sz.height() / 2)

    def save_configuration(self):
        scgh = self.cgh.serialize()
        tn = datetime.datetime.now()
        fn = '~/.pyfab/pyfab_{:%Y%b%d_%H:%M:%S}.json'.format(tn)
        with io.open(fn, 'w', encoding='utf8') as configfile:
            configfile.write(unicode(scgh))

    def closeEvent(self, event):
        self.save_configuration()
        self.slm.close()
        self.fabscreen.camera.close()
        self.app.closeAllWindows()
        self.app.exit()
            
    #QActions
	@property
	def save(self):
		return self._save
	
	@save.setter
	def save(self, save):
		self._save = save
		self._save.setShortcut('Ctrl+S')
		self._save.triggered.connect(self.save_configuration)
		
	@property
	def restore(self):
		return self._restore
		
	@restore.setter
	def restore(self, restore):
		self._restore = restore
		self._restore.setShortcut('Ctrl+R')
		#self._restore.triggered.connect(self.)
        

if __name__ == '__main__':
    instrument = pyfab()
    sys.exit(app.exec_())
