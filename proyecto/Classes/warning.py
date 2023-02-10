from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import sys
from time import strftime
import time

from Classes.Design.warning import Ui_Dialog
from Classes.db.utils import Data

class Overtime(QDialog, Ui_Dialog):
	"""docstring for Settigns"""
	def __init__(self, isOvertime, ventana, fouls=False, teams=[], ganador=0, juego_id=0):
		super().__init__()
		self.setupUi(self)
		self.ventana=ventana
		self.isOvertime=isOvertime
		self.teams=teams
		self.time=strftime("%Y-%m-%d %H:%M:%S")
		self.ganador_id=ganador
		self.juego_id=juego_id
		self.oldPos = self.pos()
		self.buttonBox.accepted.connect(self.aceptado)
		self.buttonBox.rejected.connect(self.rechazado)
		if not isOvertime:
			self.label_2.setText("Game Over")
			self.label.setText("El partido ha Finalizado")
		if fouls:
			self.label_2.setText("Expulsion")
			self.label.setText("Jugador expulsado por 5 faltas")
			self.buttonBox.clear()

	def aceptado(self):
		if not self.isOvertime:
			self.destroy()
			time.sleep(1)
			screen = QtWidgets.QApplication.primaryScreen()
			screenshot = screen.grabWindow(self.ventana.winId())
			screenshot.save('./Reportes/{0} vs {1} {2}.jpg'.format(self.teams[0],self.teams[1], self.time), 'jpg')
			self.ventana.destroy()
			data=Data()
			data=data.set_ganador(self.ganador_id, self.juego_id)
		self.rechazado()

	def rechazado(self):
		self.close()
		
if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Categoria()
	win.show()
	sys.exit(app.exec())