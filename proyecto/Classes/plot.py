from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from pyqtgraph import PlotWidget, plot, DateAxisItem
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from datetime import datetime

from Classes.Design.grafico import Ui_Form

from Classes.db.utils import Data

class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value) for value in values]

class Plot(QDialog, Ui_Form):

    def __init__(self, id, nombre):
        super().__init__()
        self.setupUi(self)
        self.oldPos = self.pos()
        data=Data()
        info=data.get_plot(id)
        self.graphWidget = pg.PlotWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.graphWidget)
        date = info[0]
        pts= info[1]
        prom = sum(pts)/len(pts)
        prom=[prom for i in pts]

        self.graphWidget.setBackground('w')

        self.graphWidget.setTitle(nombre, color="b", size="30pt")

        styles = {'color':'r', 'font-size':'20px'}
        self.graphWidget.setLabel('left', 'Puntos', **styles)

        pen = pg.mkPen(color=(255,0,0), width=15, style=QtCore.Qt.DashLine)
        pen1 = pg.mkPen(color=(0, 0, 255), width=15, style=QtCore.Qt.DashLine)

        date_axis = TimeAxisItem(x=[x.timestamp() for x in date], orientation='bottom')
        self.graphWidget.setAxisItems({'bottom': date_axis})
        self.graphWidget.plot(x=[x.timestamp() for x in date], y=pts, name="Puntos", pen=pen, symbol='+', symbolSize=30, symbolBrush=('b'))
        #PROMEDIO
        self.graphWidget.plot(x=[x.timestamp() for x in date], y=prom,pen=pen1)
        self.graphWidget.setAxisItems({'bottom':date_axis})
        self.graphWidget.setLabel('bottom', 'Partidos', **styles)
        self.setLayout(layout)


def main():
    app = QtWidgets.QApplication([])
    main = Plot()
    main.show()
    app.exec_()


if __name__ == '__main__':
    main()