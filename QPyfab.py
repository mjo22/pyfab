#!/usr/bin/env python

"""QPyfab.py: Application that implements GUI holographic optical trapping."""

from pyqtgraph.Qt import QtGui, QtCore
from traps import QTrappingPattern
from QFabGraphicsView import QFabGraphicsView
from QSLM import QSLM
from CGH import CGH
from QCGH import QCGH
from QFabDVR import QFabDVR
from QFabVideo import QFabVideo
from QFabFilter import QFabFilter
import sys
import io
import datetime
import os


class QPyfab(QtGui.QMainWindow):
	
    sigClosed = QtCore.pyqtSignal()

    def __init__(self):
		super(QPyfab, self).__init__()
		self.init_hardware()
		self.init_ui()
		self.init_configuration()

    def init_hardware(self):
		# video screen
        screen_size = (640, 480)
        self.fabscreen = QFabGraphicsView(
            size=screen_size, gray=True, mirrored=False)
        # DVR
        self.dvr = QFabDVR(source=self.fabscreen.video)
        # spatial light modulator
        self.slm = QSLM()
        # computation pipeline for the trapping pattern
        self.pattern = QTrappingPattern(self.fabscreen)
        self.cgh = CGH(self.slm)
        self.pattern.pipeline = self.cgh

    def init_ui(self):
        self.setWindowTitle("Pyfab")
        #set layout
        wpyfab = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        layout.addWidget(self.fabscreen)
        wcontrols = QtGui.QWidget()
        controls = QtGui.QVBoxLayout()
        controls.setSpacing(1)
        controls.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        controls.addWidget(self.dvr)
        self.wvideo = QFabVideo(self.fabscreen.video)
        controls.addWidget(self.wvideo)
        controls.addWidget(QFabFilter(self.fabscreen.video))
        controls.addWidget(QCGH(self.cgh))
        wcontrols.setLayout(controls)
        layout.addWidget(wcontrols)
        wpyfab.setLayout(layout)
        #create menu bar
        menu = QtGui.QMenuBar()
        #calibration menu
        self.calMenu = menu.addMenu('Calibration')
        self._save = QtGui.QAction('&Save', self)
        self.save = self._save
        self.calMenu.addAction(self.save)
        self._restore = QtGui.QAction('&Restore', self)
        self.restore = self._restore
        self.calMenu.addAction(self._restore)
        self.setMenuBar(menu)
        
        self.setCentralWidget(wpyfab)
        self.show()
        self.dvr.recording.connect(self.handleRecording)

    def handleRecording(self, recording):
        self.wvideo.enabled = not recording

    def init_configuration(self):
        sz = self.fabscreen.video.device.size
        self.cgh.rc = (sz.width() / 2, sz.height() / 2, 0.)
        sz = self.slm.size()
        self.cgh.rs = (sz.width() / 2, sz.height() / 2)

    def save_configuration(self):
        scgh = self.cgh.serialize()
        tn = datetime.datetime.now()
        fn = '~/.pyfab/pyfab_{:%Y%b%d_%H:%M:%S}.json'.format(tn)
        fn = os.path.expanduser(fn)
        with io.open(fn, 'w', encoding='utf8') as configfile:
            configfile.write(unicode(scgh))
            
            
    def closeEvent(self, event):
        self.save_configuration()
        self.slm.close()
        self.fabscreen.camera.close()
        self.sigClosed.emit()
            
    #Calibration menu QActions
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
    app = QtGui.QApplication(sys.argv)
    instrument = QPyfab()
    sys.exit(app.exec_())
