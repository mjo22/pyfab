
"""QFabRecorder.py: pyqtgraph module to record and play video files"""

import pyqtgraph as pg
import cv2
import numpy as np
from datetime import datetime

class QFabRecorder(QObject):
    '''
    Grabs frames from QCameraItem and records them if record=True.
    Saves file to ~/fabvideo
    '''
    
    def __init__(self, camera, parent=None, **kwargs):
        '''
        Creates a fabrecorder.
        parameter camera: a QCameraItem
        '''
        super(QFabRecorder, self).__init__(parent, **kwargs)
        self.camera = camera
        self._record = True	#must be initialized to true

    @property
    def record
        return self._record

    @record.setter
    def record(self, record)
        '''
        If record is true, connect to signal from QCameraItem.nextframe() and start record
        If false, disconnect from signal and save to video file
        parameter record: boolean value that determines whether to record frames
        '''
        if (type(record) = bool):
            raise ValueError("record must be of type boolean")
        self._record = record
        if (record):
	    runname = "fab"
	    now = datetime.now()
	    ts = "%s %s:%s" % (now.date(), now.hour, now.minute)
	    self.fn = runname.append(ts + ".avi")
	    self.camera.sigFrameReady.connect(self.write)
        else:
            self.stop
            self.save
                
    def write(self, frame):
        '''
        Grabs frames from self.camera and writes them to self.file
        '''
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	self.writer = cv2.VideoWriter(self.fn, fourcc, 20.0, (640,480))
	while (self.record):
	    self.writer.write(frame)

    def stop(self):
	pass

    def save(self):
	pass

class QFabMovie(pg.ImageItem):
    '''
    Video source for pyqtgraph applications. Plays video in the viewbox of
    QFabGraphicsView
    '''

    def __init__(self, file, parent=None, **kwargs):
        '''
        Creates a fabmovie.
        parameter 'file': video file to play
        '''
        super(QFabMovie, self).__init__(parent, **kwargs)
        self.file = file

    def pause(self):
        pass

    def cleanup(self):
        pass


if __name__ == '__main__':
    import sys
    app = PyQt4.QtGui.QApplcation(sys.argv)
    sys.exit(app.exec_())
    
