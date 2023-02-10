from PyQt5.QtWidgets import *
import sys

from Classes.Design.ingresar_jugador import Ui_Dialog
from Classes.db.utils import Data

class Jugador(QDialog, Ui_Dialog):
	"""docstring for Settigns"""
	def __init__(self, eq_id):
		super().__init__()
		self.eq_id = eq_id
		self.id_opt=[[0]]
		self.setupUi(self)
		self.oldPos = self.pos()

		self.data=Data()
		eqs=self.data.get_equipo(self.eq_id)
		if len(eqs) != 0:
			self.comboBox.addItem("-Seleccione un Equipo-")
			for eq in eqs:
				self.comboBox.addItem(eq[1])
				self.id_opt.append(eq[0])

		self.buttonBox.accepted.connect(self.aceptado)
		self.buttonBox.rejected.connect(self.rechazado)

	def aceptado(self):
		data = Data()
		nombre = self.lineEdit.text()
		nro = self.lineEdit_2.text()
		equipo = self.comboBox.currentIndex()
		if nombre != '' and nro != '' and equipo > 0:
			equipo=self.id_opt[equipo]
			print(equipo)
			data.set_jugadores(nombre, nro, equipo)
		data.desconectar()
		self.rechazado()


	def rechazado(self):
		self.close()
		
if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Categoria()
	win.show()
	sys.exit(app.exec())