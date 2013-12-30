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
        #self.test_gradient()

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

    def magnetic(self, point):
        u"""
        Swaps point with point on border and central figure if within a certain threshold.
        """
        return point

    def ink(self, outline, brush_size=10, brush_type='pig-hair'):
        u"""
        TODO: should stroke the outline with an ink pattern brush.
        """
        pass

    def micron(self, nib_size=10, color='black'):
        u"""
        TODO: should stroke the outline with a Micron pattern brush.
        """
        pass

    def test_gradient(self):
        rgba0 = (1, 0.5, 0.0, 1)
        rgba1 = (0.2, 0.7, 0.7, 0.5, 0.5)
        rgba2 = (0.8, 1, 0.3, 0.7, 0.6)
        rgbas = [rgba1, rgba2]
        gradient = self.gradient(rgba0, rgbas)
        self.context.rectangle(0, 0, 100, 100)
        self.context.set_source(gradient)
        self.context.fill()

    '''
    def save(self):
        print 'Saving %s' % self.path
        self.context.save()
    '''
