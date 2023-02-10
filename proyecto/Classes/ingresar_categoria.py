from PyQt5.QtWidgets import *
import sys

from Classes.Design.ingresar_categoria import Ui_Dialog
from Classes.db.utils import Data

class Categoria(QDialog, Ui_Dialog):
	"""docstring for Settigns"""
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.oldPos = self.pos()
		self.buttonBox.accepted.connect(self.aceptado)
		self.buttonBox.rejected.connect(self.rechazado)

	def aceptado(self):
		data = Data()
		cat = self.lineEdit.text()
		if cat != '':
			data.set_categoria(cat)
		data.desconectar()
		self.rechazado()


	def rechazado(self):
		self.close()
		
if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Categoria()
	win.show()
	sys.exit(app.exec())