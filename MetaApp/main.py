# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Meta appication.
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.mijksenaar.com
#
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    main.py
#

# PyObjC application startup.
from PyObjCTools import AppHelper

# Adds Twisted server. Using specialized reactor for integrating with arbitrary
# foreign event loop, such as those you find in GUI toolkits.
from twisted.internet._threadedselect import install
reactor = install()

# We need to import all classes used in nib files before running the
# application.
import delegate
#import Print

import objc; objc.setVerbose(True)

AppHelper.runEventLoop()
