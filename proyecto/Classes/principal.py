from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
import sys

from Classes.Design.principal import Ui_Form
from Classes.nuevo_juego import Settings
from Classes.anteriores import Anteriores
from Classes.estadisticas import Stats

from Classes.db.utils import Data

class Interfaz(QDialog,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.oldPos = self.pos()

        data=Data()

        #conectar botones a abrir ventanas
        self.pushButton.clicked.connect(self.abrir_opcion)
        self.pushButton_2.clicked.connect(self.abrir_opcion)
        self.pushButton_3.clicked.connect(self.abrir_opcion)

        self.label_5.setText(str(data.get_len_torneos()[0]))
        self.label_6.setText(str(data.get_len_partidos()[0]))
        self.label_9.setText(str(data.get_len_equipos()[0]))
        self.label_10.setText(str(data.get_len_jugadores()[0]))

    #abrir ventanas
    def abrir_opcion(self):
    	sender = self.sender()
    	if sender.text() == "Nuevo Partido":
    		Settings().exec_()
    	elif sender.text() == "Partidos Anteriores":
    		Anteriores().exec_()
    	elif sender.text() == "Estadisticas Jugadores":
    		Stats().exec_()

if __name__=="__main__":
    app=QApplication(sys.argv)
    win=Interfaz()
    win.show()
    sys.exit(app.exec())