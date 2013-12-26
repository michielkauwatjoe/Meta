#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# https://github.com/michielkauwatjoe/Meta

import Image
import ImageDraw
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
        self.path = self.folder + '/' + self.name + '.' + self.format
        self.colorspace = colorspace
        self.background = background
        super(Giclee, self).__init__()
        self.size_mm = self.getMmSize(size)
        self.canvas = Image.new(self.colorspace, self.size_mm, self.background)
        self.draw = ImageDraw.Draw(self.canvas)

    def grid(self, nx, ny, stroke='1px solid black'):
        u"""
        Draws an auxiliary grid. Should be useful for for example taxi cab Voronoi tessellation.
        """
        pass

    def make_bezier(self, xys):
        u"""
        xys should be a sequence of 2-tuples (Bezier control points).
        """
        n = len(xys)
        combinations = self.pascal_row(n-1)

        def bezier(ts):
            u"""
            This uses the generalized formula for Bezier curves
            http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
            """
            result = []
            for t in ts:
                tpowers = (t**i for i in range(n))
                upowers = reversed([(1-t)**i for i in range(n)])
                coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
                result.append(
                    tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
            return result
        return bezier
    
    def pascal_row(self, n):
        u"""
        This returns the nth row of Pascal's Triangle.
        """
        result = [1]
        x, numerator = 1, n

        for denominator in range(1, n//2+1):
            # print(numerator, denominator, x)
            x *= numerator
            x /= denominator
            result.append(x)
            numerator -= 1
            
        if n&1 == 0:
            # n is even
            result.extend(reversed(result[:-1]))
        else:
            result.extend(reversed(result)) 
        return result

    def demo_heart(self):
        ts = [t/100.0 for t in range(101)]
        xys = [(50, 100), (80, 80), (100, 50)]
        bezier = self.make_bezier(xys)
        points = bezier(ts)
        xys = [(100, 50), (100, 0), (50, 0), (50, 35)]
        bezier = self.make_bezier(xys)
        points.extend(bezier(ts))
        
        xys = [(50, 35), (50, 0), (0, 0), (0, 50)]
        bezier = self.make_bezier(xys)
        points.extend(bezier(ts))
        
        xys = [(0, 50), (20, 80), (50, 100)]
        bezier = self.make_bezier(xys)
        points.extend(bezier(ts))
        self.draw.polygon(points, fill='red')

    def save(self):
        self.demo_heart()
        print 'Saving %s' % self.path
        self.canvas.save(self.path)
