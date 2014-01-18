#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://github.com/michielkauwatjoe/Meta

import cairo
from sizes import Sizes
from configuration.configuration import Configuration
from svg import SVG
from strokes import Strokes
from reportlab.graphics.renderSVG import SVGCanvas

class Giclee(Sizes, SVG, Strokes, Configuration):
    u"""
    Base class for the Giclée print canvas.
    """

    def __init__(self, name='test', folder='/Users/michiel/Downloads/', size='A2', colorspace='RGB', background='white',
                 border_points=[]):
        u"""
        Sets up a Python Imaging Library canvas.
        """
        self.name = name
        self.folder = folder
        self.path = self.folder + self.name + '.svg'
        self.colorspace = colorspace
        self.background = background
        self.border_points = border_points
        super(Giclee, self).__init__()
        self.width, self.height = self.getMmSize(size)
        self.surface = cairo.SVGSurface(self.path, self.width, self.height)
        self.context = cairo.Context(self.surface)
        self.draw_border()

    def gradient(self, rgba, rgbas):
        gradient = cairo.LinearGradient(rgba[0], rgba[1], rgba[2], rgba[3])
        for rgba in rgbas:
            gradient.add_color_stop_rgba(rgba[0], rgba[1], rgba[2], rgba[3], rgba[4])
        return gradient

    def draw_border(self):
        self.context.set_source_rgb(1, 0, 0)
        self.context.rectangle(0, 0, self.width, self.height)
        self.context.set_line_width(0.2)
        self.context.stroke()

    def grid(self, nx, ny, stroke='1px solid black'):
        u"""
        Draws an auxiliary grid. Should be useful for for example taxi cab Voronoi tessellation.
        """
        pass
