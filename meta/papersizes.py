#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://github.com/michielkauwatjoe/Meta

class PaperSizes(object):
    u"""
    """

    # A_SERIES

    ISO_216_A = {
        'A0': {'mm': (841, 1189), 'in': (33.1, 46.8)},
        'A1': {'mm': (594, 841), 'in': (23.4, 33.1)},
        'A2': {'mm': (420, 594), 'in': (16.5, 23.4)},
        'A3': {'mm': (297, 420), 'in': (11.7, 16.5)},
        'A4': {'mm': (210, 297), 'in': (8.3, 11.7)},
        'A5': {'mm': (148, 210), 'in': (5.8, 8.3)},
        'A6': {'mm': (105, 148), 'in': (4.1, 5.8)},
        'A7': {'mm': (74, 105), 'in': (2.9, 4.1)},
        'A8': {'mm': (52, 74), 'in': (2.0, 2.9)},
        'A9': {'mm': (37, 52), 'in': (1.5, 2.0)},
        'A10': {'mm': (26, 37), 'in': (1.0, 1.5)},
    }

    # B_SERIES

    ISO_216_B = {
        'B0': {'mm': (1000, 1414), 'in': ( 39.4, 55.7)},
        'B1': {'mm': (707, 1000), 'in': ( 27.8, 39.4)},
        'B2': {'mm': (500, 707), 'in': ( 19.7, 27.8)},
        'B3': {'mm': (353, 500), 'in': (13.9, 19.7)},
        'B4': {'mm': (250, 353), 'in': (9.8, 13.9)},
        'B5': {'mm': (176, 250), 'in': (6.9, 9.8)},
        'B6': {'mm': (125, 176), 'in': (4.9, 6.9)},
        'B7': {'mm': (88, 125), 'in': (3.5, 4.9)},
        'B8': {'mm': (62, 88), 'in': (2.4, 3.5)},
        'B9': {'mm': (44, 62), 'in': (1.7, 2.4)},
        'B10': {'mm': (31, 44), 'in': (1.2, 1.7)},
    }

    # C_SERIES

    ISO_269_C = {
        'C0': {'mm': (917, 1297), 'in': (36.1, 51.1)},
        'C1': {'mm': (648, 917), 'in': (25.5, 36.1)},
        'C2': {'mm': (458, 648), 'in': (18.0, 25.5)},
        'C3': {'mm': (324, 458), 'in': (12.8, 18.0)},
        'C4': {'mm': (229, 324), 'in': (9.0, 12.8)},
        'C5': {'mm': (162, 229), 'in': (6.4, 9.0)},
        'C6': {'mm': (114, 162), 'in': (4.5, 6.4)},
        'C7/6': {'mm': (81, 162), 'in': (3.2, 6.4)},
        'C7': {'mm': (81, 114), 'in': (3.2, 4.5)},
        'C8': {'mm': (57, 81), 'in': (2.2, 3.2)},
        'C9': {'mm': (40, 57), 'in': (1.6, 2.2)},
        'C10': {'mm': (28, 40), 'in': (1.1, 1.6)},
    }

    ISO_269_D = {
        'DL': {'mm': (110, 220), 'in': ()}
    }

    LETTER = {'Letter': {'mm': (215.9, 279.4), 'in': (8.5, 11)}}


    STANDARDS = [ISO_216_A, ISO_216_B, ISO_269_C, ISO_269_D, LETTER]

    @classmethod
    def getSize(self, name, unit):
        u"""
        name:
        unit: mm ('mm') or inch ('in')
        """
        if name.startswith('A'):
            sizes = self.ISO_216_A[name]
            return sizes[unit]
        elif name.startswith('B'):
            sizes = self.ISO_216_B[name]
            return sizes[unit]
        elif name.startswith('C'):
            sizes = self.ISO_269_C[name]
            return sizes[unit]
        elif name.startswith('D'):
            sizes = self.ISO_269_D[name]
            return sizes[unit]
        elif name.startswith('L'):
            sizes = self.LETTER
            return sizes[unit]

    @classmethod
    def getAllPaperSizes(self):
        names = []

        for standard in self.STANDARDS:
            names += standard.keys()

        return names
