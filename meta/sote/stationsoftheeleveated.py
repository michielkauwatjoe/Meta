#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# https://github.com/michielkauwatjoe/Meta

from meta.giclee import Giclee
from circus.toolbox.voronoi import Voronoi

class StationsOfTheElevated(Giclee):

    def __init__(self):
        super(StationsOfTheElevated, self).__init__(name='stations-of-the-elevated')
        self.coordinates = self.loadCoordinates()
        # Place pattern points around it.

    def loadCoordinates(self):
        # Load SVG.
        pass

if __name__ == "__main__":
    sote = StationsOfTheElevated()
    sote.save()