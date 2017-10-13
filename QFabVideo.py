
"""QFabRecorder.py: pyqtgraph module to record and play video files"""

from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
import cv2
import numpy as np
from datetime import datetime

class QFabRecorder(QtCore.QObject):
    '''Grabs frames from QCameraItem and records them if record=True.
    Saves file to ~/fabvideo/fabDATE HOUR:MINUTE
    '''
    
    def __init__(self, camera, parent=None, **kwargs):
        '''Creates a fabrecorder.
        ==============  ===================================================================
        **Arguments:**
        camera    	a QCameraItem acting as video source for recording
        ==============  ===================================================================
        '''
        super(QFabRecorder, self).__init__(parent, **kwargs)
        self.camera = camera
	runname = "fab"
        ts = "%s %s:%s" % (datetime.now().date(), datetime.now().hour, datetime.now().minute)
	self.fn = runname + ts + ".avi"		#create filename
	fourcc = cv2.cv.CV_FOURCC(*'XVID')
	self.writer = cv2.VideoWriter('~/fabvideo/' + self.fn, fourcc, self.camera.cameraDevice.fps, (int(self.camera.cameraDevice.size.width()), int(self.camera.cameraDevice.size.height())))
        self._record = True	#must be initialized to true
	self.record = self._record	#begin recording

    @property
    def record(self):
        return self._record

    @record.setter
    def record(self, record):
	#public
        '''If record is true, connect to signal from QCameraItem.nextframe() and start record
        If false, disconnect from signal and save to video file
	==============  ===================================================================
        **Arguments:**
        record    	Boolean value that determines whether to record frames
        ==============  ===================================================================
        '''
        if (type(record) != bool):
            raise ValueError("record must be of type boolean")
        self._record = record
	self.i = 0
        while(record and self.i<1000):	#for testing purposes, just write 1000 frames
	    self.camera.sigFrameReady.connect(self.write)
	    self.i = self.i + 1
        self.stop
                
    def write(self, frame):
	#private
        '''Grabs frames from self.camera and writes them to self.file
	==============  ===================================================================
        **Arguments:**
        frame    	Frame emitted by camera to be written to .avi file. Is type np.ndarray.
        ==============  ===================================================================
        '''
	self.writer.write(frame)

    def stop(self):
	#public
	self.camera.sigFrameReady.disconnect()
	#save
	self.writer.release()
	#how to destroy this object in memory?

class QFabMovie(pg.ImageItem):
    '''Video source for pyqtgraph applications. Plays video in the viewbox of
    QFabGraphicsView
    '''

    def __init__(self, file, parent=None, **kwargs):
        '''
        Creates a fabmovie.
        ==============  ===================================================================
        **Arguments:**
        file    	File name and path (~/path/to/file/file.avi) that will be played in
			QFabGraphicsView viewbox.
        ==============  ===================================================================
        '''
        super(QFabMovie, self).__init__(parent, **kwargs)
        self.file = file

    def pause(self):
	#public
        pass

    def cleanup(self):
	#public
        pass


if __name__ == '__main__':
    import sys
    app = PyQt4.QtGui.QApplcation(sys.argv)
    sys.exit(app.exec_())
    
