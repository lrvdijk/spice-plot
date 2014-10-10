"""
:mod:`spiceplot.importer.base` - Base classes for several import backends
=========================================================================

.. module:: spiceplot.importer.base
    :synopsis: Base classes for the several import backends.

.. moduleauthor:: Lucas van Dijk
"""

class PlotData:
    """
        A plot is a collection of one or more data vectors, to be displayed
        as a graph.
    """

    def __init__(self, title=""):
        self.title = title
        self.is_complex = False
        self.num_variables = 0
        self.num_points = 0

        self.x_axis = None
        self.vectors = []

    def add_vector(self, vector):
        self.vectors.append(vector)

class Vector:
    def __init__(self, data=None, name="", data_type="", is_complex=False):
        self.data = data
        self.name = name
        self.data_type = data_type
        self.is_complex = is_complex
