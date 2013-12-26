#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# https://github.com/michielkauwatjoe/Meta

from meta.giclee import Giclee
from circus.voronoi import Voronoi

class StationsOfTheElevated(Giclee):

    def __init__(self):
        super(Giclee, self).__init__(name='stations-of-the-elevated')
        self.coordinates = self.loadCoordinates()
        # Place random points around it.

    def loadCoordinates(self):
        # Load SVG.
        pass

def main():
    sote = StationsOfTheElevated()
    sote.save()