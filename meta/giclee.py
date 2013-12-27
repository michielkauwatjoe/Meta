#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# https://github.com/michielkauwatjoe/Meta

#import Image
#import ImageDraw
import cairo
from sizes import Sizes

class Giclee(Sizes):
    u"""
    Base class for the Giclée print canvas.
    """

    def __init__(self, name='test', format='png', folder='/tmp', size='A2', colorspace='RGB', background='white',
                 border_points=[]):
        u"""
        Sets up a Python Imaging Library canvas.
        """
        self.name = name
        self.format = format
        self.folder = folder
        self.path = self.folder + '/' + self.name + '.' + self.format
        self.colorspace = colorspace
        self.background = background
        self.border_points = border_points
        super(Giclee, self).__init__()
        width, height = self.getMmSize(size)
        #self.canvas = Image.new(self.colorspace, self.size_mm, self.background)
        #self.draw = ImageDraw.Draw(self.canvas)
        self.surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
        self.ctx = cairo.Context (surface)

    def grid(self, nx, ny, stroke='1px solid black'):
        u"""
        Draws an auxiliary grid. Should be useful for for example taxi cab Voronoi tessellation.
        """
        pass

    def magnetic(self, point):
        u"""
        Swaps point with point on border if within a certain threshold.
        """
        return point

    def save(self):
        print 'Saving %s' % self.path
        surface.write_to_png(self.path)
