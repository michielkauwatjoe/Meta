# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+ www.michielkauwatjoe.com
#
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    python setup.py py2app
#
"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

setup(
    app=['main.py'],
    name="Meta",
    data_files=['en.lproj'],
    setup_requires=['py2app'],
    options=dict(py2app=dict(iconfile='en.lproj/meta.icns',
                             includes=['lxml.etree', 'lxml._elementpath', 'pdflib_py'],
                             packages=['meta']
                             )
                 )
)
