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
        try:
            self._writer = cv2.VideoWriter(self.filename,
                                           self._fourcc,
                                           self.camera.device.fps,
                                           self.size(),
                                           not self.camera.device.gray)
        except:
            print('did not get video writer!')
            raise
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
	print 'o'
        #self.framenumber += 1
        #if (self.framenumber == self._nframes):
            #self.stop()

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
    '''Widget to play and record video
    '''
    def __init__(self, camera, parent=None, **kwargs):
        super(QFabdvr, self).__init__(parent, **kwargs)

	self.setGeometry(200,100,300,200)

        self.dvr = fabdvr(camera=camera)

        self.layout = QtGui.QHBoxLayout(self)
        record = QtGui.QPushButton("Record", self)
	record.clicked.connect(self.dvr.start)
        stop =  QtGui.QPushButton("Stop", self)
	record.clicked.connect(self.dvr.stop)
        self.layout.addWidget(record)
        self.layout.addWidget(stop)

	self.setLayout(self.layout)
        self.show()
        
        
	#set geometry

	#init subwidgets
        
	#add subwidgets

    #define subwidgets


    
    def fileInput(self):
	pass

    def recorder(self):
	pass

    def replay(self):
	pass

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
