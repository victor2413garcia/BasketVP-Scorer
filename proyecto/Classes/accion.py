from PyQt5.QtWidgets import *
from time import strftime
import sys

from Classes.Design.accion import Ui_Dialog
from Classes.db.utils import Data

class Accion(QDialog, Ui_Dialog):
	"""docstring for Settigns"""
	def __init__(self,isLocal, jug_info, jueg_id, qt, ventana):
		super().__init__()
		self.setupUi(self)
		self.jug_info=jug_info
		self.jueg_id=jueg_id
		self.qt=qt
		self.isLocal=isLocal
		self.ventana=ventana
		self.oldPos = self.pos()

		self.label_4.setText("{nombre} #{nro}".format(nombre=self.jug_info[1], nro=self.jug_info[2]))

		self.buttonBox.accepted.connect(self.aceptado)
		self.buttonBox.rejected.connect(self.rechazado) 

		self.radioButton.toggled.connect(self.on_toggled)
		self.radioButton_2.toggled.connect(self.on_toggled)
		self.radioButton_3.toggled.connect(self.on_toggled)

		self.radioButton_4.toggled.connect(self.on_toggled_2)
		self.radioButton_5.toggled.connect(self.on_toggled_2)

	def aceptado(self):
		data = Data()
		self.pt=0
		self.foul=0
		if self.radioButton_2.isChecked():
			self.pt=1
		elif self.radioButton_3.isChecked():
			self.pt=2
		elif self.radioButton.isChecked():
			self.pt=3
		elif self.radioButton_4.isChecked():
			self.foul=1
		elif self.radioButton_5.isChecked():
			self.foul=1
		if self.pt==0 and self.foul==0:
			pass
		else:
			data.set_score(self.jug_info[0], self.jueg_id, self.pt, self.foul, self.qt)
			data.desconectar()
			self.rechazado()
			self.updateScore()
			self.ventana.actualizar_tablas()

	def rechazado(self):
		self.ventana.actualizar_tablas()
		self.close()

	def on_toggled(self):
		self.radioButton_4.setCheckable(False)
		self.radioButton_5.setCheckable(False)

	def on_toggled_2(self):
		self.radioButton.setCheckable(False)
		self.radioButton_2.setCheckable(False)
		self.radioButton_3.setCheckable(False)

	def updateScore(self):
		if self.isLocal:
			self.ventana.pt_local += self.pt
			self.ventana.lcdNumber.display(self.ventana.pt_local)

			self.ventana.foul_l += self.foul
			if self.ventana.foul_l > 5:
				self.ventana.foul_l = 5
			elif self.ventana.foul_l >= 4:
				self.ventana.lcdNumber_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(239, 41, 41);")
			self.ventana.lcdNumber_4.display(self.ventana.foul_l)
		else:
			self.ventana.pt_visit += self.pt
			self.ventana.lcdNumber_2.display(self.ventana.pt_visit)

			self.ventana.foul_v += self.foul
			if self.ventana.foul_v > 5:
				self.ventana.foul_v= 5
			elif self.ventana.foul_v >= 4:
				self.ventana.lcdNumber_5.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(239, 41, 41);")
			self.ventana.lcdNumber_5.display(self.ventana.foul_v)

if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Categoria()
	win.show()
	sys.exit(app.exec())