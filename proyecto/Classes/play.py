from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from pyqtgraph import PlotWidget, plot, DateAxisItem
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from datetime import datetime

from Classes.Design.play import Ui_Form

from Classes.db.utils import Data

class Play(QDialog, Ui_Form):

    def __init__(self, juego_id):
        super().__init__()
        self.setupUi(self)
        self.oldPos = self.pos()
        data=Data()
        plays=data.get_plays(juego_id)
        self.llenar(plays)

    def llenar(self, plays):
        for i in plays:
            jugador=Data()
            jugador=jugador.get_roster([i[1]])[0][1]
            if i[3] > 0:
                string="Q{0}: {1} anota {2}pts".format(i[5], jugador, i[3])
            elif i[4]>0:
                string="Q{0}: Falta de {1}".format(i[5], jugador)
            self.textBrowser.append(string)

def main():
    app = QtWidgets.QApplication([])
    main = Play()
    main.show()
    app.exec_()


if __name__ == '__main__':
    main()