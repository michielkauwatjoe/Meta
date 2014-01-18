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

    def linearGradient(self, box, rgba1, rgba2):
        u"""
        Wraps pyCairo linear gradient.
        """
        gradient = cairo.LinearGradient(box[0], box[1], box[2], box[3])
        gradient.add_color_stop_rgb(rgba1[0], rgba1[1], rgba1[2], rgba1[3])
        gradient.add_color_stop_rgb(rgba2[0], rgba2[1], rgba2[2], rgba2[3])
        return gradient

    def radialGradient(self, box):
        u"""
        Wraps pyCairo radial gradient.
        """
        cx = box[2] / 2
        cy = box[3] / 2
        gradient = cairo.RadialGradient(cx, cy, cx / 2, cx, cy, cx + cx / 2)
        gradient.add_color_stop_rgba(0.5, 0, 0, 0, 0)
        gradient.add_color_stop_rgba(0, 0, 0, 0, 1)
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
