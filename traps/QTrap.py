#!/usr/bin/env python

"""QTrap.py: Base class for an optical trap."""

import numpy as np
import pyqtgraph as pg
from PyQt4 import QtCore, QtGui
from states import states


class QTrap(object):
    """A trap has physical properties, including three-dimensional
    position, relative amplitude and relative phase.
    It also has an appearance as presented on the QFabScreen.
    """

    def __init__(self, parent=None, r=None, a=None, phi=None,
                 state=None, name=None):
        # organization
        self.parent = parent
        self.name = name
        # physical properties
        self._r = QtGui.QVector3D(0, 0, 0)
        if a is None:
            a = 1.
        if phi is None:
            phi = np.random.uniform() * 2 * np.pi
        self.r = r
        self.a = a
        self.phi = phi
        # appearance
        symbol = 'o'
        self.brush = {states.normal: pg.mkBrush(100, 255, 100, 120),
                      states.selected: pg.mkBrush(255, 100, 100, 120),
                      states.grouping: pg.mkBrush(255, 255, 100, 120)}
        self.pen = pg.mkPen('k', width=0.5)
        self.symbol = symbol
        # operational state
        self._state = None
        self.state = state

    def moveBy(self, dr):
        """Translate trap.
        """
        self.r = self.r + dr
        

    def isWithin(self, rect):
        """Return True if this trap lies within the specified rectangle.
        """
        return rect.contains(self.pos)

    @property
    def r(self):
        """Three-dimensional position of trap."""
        return self._r

    @r.setter
    def r(self, r):
        if r is None:
            return
        elif type(r) == QtGui.QVector3D:
            self._r = r
        elif type(r) == QtCore.QPointF:
            z = self._r.z()
            self._r = QtGui.QVector3D(r)
            self._r.setZ(z)
        elif isinstance(r, (list, tuple)):
            self._r = QtGui.QVector3D(r[0], r[1], r[2])

    @property
    def pos(self):
        """In-plane position of trap.
        """
        return self.r.toPointF()

    @property
    def state(self):
        """Current state of trap
        """
        return self._state

    @state.setter
    def state(self, state):
        if self._state == states.static:
            return
        if state in states:
            self._state = state
        else:
            self._state = states.normal

    @property
    def spot(self):
        """Graphical representation of trap.
        """
        size = np.clip(10. + self.r.z()/10., 5., 20.)
        return {'pos': self._r.toPointF(),
                'size': size,
                'pen': self.pen,
                'brush': self.brush[self._state],
                'symbol': self.symbol}

    @property
    def properties(self):
        """Physical properties of trap.
        """
        return {'r': self._r,
                'a': self.a,
                'phi': self.phi}
