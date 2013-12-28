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
        number_of_points = 30
        dimension = 2
        self.points = self.loadPoints(number_of_points, dimension)
        self.setMinMaxDeltas()

        self.qhull = QHull()
        voronoi = self.qhull.voronoi(self.points)
        self.drawLines(voronoi)
        self.drawPoints(voronoi)
        # Place pattern points around it in rows of several ellipses.

    def normalize(self, point):
        dx = -self.min_x
        dy = -self.min_y
        nx = self.width / self.diff_x
        ny = self.height / self.diff_y
        x0 = (point[0] + dx) * nx + (numpy.random.rand() * 3)
        y0 = (point[1] + dy) * ny + (numpy.random.rand() * 3)
        return (x0, y0)
    
    def setMinMaxDeltas(self):
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None

        for point in self.points:
            if self.min_x == None or point[0] < self.min_x:
                self.min_x = point[0]
            if self.max_x == None or point[0] > self.max_x:
                self.max_x = point[0]
            if self. min_y == None or point[1] < self.min_y:
                self.min_y = point[1]
            if self.max_y == None or point[1] > self.max_y:
                self.max_y = point[1]

        self.diff_x = self.max_x - self.min_x
        self.diff_y = self.max_y - self.min_y

    def drawLines(self, voronoi):
        points = voronoi.points
        avg = numpy.average(points, 0)
        vertices = voronoi.vertices
        offset = 0.2

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

            n1 = self.normalize(c1)
            n2 = self.normalize(c2)

            self.context.set_source_rgb(0.85, 0.7, 0)
            self.context.set_line_width(0.4)
            self.context.move_to(n1[0] + offset, n1[1] + offset)
            self.context.line_to(n2[0] + offset, n2[1] + offset)
            self.context.stroke()

            self.context.set_source_rgb(0.8, 1, 0)
            self.context.set_line_width(0.3)
            self.context.move_to(n1[0], n1[1])
            self.context.line_to(n2[0], n2[1])
            self.context.stroke()

    def drawPoints(self, voronoi):

        self.context.set_source_rgb(0.8, 0.8, 0.2)
        self.context.set_line_width(0.5)

        for point in voronoi.points:
            n1, n2 = self.normalize(point)
            self.context.arc(n1, n2, math.sqrt(2), -1 * math.pi, 1 * math.pi)
            self.context.fill()
            #self.context.stroke()

        self.context.set_source_rgb(0, 1, 0)

        for vertex in voronoi.vertices:
            n1, n2 = self.normalize(vertex)
            #self.context.line_to(n1, n2)
            self.context.arc(n1, n2, math.sqrt(2), -1 * math.pi, 1 * math.pi)
            self.context.stroke()

        self.context.set_source_rgb(0, 0, 1)

        for ridge in voronoi.ridges:
            n1, n2 = self.normalize(ridge)
            self.context.arc(n1, n2, 2* math.sqrt(2), -2 * math.pi, 2 * math.pi)
            self.context.stroke()

    def loadPoints(self, number_of_points, dimension):
        return self.getCirclePoints(number_of_points)
        #return self.getRandomPoints(number_of_points, dimension)

    def getCirclePoints(self, number_of_points):
        points = []
        
        for r in range(1, 20):
            for i in range(number_of_points):
                a = i * 360.0 / number_of_points
                x = math.sqrt(r) * math.cos(a)
                y = math.sqrt(r) * math.sin(a)
                points.append((x, y))
            number_of_points = number_of_points + 5
        return points

    def getRandomPoints(self, number_of_points, dimension):
        return numpy.random.randn(number_of_points, dimension)

if __name__ == "__main__":
    sote = StationsOfTheElevated()
    sote.save()