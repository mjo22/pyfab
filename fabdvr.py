import cv2
from QCameraItem import QCameraItem
from PyQt4 import QtGui
from datetime import datetime
import os


class fabdvr(object):

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
            self._writer.release()
        self.nframes = 0
        self._writer = None

    def write(self, frame):
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

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        ts = "_%s:%s_%s" % (datetime.now().hour, datetime.now().minute, datetime.now().date())
	fn = filename + ts + ".avi"		
	filepath = os.path.join(os.path.expanduser('~'), 'fabvideo', fn)
        if not self.isrecording():
            self._filename = filepath

    def hascamera(self):
        return isinstance(self.camera, QCameraItem)

    def isrecording(self):
        return (self._writer is not None)

    def size(self):
        if self.hascamera():
            sz = self.camera.size
            w = int(sz.width())
            h = int(sz.height())
            return (w, h)
        else:
            return None

    def framenumber(self):
        return self._framenumber


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
    import sys

    app = QtGui.QApplication(sys.argv)
    device = QCameraDevice(size=(640, 480), gray=True)
    camera = QCameraItem(device)
    widget = QCameraWidget(camera, background='w')
    widget.show()
    dvr = fabdvr(camera=camera)
    dvr.record(100)
    sys.exit(app.exec_())
