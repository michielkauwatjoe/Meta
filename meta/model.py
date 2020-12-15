#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://github.com/michielkauwatjoe/Meta

from document import Document

class Model(object):

    def __init__(self):
        self.path = None

    def newDocument(self):
        pass

    def openDocument(self, path):
        self.path = path

        with open(path) as infile:
            return json.load(infile)

    def closeDocument(self, documentId, save=False):
        # TODO: build j dict.

        with open(self.path, 'w') as outfile:
            json.dump(j, outfile)

