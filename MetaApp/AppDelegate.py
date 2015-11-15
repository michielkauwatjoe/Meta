# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Meta appication.
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.mijksenaar.com
#
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    AppDelegate.py
#

# General Python libraries.

import os, os.path
import unirest

# Objective-C.

from AppKit import NSObject, NSBundle, NSImage, NSSegmentStyleSmallSquare, \
    NSSegmentedControl, NSSegmentSwitchTrackingSelectOne, NSCursor, NSPoint
from Quartz import CGColorSpaceCreateWithName, kCGColorSpaceGenericRGB,\
    CGColorCreate, CGImageGetWidth, CGImageGetHeight
from CoreText import CTFontCreateWithName
from PyObjCTools import AppHelper
import objc

# GUI wrappers.

from vanilla import Window, List, TextBox, EditText, PopUpButton, RadioGroup, SegmentedButton, \
    Button, ScrollView, Group, CheckBox, ImageView, SearchBox

from defconAppKit.windows.progressWindow import ProgressWindow

# Model & web.

import meta
from meta.model import Model

# Application object.

'''
from KeysAndMouse import MetaKeysAndMouse
from Drawing import MetaDrawing
from Canvas import MetaCanvas
from Clicked import MetaClicked
from Marquee import MetaMarquee
from Aux import MetaAuxiliary
from Dialogs import MetaDialogs
'''

class MetaAppDelegate(NSObject):
    u"""
    Main delegate for Meta application. Passed as delegate to CanvasView,
    so controls and drawing are all done inside this object.
    """

    # Main global objects.

    model = None
    projectWindows = {}

    # Dialogs.

    dialogSize = (400, 300)
    saveDialogSize = (400, 100)

    startDialog = None
    newProjectDialog = None
    saveProjectDialog = None

    # Default values.

    defaultWidth = '29.7'
    defaultHeight = '21.0'
    defaultName = 'Untitled'

    # Initial dialog values.

    projectValues = {}

    # Active project & window.

    currentProject = None

    # Units & measures. TODO: move to project.

    width = None
    height = None
    zoomFactor = 1.33
    zoomLevel = 1

    def applicationDidFinishLaunching_(self, notification):
        u"""
        Setting up globals.
        """
        print '* Meta Application finished launching, initializing...'
        self.model = Model()
        self.path = os.path.join(os.path.dirname(__file__))
        self.resourcePath = NSBundle.mainBundle().resourcePath()
        self.projectFilesPath = self.resourcePath + '/en.lproj/'
        self.openStartWindow()

    def applicationShouldTerminate_(self, sender):
        if reactor.running:
            reactor.addSystemEventTrigger('after', 'shutdown', AppHelper.stopEventLoop)
            reactor.stop()
            return False
        return True

    # Interface Builder actions and dialogs.

    def openProjectWindow(self, project):
        u"""
        Controls and canvas view for a project.
        """
        self.windowSize = (project.width, project.height)
        w = Window(self.windowSize, minSize=(1, 1), maxSize=self.windowSize, closable=False)
        self.setCanvas(w, project)
        self.setStatusBar(w, project)
        w.bind("should close", self.windowShouldCloseCallback)
        w.bind("close", self.windowCloseCallback)
        w.open()
        return w

    def setToolBar(self, w):
        tools = self.getTools()
        w.addToolbar("Toolbar", toolbarItems=tools)
        w.getNSWindow().toolbar().setSelectedItemIdentifier_("arrow")

    def setCanvas(self, w, project):
        u"""
        Scalable and resizable drawing canvas.
        """
        w.canvas = MetaCanvas((0, 30, -230, -20), delegate=self, canvasSize=self.windowSize, width=project.width, height=project.height)
        w.canvas.getNSSubView().scaleUnitSquareToSize_((1.0, 1.0))

    def setStatusBar(self, w, project):
        u"""
        Sets up status bar at the bottom.
        """
        w.popUpButton = PopUpButton((0, -20, 150, 18), ["Display...", "Flow Control Points", "Flow Labels"], callback=self.popUpButtonCallback)
        w.popUpButton.getNSPopUpButton().setPullsDown_(True)
        w.projectNameLabel = TextBox((154, -18, 100, 18), 'Project:', sizeStyle='small')
        w.projectNameText = TextBox((204, -18, 150, 18), project.name, sizeStyle='small')
        w.projectPathLabel = TextBox((354, -18, 100, 18), 'Path:', sizeStyle='small')
        w.projectPathText = TextBox((404, -18, 400, 18), project.path, sizeStyle='small')

    def windowCloseCallback(self, sender):
        u"""
        TODO: implement.
        """
        print 'close'

    # IBActions.

    @objc.IBAction
    def openProject_(self, sender):
        self.openOpenProjectDialog()

    @objc.IBAction
    def newProject_(self, sender):
        if self.newProjectDialog is None:
            self.openNewProjectDialog()

    @objc.IBAction
    def importDestinations_(self, sender):
        u"""
        """
        pass

    @objc.IBAction
    def zoomIn_(self, sender):
        u"""Increases scale unit, canvas size."""
        window = self.getCurrentWindow()
        project = self.currentProject
        z = 1 * self.zoomFactor
        window.canvas.zoom(z)
        window.canvas.update()

    @objc.IBAction
    def zoomOut_(self, sender):
        u"""Decreases scale unit, canvas size."""
        window = self.getCurrentWindow()
        project = self.currentProject
        z = 1 / self.zoomFactor
        window.canvas.zoom(z)
        window.canvas.update()

    @objc.IBAction
    def closeProject_(self, sender):
        if not self.currentProject is None and self.currentProject.isDirty():
            self.openSaveProjectDialog()
        else:
            self.closeProject()
            self.closeSaveProjectDialog()

    @objc.IBAction
    def selectAll_(self, sender):
        window = self.getCurrentWindow()
        floor = self.getFloor()
        floor.selectAll()
        window.canvas.update()

    def closeProject(self, save=False):
        self.model.closeProject(self.currentProject.pid, save=save)
        self.projectWindows[self.currentProject.pid].close()

    def closeSaveProjectDialog(self):
        self.saveProjectDialog.close()
        self.saveProjectDialog = None

    @objc.IBAction
    def saveProject_(self, sender):
        self.model.saveProject(self.currentProject.pid)

    @objc.IBAction
    def saveProjectAs_(self, sender):
        self.model.saveProjectAs(self.currentProject.pid)

    @objc.IBAction
    def undo_(self, sender):
        self.currentProject.undo()
        self.setCurrentObjects()
        self.update()

    @objc.IBAction
    def redo_(self, sender):
        self.currentProject.redo()
        self.setCurrentObjects()
        self.update()

    # Project.

    def initProject(self, added, project):
        u"""
        """
        #progressWindow = ProgressWindow()

        if not added:
            print 'Project %s, already open' % project.pid
        else:
            self.currentProject = project
            window = self.openProjectWindow(project)
            self.projectWindows[project.pid] = window
            self.redrawCanvas = True
            window.canvas.update(source='initProject')

        #progressWindow.close()

    # Main view update logic.

    def update(self):
        u"""
        Main view update logic, to be called when window is not yet known.
        """
        window = self.getCurrentWindow()

        if not window is None:
            window.canvas.update(source='main update')
