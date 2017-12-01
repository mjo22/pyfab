#!/usr/bin/env python

"""CGH.py: compute phase-only holograms for optical traps."""

import numpy as np
<<<<<<< HEAD
from pyqtgraph.Qt import QtGui, QtCore
from numba import jit
from QSLM import QSLM
=======
from PyQt4 import QtGui, QtCore
from numba import jit
import json
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f


class CGH(object):
    """Base class for computing computer-generated holograms.

    For each trap, the coordinate r obtained from the fabscreen
    is measured relative to the calibrated location rc of the
    zeroth-order focal point, which itself is measured relative to
    the center of the focal plane. The resulting displacement is
    projected onto the coordinate system in the SLM place.
    Projection involves a calibrated rotation about z with
    a rotation matrix m.

    The hologram is computed using calibrated wavenumbers for
    the Cartesian coordinates in the SLM plane.  These differ from
    each other because the SLM is likely to be tilted relative to the
    optical axis.
    """

    def __init__(self, slm=None):
        # Trap properties for current pattern
        self.trapdata = []

        # SLM geometry
        self.slm = slm
        self.w = self.slm.width()
        self.h = self.slm.height()
<<<<<<< HEAD
        # Conversion from SLM pixels to wavenumbers
        # Calibration constant:
        # qpp: float
        self._qpp = 2. * np.pi / self.w / 10.
        # Effective aspect ratio of SLM pixels
        # Calibration constant:
        # alpha: float
        self._alpha = 1.
        # Location of optical axis in SLM coordinates
        # Calibration constant:
        # rs: QPointF
        self.rs = QtCore.QPointF(self.w / 2., self.h / 2.)

        # Coordinate transformation matrix for trap locations
        self.transformationMatrix = QtGui.QMatrix4x4()
        # Calibration constant:
        # location of optical axis in camera coordinates
        self._rc = QtCore.QPointF()
        # Calibration constant:
        # orientation of camera relative to SLM
        self._theta = 0.
        
    @jit
    def compute(self):
        psi = np.zeros((self.w, self.h), dtype=np.complex_)
        for properties in self.trapdata:
            r = self.transformationMatrix.map(properties['r'])
            amp = properties['a'] * np.exp(1j * properties['phi'])
            ex = np.exp(self.iqx * r.x() + self.iqxsq * r.z())
            ey = np.exp(self.iqy * r.y() + self.iqysq * r.z())
            psi += np.outer(amp*ex, ey)
        phi = (128 * (np.angle(psi) / np.pi + 1.)).astype(np.uint8)
        self.slm.setData(phi)

    def updateSlmGeometry(self):
        """Compute position-dependent properties in SLM plane.
        """
        qx = np.linspace(-self.rs.x(), self.w - 1 - self.rs.x(), self.w)
        qy = np.linspace(-self.rs.y(), self.h - 1 - self.rs.y(), self.h)
        qx = self._qpp * qx
        qy = self._alpha * self._qpp * qy
        self.iqx = 1j * qx
        self.iqy = 1j * qy
        self.iqxsq = 1j * qx * qx
        self.iqysq = 1j * qy * qy

=======

        # Conversion from SLM pixels to wavenumbers
        self._qpp = 2. * np.pi / self.w / 10.
        # Effective aspect ratio of SLM pixels
        self._alpha = 1.
        # Location of optical axis in SLM coordinates
        self._rs = QtCore.QPointF(self.w / 2., self.h / 2.)
        self.updateGeometry()

        # Coordinate transformation matrix for trap locations
        self.m = QtGui.QMatrix4x4()
        # Location of optical axis in camera coordinates
        self._rc = QtGui.QVector3D(320., 240., 0.)
        # Orientation of camera relative to SLM
        self._theta = 0.
        self.updateTransformationMatrix()

    @jit(parallel=True)
    def compute_one(self, amp, x, y, z):
        """Compute phase hologram for one trap with
        specified complex amplitude and position
        """
        ex = np.exp(self.iqx * x + self.iqxsq * z)
        ey = np.exp(self.iqy * y + self.iqysq * z)
        return np.outer(amp * ex, ey)

    @jit(parallel=True)
    def compute(self):
        """Compute phase hologram for specified traps
        """
        psi = np.zeros((self.w, self.h), dtype=np.complex_)
        for properties in self.trapdata:
            r = self.m * properties['r']
            amp = properties['a'] * np.exp(1j * properties['phi'])
            psi += self.compute_one(amp, r.x(), r.y(), r.z())
        phi = (256. * (np.angle(psi) / np.pi + 1.)).astype(np.uint8)
        self.slm.data = phi

    def updateGeometry(self):
        """Compute position-dependent properties in SLM plane.
        """
        qx = np.linspace(-self.rs.x(), self.w - 1 - self.rs.x(), self.w)
        qy = np.linspace(-self.rs.y(), self.h - 1 - self.rs.y(), self.h)
        qx = self.qpp * qx
        qy = self.alpha * self.qpp * qy
        self.iqx = 1j * qx
        self.iqy = 1j * qy
        self.iqxsq = 1j * qx * qx
        self.iqysq = 1j * qy * qy

>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
    @property
    def rs(self):
        return self._rs

    @rs.setter
    def rs(self, rs):
<<<<<<< HEAD
        self._rs = rs
        self.updateSlmGeometry()
=======
        if isinstance(rs, QtCore.QPointF):
            self._rs = rs
        else:
            self._rs = QtCore.QPointF(rs[0], rs[1])
        self.updateGeometry()
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
        self.compute()

    @property
    def qpp(self):
        return self._qpp

    @qpp.setter
<<<<<<< HEAD
    def qpp(self, value):
        self._qpp = value
        self.updateSlmGeometry()
=======
    def qpp(self, qpp):
        self._qpp = float(qpp)
        self.updateGeometry()
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
        self.compute()

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
<<<<<<< HEAD
    def alpha(self, value):
        self._alpha = value
        self.updateSlmGeometry()
        self.compute()

    def updateTransformationMatrix(self):
        self.transformationMatrix.setToIdentity()
        self.transformationMatrix.translate(-self._rc.x(), -self._rc.y())
        self.transformationMatrix.rotate(self._theta, 0., 0., 1.)
=======
    def alpha(self, alpha):
        self._alpha = float(alpha)
        self.updateGeometry()
        self.compute()

    def updateTransformationMatrix(self):
        self.m.setToIdentity()
        self.m.translate(-self.rc)
        self.m.rotate(self._theta, 0., 0., 1.)
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f

    @property
    def rc(self):
        return self._rc

    @rc.setter
<<<<<<< HEAD
    def rc(self, value):
        self._rc = value
=======
    def rc(self, rc):
        if isinstance(rc, QtGui.QVector3D):
            self._rc = rc
        else:
            self._rc = QtGui.QVector3D(rc[0], rc[1], rc[2])
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
        self.updateTransformationMatrix()
        self.compute()

    @property
    def theta(self):
        return self._theta

    @theta.setter
<<<<<<< HEAD
    def theta(self, value):
        self._theta = value
        self.updateTransformationMatrix()
        self.compute()
        
    def setData(self, trapdata):
        self.trapdata = trapdata
        self.compute()
        
    @property
    def calibration(self):
        return {'qpp': self.qpp,
                'alpha' : self.alpha,
                'rs': self.rs,
                'rc': self.rc,
=======
    def theta(self, theta):
        self._theta = float(theta)
        self.updateTransformationMatrix()
        self.compute

    def setData(self, trapdata):
        self.trapdata = trapdata
        self.compute()

    @property
    def calibration(self):
        return {'qpp': self.qpp,
                'alpha': self.alpha,
                'rs': (self.rs.x(), self.rs.y()),
                'rc': (self.rc.x(), self.rc.y(), self.rc.z()),
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
                'theta': self.theta}

    @calibration.setter
    def calibration(self, values):
        if not isinstance(values, dict):
            return
<<<<<<< HEAD
        if values.has_key('qpp'):
            self._qpp = values['qpp']
        if values.has_key('alpha'):
            self._alpha = values['alpha']
        if values.has_key('rs'):
            self._rs = values['rs']
        if values.has_key('rc'):
            self._rc = values['rc']
        if values.has_key('theta'):
            self._theta = values['theta']
        self.updateSlmGeometry()
        self.updateTransformationMatrix()
        self.compute()
=======
        for attribute, value in values.iteritems():
            try:
                setattr(self, attribute, value)
            except AttributeError:
                print('unknown attribute:', attribute)

    def serialize(self):
        return json.dumps(self.calibration,
                          indent=2,
                          separators=(',', ': '),
                          ensure_ascii=False)

    def deserialize(self, s):
        values = json.loads(s)
        self.calibration = values
>>>>>>> 6532502fe930486ec1e7d5fabb39cf57644da78f
