#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://github.com/michielkauwatjoe/Meta


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
