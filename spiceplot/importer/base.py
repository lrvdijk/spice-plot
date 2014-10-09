"""
:mod:`spiceplot.importer.base` - Base classes for several import backends
=========================================================================

.. module:: spiceplot.importer.base
    :synopsis: Base classes for the several import backends.

.. moduleauthor:: Lucas van Dijk
"""

import numpy as np

class PlotData:
    """
        A plot is a collection of one or more data vectors, to be displayed
        as a graph.
    """

    def __init__(self, title=""):
        self.title = title
        self.x_axis = np.array([])

        self.properties = {}
        self.vectors = []

    def set_properties(self, **kwargs):
        self.properties.update(kwargs)

    def add_vector(self, data):
        self.vectors.append(data)

