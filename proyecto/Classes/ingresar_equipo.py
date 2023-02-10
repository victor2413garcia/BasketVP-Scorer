from PyQt5.QtWidgets import *
import sys

from Classes.Design.ingresar_equipo import Ui_Dialog
from Classes.db.utils import Data

class Equipo(QDialog, Ui_Dialog):
	"""docstring for Settigns"""
	def __init__(self, torn_id):
		super().__init__()
		self.torn_id = torn_id
		self.setupUi(self)
		self.oldPos = self.pos()
		self.buttonBox.accepted.connect(self.aceptado)
		self.buttonBox.rejected.connect(self.rechazado)

	def aceptado(self):
		data = Data()
		equ = self.lineEdit.text()
		if equ != '':
			data.set_equipo(equ, self.torn_id)
		data.desconectar()
		self.rechazado()


	def rechazado(self):
		self.close()
		
if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Equipo()
	win.show()
	sys.exit(app.exec())