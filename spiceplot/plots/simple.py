"""
:mod:`spiceplot.plots` - Generate matplotlib plots from imported data
=====================================================================

.. module:: spiceplot.plots
    :synopsis: Generate matplotlib plots from imported data

.. moduleauthor:: Lucas van Dijk
"""

import matplotlib.pyplot as plt

class LinePlot:
    """
        A simple line plot with one or more variables
    """

    def __init__(self, plot_data, plot_func='plot', **kwargs):
        self.plot_data = plot_data
        self.plot_func = plot_func
        self.plot_args = kwargs

        self._x_label = ""
        self._y_label = ""

    @property
    def x_label(self):
        def getter():
            return self._x_label

        def setter(value):
            self._x_label = value

    @property
    def y_label(self):
        def getter():
            return self._y_label

        def setter(value):
            self._y_label = value

    def create_plot(self):
        figure = plt.figure()

        ax = figure.add_subplot(1, 1, 1)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        self.generate_axis(ax, self.plot_data)

        return figure

    def generate_axis(self, ax, plot_data):
        for vector in plot_data.vectors:
            plot_func = getattr(ax, self.plot_func, 'plot')
            plot_func(plot_data.x_axis.data, vector.data, **self.plot_args)

        ax.grid(which='both')
        ax.legend([vector.name for vector in plot_data.vectors])
        ax.set_title(plot_data.title)

class MultipleLinePlot(LinePlot):
    """
        Create a figure with multiple line plots for each given plot data object
    """

    def __init__(self, plot_datas, plot_func='plot', **kwargs):
        LinePlot.__init__(self, plot_datas, plot_func, **kwargs)

        self._x_label = [""]
        self._y_label = [""]

    @property
    def x_label(self):
        def getter():
            return self._x_label

        def setter(value):
            if type(value) == list:
                self._x_label = value
            else:
                self._x_label = [value]

    @property
    def y_label(self):
        def getter():
            return self._y_label

        def setter(value):
            if type(value) == list:
                self._y_label = value
            else:
                self._y_label

    def create_plot(self):
        figure = plt.figure()

        for i, plot in enumerate(self.plot_data):
            ax = figure.add_subplot(len(self.plot_data), 1, i+1)
            ax.set_xlabel(self._x_label[i]
                if i < len(self._x_label) else self._x_label[0])
            ax.set_ylabel(self._y_label[i]
                if i < len(self._y_label) else self._y_label[0])

            self.generate_axis(ax, plot)

        return figure

class CombinedLinePlot(LinePlot):
    def __init__(self, plot_datas, plot_func='plot', **kwargs):
        LinePlot.__init__(self, plot_datas, plot_func, **kwargs)

    def create_plot(self):
        figure = plt.figure()
        ax = figure.add_subplot(1, 1, 1)
        ax.set_xlabel(self._x_label)
        ax.set_ylabel(self._y_label)
        ax.grid(which='both')

        legend = []

        for plot in self.plot_data:
            self.generate_axis(ax, plot)

            legend.extend([" - ".join([plot.title, vector.name])
                for vector in plot.vectors])

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, 0.7 * box.width, box.height])
        ax.legend(legend, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        ax.grid(which='both')

