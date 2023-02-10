from PyQt5.QtWidgets import *
from time import strftime
import sys

from Classes.Design.confirmar_jugadores import Ui_Dialog
from Classes.boxscore import Boxscore
from Classes.db.utils import Data

class Confirmar(QDialog, Ui_Dialog):
	"""docstring for Settigns"""
	def __init__(self, data, time, ventana, eq_id):
		super().__init__()
		self.setupUi(self)
		self.data=data
		self.time=time
		self.ventana=ventana
		self.eq_id=eq_id
		self.oldPos = self.pos()

		self.label_2.setText("{local}: {cant} Jugadores".format(local=list(data.keys())[0],cant=len(list(data.values())[0])))
		self.label_3.setText("{visit}: {cant} Jugadores".format(visit=list(data.keys())[1],cant=len(list(data.values())[1])))

		if len(list(data.values())[0]) < 5 or len(list(data.values())[0]) > 12:
			self.label.setText("Ingrese cantidades validas")
			self.label_2.setText("{local}: {cant} Jugadores".format(local=list(data.keys())[0],cant="MIN:5, MAX:12 Jugadores"))
			self.buttonBox.clear()
		if len(list(data.values())[1]) < 5 or len(list(data.values())[1]) > 12:
			self.label.setText("Ingrese cantidades validas")
			self.label_3.setText("{visit}: {cant} Jugadores".format(visit=list(data.keys())[1],cant="MIN:5, MAX:12 Jugadores"))
			self.buttonBox.clear()
		self.buttonBox.accepted.connect(self.aceptado)
		self.buttonBox.rejected.connect(self.rechazado)

	def aceptado(self):
		data = Data()
		juego_id=data.get_juego(self.time)[0][0]
		jugs_id=[k for k in self.data.values() for k in k]
		for jug_id in jugs_id:
			data.set_roster(juego_id, jug_id)
		data.desconectar()
		self.rechazado()
		self.ventana.close()
		Boxscore(self.data, juego_id, self.eq_id).exec_()

	def rechazado(self):
		self.close()
		
if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Categoria()
	win.show()
	sys.exit(app.exec())