#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://github.com/michielkauwatjoe/Meta

from lxml import etree

class SVG(object):

    def loadSVG(self, path):
        file = open(path, 'r')
        file_string = ''.join(file.readlines())
        svg = etree.fromstring(file_string)
        for element in svg.iter():
            print element.tag, element.attrib

    def executeSVG(self, command, c):
        if command == "M":
            self.context.move_to(c[0], c[1])
        elif command == "C":
            self.context.curve_to(c[0], c[1], c[2], c[3], c[4], c[5])
        elif command == "L":
            self.context.line_to(c[0], c[1])
        elif command == "Z":
            self.context.close_path();

    def magnetic(self, point):
        u"""
        Swaps point with point on border and central figure if within a certain threshold.
        """
        return point
