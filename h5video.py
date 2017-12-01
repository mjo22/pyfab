#!/usr/bin/env python

"""Create HDF5 video files"""

import h5py
import time
<<<<<<< HEAD
from PyQt4 import QtCore


class h5video(QtCore.QObject):
=======


class h5video(object):
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
    """Object for writing HDF5 video files
    """

    def __init__(self, filename="h5video.h5", overwrite=False):
        if overwrite:
            self.file = h5py.File(filename, 'w')
        else:
            self.file = h5py.File(filename, 'w-')
        self.file.attrs['timestamp'] = time.asctime()
        self.file.attrs['HDF5_version'] = h5py.version.hdf5_version
        self.file.attrs['h5py_version'] = h5py.version.version
        self.images = self.file.create_group("images")
        self.images.attrs['timestamp'] = time.asctime()

    def close(self):
        if isinstance(self.file, h5py.File):
            self.file.flush()
            self.file.close()
            self.images = None
            self.file = None

    def timestamp(self):
        return "%.6f" % time.time()

    def write(self, image):
<<<<<<< HEAD
	print 'h5 write'
=======
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
        self.images.create_dataset(self.timestamp(), data=image)

    def filename(self):
        return self.file.filename()


def main():
    import numpy as np

    video = h5video("junk.h5", overwrite=True)
    for i in np.arange(10):
        video.write(np.random.randint(0, 256, size=(480, 640),
                                      dtype=np.uint8))
    video.close()

if __name__ == "__main__":
    main()
