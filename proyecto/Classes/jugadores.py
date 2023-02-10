from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPoint
import sys

from Classes.Design.nuevo_jugadores import Ui_Form
from Classes.ingresar_jugador import Jugador
from Classes.confirmar_jugadores import Confirmar
from Classes.db.utils import Data

class Roster(QDialog, Ui_Form):
	"""docstring for Settigns"""
	def __init__(self, eq_id, time):
		super().__init__()
		self.jug=[[],[]]
		self.time=time
		self.eq_id=eq_id
		self.eliminados=[[],[]]

		self.setupUi(self)
		self.oldPos = self.pos()
		data = Data()
		for i,k in enumerate(self.eq_id):
			equipo=data.get_equipo([k])
			if i==0:
				self.label_2.setText(equipo[0][1].split()[0])
			else:
				self.label_3.setText(equipo[0][1].split()[0])

		self.tableWidget.doubleClicked.connect(self.eliminar)
		self.tableWidget_2.doubleClicked.connect(self.eliminar_2)
		self.actualizar_tablas()

		self.pushButton_2.clicked.connect(self.abrir_jugadores)
		self.pushButton.clicked.connect(self.confirmar)

	@QtCore.pyqtSlot(QtCore.QModelIndex)
	def eliminar(self, index):
		row = index.row()
		self.tableWidget.removeRow(row)
		self.jug[0].remove(self.jug[0][row])
		self.eliminados[0].append(self.jug[0][row])
		

	@QtCore.pyqtSlot(QtCore.QModelIndex)
	def eliminar_2(self, index):
		row = index.row()
		self.tableWidget_2.removeRow(row)
		self.jug[1].remove(self.jug[1][row])

	def abrir_jugadores(self):
		Jugador(self.eq_id).exec_()
		self.tableWidget.clearContents()
		self.tableWidget_2.clearContents()
		self.actualizar_tablas()

	def confirmar(self):
		data={}
		conn=Data()
		for i,k in enumerate(self.eq_id):
			equipo=conn.get_equipo([k])
			data[equipo[0][1].split()[0]]=self.jug[i]
		Confirmar(data, self.time, self, self.eq_id).exec_()

	def actualizar_tablas(self):
		self.data = Data()
		self.jug[0]=[]

		jugs = self.data.get_jugadores(self.eq_id[0])
		for i in jugs:
			if i[0] in self.eliminados[0]:
				jugs.remove(i)
		self.tableWidget.setRowCount(len(jugs))
		for i,juga in enumerate(jugs):
			for k in range(len(juga)):
				item = QtWidgets.QTableWidgetItem()
				self.tableWidget.setItem(i, k, item)
				item = self.tableWidget.item(i, k)
				if k==0 or k!=2:
					item.setText(str(juga[k+1]))
			self.jug[0].append(juga[0])


		self.jug[1]=[]
		jugs = self.data.get_jugadores(self.eq_id[1])
		self.tableWidget_2.setRowCount(len(jugs))
		for i,juga in enumerate(jugs):
			for k in range(len(juga)):
				item = QtWidgets.QTableWidgetItem()
				self.tableWidget_2.setItem(i, k, item)
				item = self.tableWidget_2.item(i, k)
				if k==0 or k!=2:
					item.setText(str(juga[k+1]))
			self.jug[1].append(juga[0])

if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Roster()
	win.show()
	sys.exit(app.exec())