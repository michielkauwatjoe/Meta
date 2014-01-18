#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://github.com/michielkauwatjoe/Meta

from meta.giclee import Giclee
from circus.toolbox.generative.quickhull import QuickHull
import numpy.random
import numpy
import math
import cairo
import datetime
from lxml import etree

class StationsOfTheElevated(Giclee):

    def __init__(self):
        name = self.getName()
        super(StationsOfTheElevated, self).__init__(name=name)
        self.layers = [1.2, 0.95, 0.8, 0.75, 0.7, 0.66, 0.5, 0.43, 0.2, 0.22, 0.23, 0.15, 0.1]
        self.number_of_layers = len(self.layers)
        self.decrease = 5
        number_of_points = self.number_of_layers * self.decrease
        dimension = 2
        path_figure = '/Users/michiel/Designs/2012-12 - Stations of the Elevated/stations-of-the-elevated.svg'

        '''Gets point set. This will be the same as voronoi.points as returned by the Qhull object.'''
        self.points = self.loadPoints(number_of_points, dimension)
        self.qhull = QuickHull()
        voronoi = self.qhull.voronoi(self.points)
        # facets = self.drawEdges(voronoi)
        # self.drawPoints(numbers=False)
        # self.drawFigure(path_figure)
        # self.sortEdges(voronoi)
        self.drawGradients()

    def drawGradients(self):
        rgba0 = (0, 0, 1, 1)
        rgba1 = (0, 0, 0.3, 0.8, 1)
        rgba2 = (1, 0, 0.8, 0.3, 1)
        rgbas = [rgba1, rgba2]
        gradient = self.gradient(rgba0, rgbas)
        self.context.rectangle(0, 0, self.width, self.height)
        self.context.set_source(gradient)
        self.context.fill()

    def getName(self):
        now = str(datetime.datetime.now())[:19]
        now = now.replace(' ', '_')
        now = now.replace(':', '.')
        return 'stations-of-the-elevated_' + now

    def drawFigure(self, path):
        u"""
        TODO: draw central text.
        """
        svg = self.loadSVG(path)
        self.drawSVG(svg)

    def sortEdges(self, voronoi):
        for point_indices, vertex_index in voronoi.ridges.items():
            print point_indices, vertex_index

    def drawEdges(self, voronoi):
        u"""
        Draws edges between Voronoi facets. From http://www.physics.nyu.edu/grierlab/idl_html_help/Q2.html:

        For two-dimensional arrays, VDIAGRAM is a 4-by-nv integer array. For each Voronoi ridge, i, VDIAGRAM[0:1, i]
        contains the index of the two input points the ridge bisects. VDIAGRAM [2:3, i] contains the indices within
        VVERTICES of the Voronoi vertices. In the case of an unbounded half-space, VDIAGRAM[2, i] is set to a negative
        index, j, indicating that the corresponding Voronoi ridge is unbounded, and that the equation for the ridge is
        contained in VNORMAL[*, -j-1], and starts at Voronoi vertex [3, i].

        For three-dimensional or higher dimensional arrays, VDIAGRAM is returned as a connectivity vector. This vector
        has the form [n, v0, v1, i0, i1, ..., in-3], where n is the number of points needed to describe that particular
        Voronoi ridge, v0 and v1 contain the indices for the two input points that the ridge bisects, and i0...in -3
        contain the indices within VVERTICES of the Voronoi vertices. In the case of an unbounded half-space,
        VDIAGRAM[i] is set to a negative index, j, indicating that the corresponding Voronoi ridge is unbounded, and
        that the equation for the ridge is contained in VNORMAL[*, -j-1].

        TODO: sort edges for each facet and return in indexed list.
        """
        avg = numpy.average(voronoi.points, 0)
        vertices = voronoi.vertices
        self.context.set_source_rgb(0.8, 0.14, 0)
        self.context.set_line_width(0.3)
        i = 1

        edges = []

        for point_indices, vertex_index in voronoi.ridges.items():
            (i1, i2) = sorted(vertex_index)

            if i1 == 0:
                # Infinite edge?
                c1 = numpy.array(vertices[i2])
                mid_point = 0.5 * (numpy.array(voronoi.points[point_indices[0]]) + numpy.array(voronoi.points[point_indices[1]]))

                if numpy.dot(avg - mid_point, c1 - mid_point) > 0:
                    c2 = c1 + 10 * (mid_point - c1)
                else:
                    c2 = c1 - 10 * (mid_point - c1)
            else:
                c1 = vertices[i1]
                c2 = vertices[i2]

            edges.append((c1, c2))
            self.context.move_to(c1[0], c1[1])
            self.context.line_to(c2[0], c2[1])
            self.context.stroke()

        return edges

    def drawPoints(self, numbers=True):
        u"""
        Draws points as dots with slightly randomized circles around them.
        """
        self.context.set_source_rgb(0.8, 0.8, 0.2)
        self.context.set_line_width(0.1)
        i = 1
        self.context.select_font_face("Gill Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        self.context.set_font_size(4)

        for point in self.points:
            n1, n2 = point
            self.context.arc(n1, n2, math.sqrt(2), -1 * math.pi, 1 * math.pi)
            self.context.fill()

            self.context.arc(n1 + numpy.random.rand(), n2 + numpy.random.rand(), 2 * math.sqrt(2), -2 * math.pi, 2 * math.pi)
            self.context.stroke()

            if numbers:
                self.context.move_to(n1 + 3, n2 + 3)
                self.context.show_text(str(i))
            i += 1

    def loadPoints(self, number_of_points, dimension):
        return self.getCirclePoints(number_of_points)
        # return self.getRandomPoints(number_of_points, dimension)

    def getCirclePoints(self, number_of_points):
        u"""
        Divides points on circles between r ��� 1 and slightly above 0. Number of points decrease for each circle. Also
        some randomness is added for each point to get less symmetric voronoi edges.
        """
        points = []
        fx = self.width / 2.0
        fy = self.height / 2.0

        for r in self.layers:
        # for r in range(self.layers):
            da = 360.0 / number_of_points
            for j in range(number_of_points):
                a = j * da
                radians = math.radians(a)
                x = r * math.cos(radians) * fx + fx + numpy.random.rand()
                y = r * math.sin(radians) * fy + fy + numpy.random.rand()
                points.append((x, y))
            number_of_points -= self.decrease
        return points

    def getRandomPoints(self, number_of_points, dimension):
        # TODO: normalize.
        return numpy.random.randn(number_of_points, dimension)

if __name__ == "__main__":
    sote = StationsOfTheElevated()
    print sote.path
