from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib


class MplCanvas(Canvas):
    def __init__(self, parent = None, width = 5, height = 4, dpi = 100):
        self.fig = Figure(figsize=(width, height), dpi = dpi)
        Canvas.__init__(self, self.fig)


class MplWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.canvas = MplCanvas()
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)
