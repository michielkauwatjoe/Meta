# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Meta appication.
#    Copyright (c) 2014+ www.michielkauwatjoe.com
#
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    callbacks.py
#

class Callbacks(object):

    def newDocumentNameCallback(self, sender):
        pass

    def newDocumentSizeCallback(self, sender):
        pass

    def newDocumentOkayCallback(self, sender):
        self.model.new()
        self.closeOpenDocumentDialog()

    def newDocumentWidthCallback(self, sender):
        pass

    def newDocumentHeightCallback(self, sender):
        pass

    def newDocumentCancelCallback(self, sender):
        pass
