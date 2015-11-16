# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Meta appication.
#    Copyright (c) 2014+ www.michielkauwatjoe.com
#
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    delegate.py
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
from keysandmouse import KeysAndMouse
from drawing import Drawing
from clicked import Clicked
from marquee import Marquee
'''
from paper import Paper
from dialogs import Dialogs
from aux import Auxiliary
from callbacks import Callbacks

class Delegate(NSObject, Dialogs, Paper, Auxiliary, Callbacks):
    u"""
    Main delegate for Meta application. Passed as delegate to Paper view,
    so controls and drawing are all done inside this object.
    """

    # Main global objects.

    model = None
    windows = {}

    # Dialogs.

    dialogSize = (400, 300)
    saveDialogSize = (400, 100)

    startDialog = None
    openDialog = None
    newDialog = None
    saveDialog = None

    # Default values.

    defaultDocumentName = 'Untitled'
    defaultPaperSize = 'A3'

    documentValues = {} # Initial document values.
    currentDocument = None # Active document.

    # Units & measures. TODO: move to document.

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
        self.documentFilesPath = self.resourcePath + '/en.lproj/'
        self.openStartWindow()

    def applicationShouldTerminate_(self, sender):
        return True

    # Interface Builder actions and dialogs.

    def openWindow(self, document):
        u"""
        Controls and paper view for a document.
        """
        self.windowSize = (document.width, document.height)
        w = Window(self.windowSize, minSize=(1, 1), maxSize=self.windowSize, closable=False)
        self.setPaper(w, document)
        self.setStatusBar(w, document)
        w.bind("should close", self.windowShouldCloseCallback)
        w.bind("close", self.windowCloseCallback)
        w.open()
        return w

    def setToolBar(self, w):
        tools = self.getTools()
        w.addToolbar("Toolbar", toolbarItems=tools)
        w.getNSWindow().toolbar().setSelectedItemIdentifier_("arrow")

    def setPaper(self, w, document):
        u"""
        Scalable and resizable drawing paper.
        """
        w.paper = MetaPaper((0, 30, -230, -20), delegate=self, paperSize=self.windowSize, width=document.width, height=document.height)
        w.paper.getNSSubView().scaleUnitSquareToSize_((1.0, 1.0))

    def setStatusBar(self, w, document):
        u"""
        Sets up status bar at the bottom.
        """
        w.popUpButton = PopUpButton((0, -20, 150, 18), ["Display...", "Flow Control Points", "Flow Labels"], callback=self.popUpButtonCallback)
        w.popUpButton.getNSPopUpButton().setPullsDown_(True)
        w.documentNameLabel = TextBox((154, -18, 100, 18), 'Document:', sizeStyle='small')
        w.documentNameText = TextBox((204, -18, 150, 18), document.name, sizeStyle='small')
        w.documentPathLabel = TextBox((354, -18, 100, 18), 'Path:', sizeStyle='small')
        w.documentPathText = TextBox((404, -18, 400, 18), document.path, sizeStyle='small')

    def windowCloseCallback(self, sender):
        u"""
        TODO: implement.
        """
        print 'close'

    # IBActions.

    @objc.IBAction
    def open_(self, sender):
        self.openOpenDocumentDialog()

    @objc.IBAction
    def new_(self, sender):
        if self.newDialog is None:
            self.openNewDialog()

    @objc.IBAction
    def zoomIn_(self, sender):
        u"""Increases scale unit, paper size."""
        window = self.getCurrentWindow()
        document = self.currentDocument
        z = 1 * self.zoomFactor
        window.paper.zoom(z)
        window.paper.update()

    @objc.IBAction
    def zoomOut_(self, sender):
        u"""Decreases scale unit, paper size."""
        window = self.getCurrentWindow()
        document = self.currentDocument
        z = 1 / self.zoomFactor
        window.paper.zoom(z)
        window.paper.update()

    @objc.IBAction
    def close_(self, sender):
        if not self.currentDocument is None and self.currentDocument.isDirty():
            self.openSaveDialog()
        else:
            self.closeDocument()
            self.closeSaveDialog()

    @objc.IBAction
    def selectAll_(self, sender):
        window = self.getCurrentWindow()
        floor = self.getFloor()
        floor.selectAll()
        window.paper.update()

    @objc.IBAction
    def save_(self, sender):
        self.model.saveDocument(self.currentDocument.pid)

    @objc.IBAction
    def saveAs_(self, sender):
        self.model.saveDocumentAs(self.currentDocument.pid)

    @objc.IBAction
    def undo_(self, sender):
        self.currentDocument.undo()
        self.setCurrentObjects()
        self.update()

    @objc.IBAction
    def redo_(self, sender):
        self.currentDocument.redo()
        self.setCurrentObjects()
        self.update()

    # Document.

    def closeDocument(self, save=False):
        self.model.closeDocument(self.currentDocument.pid, save=save)
        self.windows[self.currentDocument.pid].close()

    def initDocument(self, added, document):
        u"""
        """
        progressWindow = ProgressWindow()

        if not added:
            print 'Document %s, already open' % document.pid
        else:
            self.currentDocument = document
            window = self.openWindow(document)
            self.windows[document.pid] = window
            self.redrawPaper = True
            window.paper.update()

        progressWindow.close()

    # Main view update logic.

    def update(self):
        u"""
        Main view update logic, to be called when window is not yet known.
        """
        window = self.getCurrentWindow()

        if not window is None:
            window.paper.update()
