
"""QFabRecorder.py: pyqtgraph module to record and play video files"""

import pyqtgraph as pg
import cv2
import numpy as np

class QFabRecorder(pg.ImageItem):
    '''
    Grabs frames from QCameraItem and records them if record=True.
    Saves file to ~/
    '''
    
    def __init__(self, camera=None, parent=None, **kwargs):
        '''
        Creates a fabrecorder.
        keyword camera: a QCameraItem
        '''
        super(QFabRecorder, self).__init__(parent, **kwargs)
        self.camera = camera
        self._record = True
        self.record = self._record #camera starts playing upon creation of fabrecorder

    @property
    def record(self):
        return self._record

    @record.setter
    def record(self, record):
        '''
        If record is true, connect to signal from QCameraItem.nextFrame().
        If false, disconnect from signal and save to video file
        parameter record: boolean value that determines whether to record frames
        '''
        if (typeOf(record) != bool):
            raise ValueError("Record must be of type boolean")
        self._record = record
        if (record):
            pass
        else:
            pass
                
        

class QFabMovie(pg.ImageItem):
    '''
    Video source for pyqtgraph applications. Plays video in the viewbox of
    QFabGraphicsView
    '''

    def __init__(self, file):
        '''
        Creates a fabmovie.
        parameter 'file': video file to play
        '''
        self.file = file

    def pause():
        pass

    def cleanup():
        pass


if __name__ == '__main__':
    import sys
    app = PyQt4.QtGui.QApplcation(sys.argv)
    sys.exit(app.exec_())
    
