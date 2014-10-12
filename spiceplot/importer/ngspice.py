"""
:mod:`spiceplot.importer.ngspice` - NGSpice importer backend
============================================================

.. module:: spiceplot.importer.ngspice
    :synopsis: NGSpice importer backend

.. moduleauthor:: Lucas van Dijk
"""

import logging

import numpy as np

from spiceplot.importer.base import PlotData, Vector

logger = logging.getLogger(__name__)

class Importer:
    def __init__(self, filename):
        self.filename = filename
        self.plots = []
        self.current_plot = None
        self.vectors = []

    def read_plots(self):
        with open(self.filename, 'rb') as f:
            while True:
                line = f.readline()
                if line == b'\n':
                    continue

                if not line.strip():
                    break

                parts = [part.strip() for part in line.split(b':', 1)]
                attr = parts[0].lower()

                possible_attrs = {
                    b'plotname': self.create_new_plot,
                    b'flags': lambda value: self.set_flags([flag.lower().strip()
                        for flag in value.split()]),
                    b'no. variables': self.set_num_variables,
                    b'no. points': self.set_num_points,
                    b'variables': lambda value: self.read_variables(f),
                    b'values': lambda value: self.read_values(f),
                    b'binary': lambda value: self.read_binary(f)
                }

                if attr in possible_attrs:
                    possible_attrs[attr](parts[1])
                else:
                    logger.info('Ignoring attribute %s', attr)

            self.plots.append(self.current_plot)

        return self.plots

    def create_new_plot(self, title=""):
        if self.current_plot:
            self.plots.append(self.current_plot)

        self.current_plot = PlotData(title)
        self.vectors = []

    def set_flags(self, flags):
        if 'real' in flags:
            self.current_plot.is_complex = False
        elif 'complex' in flags:
            self.current_plot.is_complex = True

    def set_num_variables(self, value):
        self.current_plot.num_variables = int(value)

    def set_num_points(self, value):
        self.current_plot.num_points = int(value)

    def read_variables(self, f):
        if not self.current_plot.num_variables:
            raise ValueError("No information available about the number of points")

        for i in range(self.current_plot.num_variables):
            line = f.readline()
            parts = [part.strip() for part in line.split()]

            if len(parts) < 3:
                logger.info('Invalid variable line "%s"', line)
                continue

            self.vectors.append(
                Vector(
                    name=parts[1], data_type=parts[2],
                    data=np.zeros(self.current_plot.num_points, dtype="float64"),
                    is_complex=self.current_plot.is_complex
                )
            )

    def read_values(self, f):
        if not self.current_plot.num_variables or not self.current_plot.num_points:
            raise ValueError("No information about the number of variables or "
                "points.")

        point_num = 0
        while point_num < self.current_plot.num_points:
            var_num = 0
            while var_num < self.current_plot.num_variables:
                line = f.readline()

                values = line.split()
                print(point_num, var_num)
                print(values)
                if not values:
                    print("-Skip")
                    continue

                if len(values) > 1:
                    self.vectors[var_num].data[point_num] = self.parse_value(
                        values[1])
                else:
                    self.vectors[var_num].data[point_num] = self.parse_value(
                        values[0])

                var_num += 1

            point_num += 1

        print(self.vectors)
        self.current_plot.x_axis = self.vectors[0]
        self.current_plot.vectors = self.vectors[1:]

        print(self.current_plot.x_axis.data)
        #print(self.current_plot.vectors[0].data)
        #print(self.current_plot.x_axis.data.size, self.current_plot.vectors[0].data.size)

    def read_binary(self, f):
        raise NotImplementedError

    def parse_value(self, value):
        if b"," in value:
            parts = value.split(b",")
            real = float(parts[0])
            imag = float(parts[1])
            return real + imag*j
        else:
            return float(value)

