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
        self.canvas = Image()