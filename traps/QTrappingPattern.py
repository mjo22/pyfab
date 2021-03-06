#!/usr/bin/env python

"""QTrappingPattern.py: Interface between QFabScreen and QSLM."""

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from QTrap import QTrap
from QTrapGroup import QTrapGroup
from states import states


class QTrappingPattern(QTrapGroup):
    """Interface between fabscreen GUI and CGH pipeline.
    Implements logic for manipulating traps.
    """

    trapAdded = QtCore.pyqtSignal(QTrap)

    def __init__(self, fabscreen, parent=None):
        super(QTrappingPattern, self).__init__()
        self.fabscreen = fabscreen
        self.parent = parent
        self.pipeline = None
        # Connect to signals coming from fabscreen (QFabGraphicsView)
        self.fabscreen.sigMousePress.connect(self.mousePress)
        self.fabscreen.sigMouseMove.connect(self.mouseMove)
        self.fabscreen.sigMouseRelease.connect(self.mouseRelease)
        self.fabscreen.sigWheel.connect(self.wheel)
        # Rubberband selection
        self.selection = QtGui.QRubberBand(
            QtGui.QRubberBand.Rectangle, self.fabscreen)
        self.origin = QtCore.QPoint()
        # selected trap and group
        self.trap = None
        self.group = None
        self.selected = []

    def updateScreen(self):
        """Provide a list of "spots" to QFabScreen.
        """
        traps = self.flatten()
        spots = []
        for trap in traps:
            spots.append(trap.spot)
        self.fabscreen.setData(spots=spots)

    def update(self):
        """Provide a list of "properties" to CGH.
        This will be called by children in response to changes in properties,
        which can be triggered by mouse events, interaction with property
        widgets, or direct programmatic control of traps or groups.
        """
        if self.pipeline is None:
            return
        traps = self.flatten()
        properties = []
        spots = []
        for trap in traps:
            properties.append(trap.properties)
            spots.append(trap.spot)
        self.pipeline.setData(properties)
        self.fabscreen.setData(spots=spots)

    def dataCoords(self, coords):
        return self.fabscreen.traps.mapFromScene(coords)

    def clickedTrap(self, position):
        """Return the trap at the specified position
        """
        trap = None
        points = self.fabscreen.traps.pointsAt(position)
        if len(points) > 0:
            index = self.fabscreen.traps.points().tolist().index(points[0])
            trap = self.flatten()[index]
        return trap

    def groupOf(self, child):
        """Return the highest-level group containing the specified object.
        """
        if not isinstance(child, QTrap):
            return None
        while child.parent.parent is not None:
            child = child.parent
        return child

    def clickedGroup(self, position):
        """Return the highest-level group containing the trap at
        the specified position.
        """
        return self.groupOf(self.clickedTrap(position))

    def selectedTraps(self, region):
        """Return a list of traps whose groups fall
        entirely within the selection region.
        """
        rect = self.dataCoords(QtCore.QRectF(region)).boundingRect()
        for child in self.children:
            if child.isWithin(rect):
                self.selected.append(child)
                child.state = states.grouping
            else:
                child.state = states.normal
        if len(self.selected) <= 1:
            self.selected = []
        self.updateScreen()

    def createGroup(self):
        """Combine selected objects into new group.
        """
        group = QTrapGroup()
        for trap in self.selected:
            trap.parent.remove(trap)
            group.add(trap)
        if group.count() > 0:
            self.add(group)
        self.selected = []

    def moveGroup(self, pos):
        """Move the selected group so that the selected
        trap is at the specified position.
        """
        position = self.dataCoords(pos)
        dr = QtGui.QVector3D(position.x() - self.trap.r.x(),
                             position.y() - self.trap.r.y(),
                             0.)
        self.group.moveBy(dr)

    def breakGroup(self):
        """Break group into children and
        place children in the top level.
        """
        if isinstance(self.group, QTrapGroup):
            for child in self.group.children:
                child.state = states.grouping
                self.group.remove(child)
                self.add(child)

    def leftPress(self, pos, modifiers):
        """Selection and grouping.
        """
        position = self.dataCoords(pos)
        self.trap = self.clickedTrap(position)
        self.group = self.groupOf(self.trap)
        # update selection rectangle
        if self.group is None:
            self.origin = QtCore.QPoint(pos)
            rect = QtCore.QRect(self.origin, QtCore.QSize())
            self.selection.setGeometry(rect)
            self.selection.show()
        # break selected group
        elif modifiers == Qt.ControlModifier:
            self.breakGroup()
        # select group
        else:
            self.group.state = states.selected
        self.updateScreen()

    def rightPress(self, pos, modifiers):
        """Creation and destruction.
        """
        position = self.dataCoords(pos)
        # Add trap
        if modifiers == Qt.ShiftModifier:
            trap = QTrap(r=position, parent=self)
            self.add(trap)
            self.trapAdded.emit(trap)
            self.update()
        # Delete trap
        elif modifiers == Qt.ControlModifier:
            self.remove(self.clickedGroup(position), delete=True)
            self.update()
        else:
            pass

    @QtCore.pyqtSlot(QtGui.QMouseEvent)
    def mousePress(self, event):
        """Event handler for mousePress events.
        """
        button = event.button()
        pos = event.pos()
        modifiers = event.modifiers()
        if button == Qt.LeftButton:
            self.leftPress(pos, modifiers)
        elif button == Qt.RightButton:
            self.rightPress(pos, modifiers)
        else:
            pass

    @QtCore.pyqtSlot(QtGui.QMouseEvent)
    def mouseMove(self, event):
        """Event handler for mouseMove events.
        """
        pos = event.pos()
        # buttons = event.buttons()
        # Move traps
        if self.group is not None:
            self.moveGroup(pos)
        # Update selection box
        elif self.selection.isVisible():
            region = QtCore.QRect(self.origin, QtCore.QPoint(pos)).normalized()
            self.selection.setGeometry(region)
            self.selectedTraps(region)

    @QtCore.pyqtSlot(QtGui.QMouseEvent)
    def mouseRelease(self, event):
        """Event handler for mouseRelease events.
        """
        self.createGroup()
        for child in self.children:
            child.state = states.normal
        self.trap = None
        self.group = None
        self.selection.hide()
        self.updateScreen()

    @QtCore.pyqtSlot(QtGui.QWheelEvent)
    def wheel(self, event):
        """Event handler for mouse wheel events.
        """
        pos = event.pos()
        position = self.dataCoords(pos)
        self.trap = self.clickedTrap(position)
        self.group = self.groupOf(self.trap)
        if self.group is not None:
            self.group.state = states.selected
            dr = QtGui.QVector3D(0., 0., event.delta() / 120.)
            self.group.moveBy(dr)
