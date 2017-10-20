
"""QFabRecorder.py: pyqtgraph module to record and play video files"""

from pyqtgraph import QtCore, QtGui
import pyqtgraph as pg
import cv2
from skvideo.io import VideoWriter
import numpy as np
from datetime import datetime
import os

class QFabRecorder(QtCore.QObject):
    '''Grabs frames from QCameraItem and records them if record=True.
    Saves file to ~/fabvideo/fabDATE HOUR:MINUTE
    '''
    
    def __init__(self, camera, record=True, parent=None, **kwargs):
        '''Creates a fabrecorder.
        ==============  ===================================================================
        **Arguments:**
        camera    	a QCameraItem acting as video source for recording
        ==============  ===================================================================
        '''
        super(QFabRecorder, self).__init__(parent, **kwargs)
        self.camera = camera

	#create file name and open VideoWriter
	runname = "fab"
        ts = "%s %s:%s" % (datetime.now().date(), datetime.now().hour, datetime.now().minute)
	fn = runname + ts + ".avi"		#create filename
	fourcc = cv2.cv.CV_FOURCC(*'XVID')
	path = os.path.join(os.path.expanduser('~'), 'fabvideo', fn)
	self.writer = cv2.VideoWriter(path, fourcc, self.camera.cameraDevice.fps, (int(self.camera.cameraDevice.size.width()), int(self.camera.cameraDevice.size.height())))
	#self.writer.open(path, fourcc, self.camera.cameraDevice.fps, (int(self.camera.cameraDevice.size.width()), int(self.camera.cameraDevice.size.height())))
	'''
	self.writer = VideoWriter(path, frameSize=(self.camera.cameraDevice.size.width(), self.camera.cameraDevice.size.height()))
	self.writer.open()
	'''
	#set properties
	self._pause = True
	self._record = record	#initialized to true by default
	self.record = self._record	#begin recording


    @property
    def record(self):
        return self._record

    @record.setter
    def record(self, record):
	#public
        '''If record is true, connect to signal from QCameraItem.nextframe() and start record
        If false, disconnect from signal and close writer
	==============  ===================================================================
        **Arguments:**
        record    	Boolean value that determines whether to record frames
        ==============  ===================================================================
        '''
        if (type(record) != bool):
            raise ValueError("record must be of type boolean")
        self._record = record
	if (record):
	    if(self.pause):
		self.pause = False
		self.camera.sigFrameReady.connect(self.write)	
	else:
	    self.stop
                
    def write(self, frame):
	#private
        '''Grabs frames from self.camera and writes them to self.file
	==============  ===================================================================
        **Arguments:**
        frame    	Frame emitted by camera to be written to .avi file. Is type np.ndarray.
        ==============  ===================================================================
        '''
	#TO DO: write is being called continuously, but write is not writing to .avi file. May be a cv2 and linux compatibility problem? 
	self.writer.write(frame)

    def stop(self):
	#public
	'''Disconnects from signal and closes writer.
	'''
	self.camera.sigFrameReady.disconnect()
	self.writer.release()
    
    @property
    def pause(self):
	return self._pause
    

    @pause.setter
    def pause(self, pause):
	#public
	'''
	==============  ===================================================================
        **Arguments:**
        pause   	Boolean value that determines whether the recording is paused.
        ==============  ===================================================================
	'''
	if (type(pause) != bool):
            raise ValueError("pause must be of type boolean")
	self._pause = pause
	if (pause):
	    self.camera.sigFrameReady.disconnect()



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


class QFabcorder(QtGui.QVBoxLayout):
    '''Widget to play and record video'''
    def __init__(self, camera, parent=None, **kwargs):
	'''Initializes
	==============  ===================================================================
        **Arguments:**
        camera   	QCameraItem to be passed to QFabRecorder
        ==============  ===================================================================
	'''
        super(QFabcorder, self).__init__(parent, **kwargs)
	#set geometry

	#init subwidgets

	#add subwidgets
	
	#init recorder
	self.fabrecord = QFabRecorder(camera)

    #define subwidgets
    def fileInput(self):
	pass

    def frames(self):
	pass

    def record(self):
	pass

    def replay(self):
	pass

    def framefeatureNum(self):
	pass

    def mode(self):
	pass


if __name__ == '__main__':
    import sys
    app = PyQt4.QtGui.QApplcation(sys.argv)
    sys.exit(app.exec_())
    
