#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# https://github.com/michielkauwatjoe/Meta

from meta.giclee import Giclee
from circus.voronoi import Voronoi

class StationsOfTheElevated(Giclee):

    def __init__(self):
        self.coordinates = self.loadCoordinates()

    def loadCoordinates(self):
        pass