# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Wayfinding appication.
#    Copyright (c) 2014+ www.michielkauwatjoe.com
#
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    paper.py
#


from AppKit import NSView, NSColor, NSMakeRect, NSRectFill, NSTrackingArea, NSSize, \
        NSTrackingMouseEnteredAndExited, \
        NSTrackingActiveAlways, NSCursor, NSTrackingActiveWhenFirstResponder
from vanilla import Group, ScrollView
import objc

class PaperNSView(NSView):
    u"""
    Inherits from a normal NSView, enables all delegate, first responder, mouse
    / key event and menu functionality.
    """

    def __new__(cls, *arg, **kwargs):
        self = cls.alloc().init()
        return self

    def __init__(self, (w, h), delegate, acceptsMouseMoved):
        rect = NSMakeRect(0, 0, w, h)
        self.setFrame_(rect)
        self.setDelegate_(delegate)
        self.setAcceptsMouseMoved_(acceptsMouseMoved)

        # FIXME: hard to determine bounds, maybe bound()? Zoom / scale influenced?
        opts = NSTrackingMouseEnteredAndExited | NSTrackingActiveWhenFirstResponder
        rect = NSMakeRect(0, 30, w, h)
        trackingArea = NSTrackingArea.alloc().initWithRect_options_owner_userInfo_(rect, opts, self, None)
        self.addTrackingArea_(trackingArea)

    def setDelegate_(self, delegate):
        self._delegate = delegate

    def delegate(self):
        return self._delegate

    def setAcceptsMouseMoved_(self, value):
        self._acceptsMouseMoved = value

    def acceptsMouseMoved(self):
        return self._acceptsMouseMoved

    def acceptsFirstResponder(self):
        return True

    def sendDelegateAction_(self, method):
        delegate = self.delegate()
        if hasattr(delegate, method):
            return getattr(delegate, method)()
        return None

    def sendDelegateAction_event_(self, method, event):
        delegate = self.delegate()
        if hasattr(delegate, method):
            return getattr(delegate, method)(event)
        return None

    def drawRect_(self, rect):
        self.delegate().draw(rect)

    def becomeFirstResponder(self):
        if self._acceptsMouseMoved:
            self.window().setAcceptsMouseMovedEvents_(True)
        self.sendDelegateAction_("becomeFirstResponder")
        return True

    def resignFirstResponder(self):
        if self._acceptsMouseMoved:
            window = self.window()
            if window:
                window.setAcceptsMouseMovedEvents_(False)
        self.sendDelegateAction_("resignFirstResponder")
        return True

    #   M E N U

    def undo_(self, event):
        self.sendDelegateAction_event_("undo", event)

    def redo_(self, event):
        self.sendDelegateAction_event_("redo", event)

    def cut_(self, event):
        self.sendDelegateAction_event_("cut", event)

    def copy_(self, event):
        self.sendDelegateAction_event_("copy", event)

    def paste_(self, event):
        self.sendDelegateAction_event_("paste", event)

    def copyAsComponent_(self, event):
        self.sendDelegateAction_event_("copyAsComponent", event)

    def delete_(self, event):
        self.sendDelegateAction_event_("delete", event)

    def selectAll_(self, event):
        self.sendDelegateAction_event_("selectAll", event)

    def selectAllAlternate_(self, event):
        self.sendDelegateAction_event_("selectAllAlternate", event)

    def selectAllControl_(self, event):
        self.sendDelegateAction_event_("selectAllControl", event)

    #   E V E N T

    def mouseDown_(self, event):
        self.sendDelegateAction_event_("mouseDown", event)

    def mouseDragged_(self, event):
        self.sendDelegateAction_event_("mouseDragged", event)

    def mouseUp_(self, event):
        self.sendDelegateAction_event_("mouseUp", event)

    def mouseEntered_(self, event):
        #self.sendDelegateAction_event_("mouseEntered", event)
        #NSCursor.resizeUpDownCursor().push()
        pass

    def mouseExited_(self, event):
        #print 'exited'
        #NSCursor.arrowCursor().set()
        pass

    def mouseMoved_(self, event):
        self.sendDelegateAction_event_("mouseMoved", event)

    def rightMouseDown_(self, event):
        result = self.sendDelegateAction_event_("rightMouseDown", event)
        if not result:
            super(PaperNSView, self).rightMouseDown_(event)

    def rightMouseDragged_(self, event):
        self.sendDelegateAction_event_("rightMouseDragged", event)

    def rightMouseUp_(self, event):
        self.sendDelegateAction_event_("rightMouseUp", event)

    def keyDown_(self, event):
        self.sendDelegateAction_event_("keyDown", event)

    def keyUp_(self, event):
        self.sendDelegateAction_event_("keyUp", event)

    def flagsChanged_(self, event):
        self.sendDelegateAction_event_("flagsChanged", event)

    def menuForEvent_(self, event):
        return self.sendDelegateAction_("menu")

class Paper(Group):
    u"""
    Wraps an PaperNSView in a ScrollView. Tells which part of the paper to redraw.
    """

    def __init__(self, posSize, delegate=None, paperSize=(1000, 1000), acceptsMouseMoved=False,
                    hasHorizontalScroller=True, hasVerticalScroller=True,
                    autohidesScrollers=False, backgroundColor=None,
                    drawsBackground=True, width=200, height=1000):

        # Initializes group first.
        super(Paper, self).__init__(posSize)

        if backgroundColor is None:
            white = NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 1, 1, 1)
            backgroundColor = white

        self.paperView = PaperNSView(paperSize, delegate, acceptsMouseMoved=acceptsMouseMoved)

        self.scrollView = ScrollView((0, 0, -0, -0), self.paperView, backgroundColor=backgroundColor,
                                    hasHorizontalScroller=hasHorizontalScroller, hasVerticalScroller=hasVerticalScroller,
                                    autohidesScrollers=autohidesScrollers, drawsBackground=drawsBackground)
        self.width = width
        self.height = height

    def zoom(self, z):
        u"""
        Zooms by factor, sets new unit and updates frame size.
        """
        self.getPaperView().scaleUnitSquareToSize_((z, z))
        self.width = z * self.width
        self.height = z * self.height
        newSize = NSSize(self.width, self.height)
        self.getPaperView().setFrameSize_(newSize)

    def update(self, source=None):
        u"""
        Updates entire drawing board.
        """
        self.paperView.setNeedsDisplay_(True)

    def hide(self):
        u"""
        Hides this view.
        """
        self.getNSView().setHidden_(True)

    def show(self):
        u"""
        Shows this view.
        """
        self.getNSView().setHidden_(False)

    def updateRect(self, rect):
        u"""
        Updates only a certain rectangular area of drawing board.
        """
        x, y, w, h = rect
        self.paperView.setNeedsDisplayInRect_(((x, y), (w, h)))
        self.paperView.setNeedsDisplay_(False)

    def getPaperView(self):
        u"""
        """
        return self.paperView
