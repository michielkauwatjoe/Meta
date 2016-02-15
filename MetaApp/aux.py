#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://github.com/michielkauwatjoe/Meta

import os
import Image

from AppKit import NSString, NSURL, NSLog
from Quartz import CGImageSourceCreateWithURL, CGImageSourceCreateImageAtIndex

from wayfinding.objects.signgroup import SignGroup
from wayfinding.objects.flow import Flow
from wayfinding.mathandlogic import MathAndLogic

class Auxiliary(object):
    u"""
    Short, application-wide auxiliary functions.
    """

    def setDefaultDocumentValues(self):
        u"""
        Resets new document dialog values to defaults.
        """
        self.documentValues = {
            'documentName': self.defaultDocumentName,
            'documentPaper': self.defaultPaperSize,
        }

