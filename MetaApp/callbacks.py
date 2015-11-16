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

    def newNameCallback(self, sender):
        pass

    def newSizeCallback(self, sender):
        pass

    def newOkayCallback(self, sender):
        self.model.new()
        self.closeOpenDialog()

    def newWidthCallback(self, sender):
        pass

    def newHeightCallback(self, sender):
        pass

    def newCancelCallback(self, sender):
        pass
