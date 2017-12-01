<<<<<<< HEAD
import cv2
from QCameraItem import QCameraItem
from PyQt4 import QtGui
from datetime import datetime
=======
#!/usr/bin/env python

import cv2
from QVideoItem import QVideoItem
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
import os


class fabdvr(object):

<<<<<<< HEAD
    def __init__(self, camera=None, filename='fabdvr'):
        self._writer = None
        self.camera = camera
        self.filename = filename
        self._framenumber = 0
        self._nframes = 0
        self._fourcc = cv2.cv.CV_FOURCC(*'FMP4')

    def record(self, nframes=None):
        if (nframes > 0):
            self._nframes = nframes
        self.start()

    def start(self):
        if not self.hascamera():
            return
        self.framenumber = 0
        self._writer = cv2.VideoWriter(self.filename,
                                           self._fourcc,
                                           self.camera.device.fps,
                                           self.size(),
                                           not self.camera.device.gray)
        self.camera.sigNewFrame.connect(self.write)

    def stop(self):
        if self.isrecording():
            self.camera.sigNewFrame.disconnect()
=======
    def __init__(self,
                 source=None,
                 filename='~/data/fabdvr.avi',
                 codec='HFYU', **kwds):
        """Record digital video stream with lossless compression

        :param camera: object reference to QCameraItem
        :param filename: video file name.  Extension determines container.
        ;    Not all containers work with all codecs.
        :param codec: FOURCC descriptor for video codec
        :returns: 
        :rtype: 
        ;
        ;Note on codecs:
        ;    On macs, FFV1 appears to work with avi containers
        ;    On Ubuntu 16.04, HFYU works with avi container.
        ;        FFV1 fails silently
        ;        LAGS does not work (not found)

        """
        super(fabdvr, self).__init__(**kwds)
        self._writer = None
        self.source = source
        self.filename = filename
        self._framenumber = 0
        self._nframes = 0
        if cv2.__version__.startswith('2'):
            self._fourcc = cv2.cv.CV_FOURCC(*codec)
        else:
            self._fourcc = cv2.VideoWriter_fourcc(*codec)

    def record(self, nframes=100):
        if (nframes > 0):
            self._nframes = nframes
            self.start()

    def start(self):
        if not self.hassource():
            return
        self.framenumber = 0
        self._writer = cv2.VideoWriter(self.filename,
                                       self._fourcc,
                                       self.source.device.fps,
                                       self.size(),
                                       not self.source.gray)
        self.source.sigNewFrame.connect(self.write)

    def stop(self):
        if self.isrecording():
            self.source.sigNewFrame.disconnect()
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
            self._writer.release()
        self.nframes = 0
        self._writer = None

    def write(self, frame):
<<<<<<< HEAD
        img = cv2.transpose(frame)
        img = cv2.flip(img, 0)
        self._writer.write(img)
        if (self._nframes > 0):
            self.framenumber += 1
            if (self.framenumber == self._nframes):
                self.stop()

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, camera):
        if isinstance(camera, QCameraItem):
            self._camera = camera
=======
        if self.source.transposed:
            frame = cv2.transpose(frame)
        if self.source.flipped:
            frame = cv2.flip(frame, 0)
        self._writer.write(frame)
        self.framenumber += 1
        if (self.framenumber == self._nframes):
            self.stop()
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
<<<<<<< HEAD
        ts = "_%s:%s_%s" % (datetime.now().hour, datetime.now().minute, datetime.now().date())
	fn = filename + ts + ".avi"		
	filepath = os.path.join(os.path.expanduser('~'), 'fabvideo', fn)
        if not self.isrecording():
            self._filename = filepath

    def hascamera(self):
        return isinstance(self.camera, QCameraItem)
=======
        if not self.isrecording():
            self._filename = os.path.expanduser(filename)

    def hassource(self):
        return isinstance(self.source, QVideoItem)
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f

    def isrecording(self):
        return (self._writer is not None)

    def size(self):
<<<<<<< HEAD
        if self.hascamera():
            sz = self.camera.size
=======
        if self.hassource():
            sz = self.source.device.size
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
            w = int(sz.width())
            h = int(sz.height())
            return (w, h)
        else:
            return None

    def framenumber(self):
        return self._framenumber


<<<<<<< HEAD
class QFabdvr(QtGui.QWidget):
    '''Widget to implement fabdvr and record video
    '''
    def __init__(self, camera, parent=None, **kwargs):
        super(QFabdvr, self).__init__(parent, **kwargs)
        
        self.setGeometry(200,100,300,200)

        self.dvr = fabdvr(camera=camera)    #create dvr
        
        self._recordB = QtGui.QPushButton("Record")
        self._stopB =  QtGui.QPushButton("Stop")    #create fields for buttons

        self.recordB = self._recordB
        self.stopB = self._stopB    #call button setters

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.recordB)
        self.layout.addWidget(self.stopB) 
	self.setLayout(self.layout)    #set layout of QFabdvr
        self.show()

    @property
    def recordB(self):
        return self._recordB
    
    @recordB.setter
    def recordB(self, button):
        self._recordB = button
        self._recordB.clicked.connect(self.dvr.start)

    @property
    def stopB(self):
        return self._stopB
    
    @stopB.setter
    def stopB(self, button):
        self._stopB = button
        self._stopB.clicked.connect(self.dvr.stop)


if __name__ == '__main__':
    from PyQt4 import QtGui
    from QCameraItem import QCameraDevice, QCameraWidget
=======
if __name__ == '__main__':
    from PyQt4 import QtGui
    from QCameraDevice import QCameraDevice
    from QVideoItem import QVideoWidget
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
    import sys

    app = QtGui.QApplication(sys.argv)
    device = QCameraDevice(size=(640, 480), gray=True)
<<<<<<< HEAD
    camera = QCameraItem(device)
    widget = QCameraWidget(camera, background='w')
    widget.show()
    dvr = fabdvr(camera=camera)
    dvr.record(100)
=======
    source = QVideoItem(device)
    widget = QVideoWidget(source, background='w')
    widget.show()
    dvr = fabdvr(source=source)
    dvr.record(24)
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
    sys.exit(app.exec_())
