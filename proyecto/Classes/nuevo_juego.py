from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
import sys
from functools import partial

from Classes.Design.nuevo_juego import Ui_Form
from Classes.ingresar_categoria import Categoria
from Classes.ingresar_torneo import Torneo
from Classes.ingresar_equipo import Equipo
from Classes.confirmar import Confirmar
from Classes.db.utils import Data

class Settings(QDialog, Ui_Form):
	"""docstring for Settigns"""
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		#indice seleccionado de categoria
		self.cats_ids =[0]
		self.tor_ids =[0]
		self.eql_ids =[0]
		self.eqv_ids =[0]

		self.torn_id=0

		self.oldPos = self.pos()
		#enlista los datos registrados
		self.data = Data()
		self.actualizar_categoria()
		#abre ventana de añadir categoria
		self.toolButton_2.clicked.connect(self.categoria)
		#actualiza los comboBox
		self.comboBox_2.currentIndexChanged.connect(self.actualizar_torneo)
		self.comboBox.currentIndexChanged.connect(self.actualizar_equipoL)
		self.comboBox_3.currentIndexChanged.connect(self.actualizar_equipoV)
		#abre ventana de añadir torneo
		self.toolButton.clicked.connect(self.torneo)
		#abre ventana de añadir equipo
		self.toolButton_3.clicked.connect(self.equipo)
		self.toolButton_4.clicked.connect(self.equipo)
		#abre siguiente ventana
		self.pushButton.clicked.connect(self.siguiente)

	def categoria(self):
		Categoria().exec_()
		self.actualizar_categoria()

	def actualizar_categoria(self):
		cats = self.data.get_categoria()
		self.comboBox_2.clear()
		if len(cats) != 0:
			self.comboBox_2.addItem("-Seleccione una Categoria-")
			self.cats_ids=[0]
			for cat in cats:
				self.cats_ids.append(cat[0])
				self.comboBox_2.addItem(cat[1])

	def torneo(self):
		indice=self.comboBox_2.currentIndex()
		if indice > -1:
			catg_id=self.cats_ids[indice]
		else:
			catg_id=self.cats_ids[0]
		if catg_id != 0:
			Torneo(catg_id).exec_()
			self.actualizar_torneo()

	def actualizar_torneo(self):
		indice=self.comboBox_2.currentIndex()
		if indice > -1:
			catg_id=self.cats_ids[indice]
		else:
			catg_id=self.cats_ids[0]
		tors = self.data.get_torneo(catg_id)
		self.comboBox.clear()
		if len(tors) != 0:
			self.comboBox.addItem("-Seleccione un Torneo-")
			self.tor_ids=[0]
			for tor in tors:
				self.tor_ids.append(tor[0])
				self.comboBox.addItem(tor[1])
		
	def equipo(self):
		indice_t=self.comboBox.currentIndex()
		if indice_t > -1:
			self.torn_id=self.tor_ids[indice_t]
		else:
			self.torn_id=self.tor_ids[0]
		if self.torn_id != 0:
			Equipo(self.torn_id).exec_()
			self.actualizar_equipoL()
			self.actualizar_equipoV()

	def actualizar_equipoL(self):
		indice_t=self.comboBox.currentIndex()
		if indice_t > -1:
			self.torn_id=self.tor_ids[indice_t]
		else:
			self.torn_id=self.tor_ids[0]
		eqs = self.data.get_equipo(self.torn_id)
		self.comboBox_3.clear()
		if len(eqs) != 0:
			self.comboBox_3.addItem("-Seleccione un Equipo-")
			self.eql_ids=[0]
			for eq in eqs:
				self.eql_ids.append(eq[0])
				self.comboBox_3.addItem(eq[1])

	def actualizar_equipoV(self):
		indice_t=self.comboBox.currentIndex()
		indice_eq=self.comboBox_3.currentIndex()
		if indice_t > -1:
			self.torn_id=self.tor_ids[indice_t]
		else:
			self.torn_id=self.tor_ids[0]
		eqs = self.data.get_equipo(self.torn_id)
		self.comboBox_4.clear()
		if len(eqs) != 0 and indice_eq > 0:
			self.comboBox_4.addItem("-Seleccione un Equipo-")
			self.eqv_ids=[0]
			for i,eq in enumerate(eqs):
				if (i+1) != indice_eq:
					self.eqv_ids.append(eq[0])
					self.comboBox_4.addItem(eq[1])
		
	def siguiente(self):
		cat=self.comboBox_2.currentIndex()>0
		tor=self.comboBox.currentIndex()>0
		eq_l=self.comboBox_3.currentIndex()>0
		eq_v=self.comboBox_4.currentIndex()>0
		if cat and tor and eq_l and eq_v:
			eq_l=self.eql_ids[self.comboBox_3.currentIndex()]
			eq_v=self.eqv_ids[self.comboBox_4.currentIndex()]
			lugar=self.lineEdit.text()
			Confirmar(eq_l,eq_v,lugar,self, self.torn_id).exec_()

if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Settings()
	win.show()
	sys.exit(app.exec())