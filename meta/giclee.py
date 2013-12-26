#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# https://github.com/michielkauwatjoe/Meta

import Image
from sizes import Sizes

class Giclee(Sizes):
    u"""
    Base class for the Giclée print canvas.
    """

    def __init__(self, name='test', format='png', folder='/tmp', size='A2', colorspace='RGB', background='white'):
        u"""
        Sets up a Python Imaging Library canvas.
        """
        self.name = name
        self.format = format
        self.folder = folder
        self.colorspace = colorspace
        self.background = background
        super(Giclee, self).__init__()
        self.size_mm = self.getMmSize(size)
        self.canvas = Image.new(colorspace, size_mm, background)

    def grid(self, nx, ny, stroke='1px solid black'):
        u"""
        Draws an auxiliary grid. Should be useful for for example taxi cab Voronoi tessellation.
        """
        pass

    def save(self):
        path = folder + '/', name + '.'
        self.canvas.save(path, format)