#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# https://github.com/michielkauwatjoe/Meta

from meta.giclee import Giclee
from circus.toolbox.generative.qhull import QHull
import numpy.random
import numpy
import math

class StationsOfTheElevated(Giclee):

    def __init__(self):
        super(StationsOfTheElevated, self).__init__(name='stations-of-the-elevated')
        self.layers = [1.2, 0.95, 0.8, 0.75, 0.7, 0.66, 0.5, 0.2, 0.22, 0.23, 0.15, 0.1]
        self.number_of_layers = len(self.layers) # TODO
        number_of_points = 144
        dimension = 2
        self.points = self.loadPoints(number_of_points, dimension)
        self.qhull = QHull()
        voronoi = self.qhull.voronoi(self.points)
        self.drawLines(voronoi)
        self.drawPoints()
        self.drawText()

    def drawText(self):
        u"""
        TODO: draw central text.
        """
        pass

    def drawLines(self, voronoi):
        u"""
        Draws edges between Voronoi facets.
        """
        points = voronoi.points
        avg = numpy.average(points, 0)
        vertices = voronoi.vertices

        for nn, vind in voronoi.ridges.items():
            (i1, i2) = sorted(vind)

            if i1 == 0:
                c1 = numpy.array(vertices[i2])
                midpt = 0.5 * (numpy.array(points[nn[0]]) + numpy.array(points[nn[1]]))
                if numpy.dot(avg - midpt, c1 - midpt) > 0:
                    c2 = c1 + 10 * (midpt - c1)
                else:
                    c2 = c1 - 10 * (midpt - c1)
            else:
                c1 = vertices[i1]
                c2 = vertices[i2]

            n1 = c1
            n2 = c2

            self.context.set_source_rgb(0.8, 1, 0)
            self.context.set_line_width(0.3)
            self.context.move_to(n1[0], n1[1])
            self.context.line_to(n2[0], n2[1])
            self.context.stroke()

    def drawPoints(self):
        u"""
        Draws points as dots with slightly randomized circles around them.
        """
        self.context.set_source_rgb(0.8, 0.8, 0.2)
        self.context.set_line_width(0.1)

        for point in self.points:
            n1, n2 = point
            self.context.arc(n1, n2, math.sqrt(2), -1 * math.pi, 1 * math.pi)
            self.context.fill()

            self.context.arc(n1 + numpy.random.rand(), n2 + numpy.random.rand(), 2* math.sqrt(2), -2 * math.pi, 2 * math.pi)
            self.context.stroke()

    def loadPoints(self, number_of_points, dimension):
        return self.getCirclePoints(number_of_points)
        #return self.getRandomPoints(number_of_points, dimension)

    def getCirclePoints(self, number_of_points):
        u"""
        Divides points on circles between r ≈ 1 and slightly above 0. Number of points decrease for each circle. Also
        some randomness is added for each point to get less symmetric voronoi edges.
        """
        points = []
        fx = self.width / 2.0
        fy = self.height / 2.0

        for r in self.layers:
        #for r in range(self.layers):
            da = 360.0 / number_of_points
            for j in range(number_of_points):
                a = j * da
                radians = math.radians(a)
                x = r * math.cos(radians) * fx + fx + numpy.random.rand()
                y = r * math.sin(radians) * fy + fy + numpy.random.rand()
                points.append((x, y))
            number_of_points -= 12
        return points

    def getRandomPoints(self, number_of_points, dimension):
        #TODO: normalize.
        return numpy.random.randn(number_of_points, dimension)

if __name__ == "__main__":
    sote = StationsOfTheElevated()
    print sote.path