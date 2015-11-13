#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://github.com/michielkauwatjoe/Meta

class CurvePoint(object)
    u"""
    A point to be used in a cubic Bézier curve.
    """

    def __init__(self, x, y, onCurve=True):
        self.x = x
        self.y = y
        self.onCurve = onCurve
