from PyQt5.QtWidgets import *
import sys

from Classes.Design.ingresar_torneo import Ui_Dialog
from Classes.db.utils import Data

class Torneo(QDialog, Ui_Dialog):
	"""docstring for Settigns"""
	def __init__(self, catg_id):
		super().__init__()
		self.catg_id = catg_id
		self.setupUi(self)
		self.oldPos = self.pos()
		self.buttonBox.accepted.connect(self.aceptado)
		self.buttonBox.rejected.connect(self.rechazado)

	def aceptado(self):
		data = Data()
		tor = self.lineEdit.text()
		if tor != '':
			data.set_torneo(tor,self.catg_id)
		data.desconectar()
		self.rechazado()


	def rechazado(self):
		self.close()
		
if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Categoria()
	win.show()
	sys.exit(app.exec())