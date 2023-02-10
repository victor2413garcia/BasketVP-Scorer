from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QPoint

import sys
from functools import partial
from datetime import datetime

from Classes.Design.estadisticas import Ui_Form
from Classes.plot import Plot
from Classes.db.utils import Data

class Stats(QDialog, Ui_Form):
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
		self.radioButton_3.toggled.connect(self.on_toggled_3)
		self.radioButton_4.toggled.connect(self.on_toggled_4)

		self.radioButton_2.toggled.connect(self.on_toggled_2)
		self.radioButton.toggled.connect(self.on_toggled)

		self.tableWidget.doubleClicked.connect(self.doubleClicked)

	@QtCore.pyqtSlot(QtCore.QModelIndex)
	def doubleClicked(self, index):
		row = index.row()
		nombre=self.tableWidget.item(row,0).text()
		id=self.jug[nombre]
		Plot(id, nombre).exec_()

	def on_toggled_2(self):
		self.tableWidget.sortByColumn(2, QtCore.Qt.DescendingOrder)

	def on_toggled_3(self):
		self.tableWidget.sortByColumn(3, QtCore.Qt.DescendingOrder)

	def on_toggled(self):
		self.tableWidget.sortByColumn(4, QtCore.Qt.DescendingOrder)

	def on_toggled_4(self):
		self.tableWidget.sortByColumn(5, QtCore.Qt.DescendingOrder)

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
			torn_id=self.tor_ids[indice_t]
			self.actualizar_tablas(indice_t)
		else:
			torn_id=self.tor_ids[0]
		self.comboBox.setEnabled(False)


	def actualizar_tablas(self, tor=0):
		while (self.tableWidget.rowCount() > 0):
			self.tableWidget.removeRow(0)
		db = Data()
		self.jug={}
		self.pts=[]
		jugs = db.get_equipo(tor)
		teams=[]
		ids=[]
		for i in jugs:
			ids.append(i[0])
			teams.append([i[0],i[1].split()[0]])
		jugs=db.get_all_jugadores(ids)
		ids=[]
		for i in jugs:
			ids.append(i[0])
		jugs[0]=list(jugs[0])
		for k in jugs:
			for i in teams:
				if i[0] == k[2]:
					k[2]=i[i.index(k[2])+1]
		
		self.pts=db.get_stats(ids)
		self.tableWidget.setRowCount(len(jugs))
		for i,juga in enumerate(jugs):
			for k in range(len(juga)+4):
				item = QtWidgets.QTableWidgetItem()
				self.tableWidget.setItem(i, k, item)
				item = self.tableWidget.item(i, k)
				if k<2:
					item.setText(str(juga[k+1]))
				elif k==2:
					element = str(self.pts[i][0])    # convert to str
					padded = ('     '+element)[-5:]
					item.setText(padded)
				elif k==3:
					element = str(self.pts[i][1])    # convert to str
					padded = ('     '+element)[-5:]
					item.setText(padded)
				elif k==4:
					element = str(self.pts[i][2])    # convert to str
					padded = ('     '+element)[-5:]   # make all elements the same length
					item.setText(padded)
				elif k==5:
					element = str(self.pts[i][3])    # convert to str
					padded = ('     '+element)[-5:]
					item.setText(padded)
				elif k==6:
					element = str(self.pts[i][4])    # convert to str
					padded = ('     '+element)[-5:]
					item.setText(padded)
			self.jug[juga[1]]=juga[0]
		self.tableWidget.sortByColumn(3, QtCore.Qt.DescendingOrder)

if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Settings()
	win.show()
	sys.exit(app.exec())