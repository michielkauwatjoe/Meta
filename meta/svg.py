#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://github.com/michielkauwatjoe/Meta

from lxml import etree

class SVG(object):

    NAMESPACE = 'http://www.w3.org/2000/svg'
    NAMESPACE_STRING = '{%s}' % NAMESPACE
    SVG_COMMANDS = ['m', 'c', 'l']

    def loadSVG(self, path):
        file = open(path, 'r')
        file_string = ''.join(file.readlines())
        return etree.fromstring(file_string)

    def drawSVG(self, svg):
        for element in svg.iter():
           tag = element.tag.replace(self.NAMESPACE_STRING, '')
           if 'd' in element.attrib:
               self.drawElementPath(element.attrib['d'])

    def drawElementPath(self, path):
        paths = path.split(' ')
        for p in paths:
            if p == '':
                continue
            print p
            subpaths = []
            subpath = p[0]

            for c in p[1:]:
                if c in self.SVG_COMMANDS or c.lower() in self.SVG_COMMANDS:
                    print subpath
                    subpaths.append(subpath)
                    subpath = c
                elif c == 'z' or c == 'Z':
                    subpaths.append(subpath)
                else:
                    subpath += c

            '''
            for s in subpaths:
                print p[0]
                points = p[1:]
                points = points.split(',')
                print points
            '''

    def drawPath(self, path):
        return
        if command == "M":
            self.context.move_to(c[0], c[1])
        elif command == "C":
            self.context.curve_to(c[0], c[1], c[2], c[3], c[4], c[5])
        elif command == "L":
            self.context.line_to(c[0], c[1])
        elif command == "Z":
            self.context.close_path();

    def magnetic(self, point):
        """Swaps point with point on border and central figure if within a
        certain threshold."""
        return point
