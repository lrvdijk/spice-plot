import sys

from spiceplot.importer.ngspice import Importer

if __name__ == '__main__':

    importer = Importer(sys.argv[1])

    plots = importer.read_plots()

    for plot in plots:
        for vector in plot.vectors:
            print(vector.name)
            print(vector.data_type)
            print(vector.data)
            print()



