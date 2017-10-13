
"""QFabRecorder.py: pyqtgraph module to record and play video files"""

import pyqtgraph as pg
import cv2
import numpy as np
from datetime import datetime

class QFabRecorder(QObject):
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
	now = datetime.now()
        ts = "%s %s:%s" % (now.date(), now.hour, now.minute)
	self.fn = runname.append(ts + ".avi")
        self._record = True	#must be initialized to true
	self.record = self._record

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
        if (type(record) = bool):
            raise ValueError("record must be of type boolean")
        self._record = record
        if (record):

	    self.camera.sigFrameReady.connect(self.write)
        else:
            self.stop
            self.save
                
    def write(self, frame):
	#private
        '''Grabs frames from self.camera and writes them to self.file
	==============  ===================================================================
        **Arguments:**
        frame    	Frame emitted by camera to be written to .avi file. Is type np.ndarray.
        ==============  ===================================================================
        '''
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	self.writer = cv2.VideoWriter('~/fabvideo/' + self.fn, fourcc, 20.0, (640,480))
	self.writer.write(frame)

    def stop(self):
	#public
	pass

    def save(self):
	#private
	pass

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
    
