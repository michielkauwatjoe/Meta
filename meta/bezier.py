#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://github.com/michielkauwatjoe/Meta

class Bezier:

    def __init__(self, bezierId=None, points=None, parent=None, isClosed=False):
        u"""
        Stores points in Bézier curve.
        """
        self.bezierId = bezierId
        self.points = points
        self.parent = parent
        self.isClosed = isClosed
