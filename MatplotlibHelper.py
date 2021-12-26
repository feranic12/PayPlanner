from PyQt5 import QtWidgets
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas


class MplCanvas(Canvas):
    def __init__(self, app):
        dataset = app.make_dataset()
        values = dataset[0]
        index = dataset[1]
        plt.bar(index, values, color="lightblue")
        fig = plt.gcf()
        fig.set_figwidth(12)
        fig.set_figheight(5)
        Canvas.__init__(self, fig)


class MplWidget(QtWidgets.QWidget):
    def __init__(self, app):
        QtWidgets.QWidget.__init__(self)
        self.canvas = MplCanvas(app)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)


