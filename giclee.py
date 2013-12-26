#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# https://github.com/michielkauwatjoe/Meta

import Image

class Giclee:
    u"""
    Base class for the Giclée print canvas.
    """

    def __init__(self, size='A2', colorspace='RGB'):
        u"""
        Sets up a Python Imaging Library canvas.
        """
        self.canvas = Image()

    def grid(self, nx, ny, stroke='1px solid black'):
        u"""
        Draws an auxiliary grid. Should be useful for for example taxi cab Voronoi tesselation.
        """
        pass