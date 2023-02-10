from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QPoint

import sys
from functools import partial
from datetime import datetime

from Classes.Design.anteriores import Ui_Form
from Classes.play  import Play
from Classes.db.utils import Data

class Anteriores(QDialog, Ui_Form):
	"""docstring for Settigns"""
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.oldPos = self.pos()
		#enlista los datos registrados
		self.data = Data()
		#indice seleccionado de torneo
		self.tor_ids =[0]

		self.actualizar_torneo()
		self.pts=[]

		self.jug ={}
		self.comboBox.currentIndexChanged.connect(self.actualizar)
		self.radioButton_3.toggled.connect(self.on_toggled)

		self.radioButton_2.toggled.connect(self.on_toggled_2)
		self.radioButton.toggled.connect(self.on_toggled_3)

		self.tableWidget.doubleClicked.connect(self.doubleClicked)

	@QtCore.pyqtSlot(QtCore.QModelIndex)
	def doubleClicked(self, index):
		row = index.row()
		nombre=self.tableWidget.item(row,4).text()
		id=self.jug[nombre]
		Play(id).exec_()

	def on_toggled_2(self):
		self.tableWidget.sortByColumn(0, QtCore.Qt.DescendingOrder)

	def on_toggled_3(self):
		self.tableWidget.sortByColumn(1, QtCore.Qt.DescendingOrder)

	def on_toggled(self):
		self.tableWidget.sortByColumn(2, QtCore.Qt.DescendingOrder)

	def actualizar_torneo(self):
		tors = self.data.get_torneos()
		self.comboBox.clear()
		if len(tors) != 0:
			self.comboBox.addItem("-Seleccione un Torneo-")
			self.tor_ids=[0]
			for tor in tors:
				self.tor_ids.append(tor[0])
				self.comboBox.addItem(tor[1])

	def actualizar(self):
		indice_t=self.comboBox.currentIndex()
		if indice_t > 0:
			self.torn_id=self.tor_ids[indice_t]
			self.actualizar_tablas(indice_t)
		else:
			self.torn_id=self.tor_ids[0]
		self.comboBox.setEnabled(False)


	def actualizar_tablas(self, tor=0):
		while (self.tableWidget.rowCount() > 0):
			self.tableWidget.removeRow(0)
		db = Data()
		self.jug={}
		self.pts=[]
		
		self.pts=db.get_juegos(self.torn_id)
		print(self.pts)
		self.tableWidget.setRowCount(len(self.pts))
		for i,juga in enumerate(self.pts):
			for k in range(len(juga)):
				item = QtWidgets.QTableWidgetItem()
				self.tableWidget.setItem(i, k, item)
				item = self.tableWidget.item(i, k)
				if k<5:
					if k==2:
						item.setBackground(QtGui.QColor(0, 128, 0))
						item.setForeground(QtGui.QColor(255, 255, 255))
					element=juga[k+1]
					if type(element) is int:
						element=str(db.get_equipo([element])[0][1]).split()[0]
					item.setText(element)
			self.jug[juga[5]]=juga[0]
		self.tableWidget.sortByColumn(3, QtCore.Qt.DescendingOrder)

if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Settings()
	win.show()
	sys.exit(app.exec())