from PyQt5.QtWidgets import *
from time import strftime
import sys

from Classes.Design.confirmar import Ui_Dialog
from Classes.jugadores import Roster
from Classes.db.utils import Data

class Confirmar(QDialog, Ui_Dialog):
	"""docstring for Settigns"""
	def __init__(self, eq_local_id, eq_visit_id, lugar, ventana, torn_id):
		super().__init__()
		self.setupUi(self)
		self.eq_local_id=eq_local_id
		self.eq_visit_id=eq_visit_id
		self.lugar=lugar
		self.torn_id=torn_id
		self.time=strftime("%Y-%m-%d %H:%M:%S")
		self.ventana=ventana
		self.oldPos = self.pos()
		self.buttonBox.accepted.connect(self.aceptado)
		self.buttonBox.rejected.connect(self.rechazado)

	def aceptado(self):
		data = Data()
		data.set_juego(self.eq_local_id, self.eq_visit_id, self.lugar, self.time, self.torn_id)
		data.desconectar()
		self.rechazado()
		self.ventana.close()
		Roster([self.eq_local_id,self.eq_visit_id], self.time).exec_()



	def rechazado(self):
		self.close()
		
if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Categoria()
	win.show()
	sys.exit(app.exec())