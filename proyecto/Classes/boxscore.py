from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QPoint
import sys

from Classes.Design.boxscore import Ui_Form
from Classes.accion import Accion
from Classes.warning import Overtime
from Classes.play import Play
from Classes.db.utils import Data

class Boxscore(QDialog, Ui_Form):
	"""docstring for Settigns"""
	def __init__(self, data, jueg_id, eq_id):
		super().__init__()
		self.jug=[[],[]]
		self.setupUi(self)
		self.oldPos = self.pos()
		self.data=data
		self.jueg_id=jueg_id
		self.eq_id=eq_id

		self.qt=1

		self.pt_local=0
		self.pt_visit=0

		self.foul_l=0
		self.foul_v=0

		self.label_2.setText(list(data.keys())[0])
		self.label_3.setText(list(data.keys())[1])

		self.label_13.setText(list(data.keys())[0])
		self.label_15.setText(list(data.keys())[1])
		self.actualizar_tablas()

		self.tableWidget.doubleClicked.connect(self.accion_local)
		self.tableWidget_2.doubleClicked.connect(self.accion_visit)

		self.pushButton_2.clicked.connect(self.next_qt)
		self.pushButton.clicked.connect(self.prev_qt)
		self.pushButton_4.clicked.connect(self.open_play)
		self.pushButton_5.clicked.connect(self.next_qt_f)

	def open_play(self):
		Play(self.jueg_id).exec_()

	@QtCore.pyqtSlot(QtCore.QModelIndex)
	def accion_local(self, index):
		db = Data()
		jug_info = db.get_roster(list(self.data.values())[0])
		qtr=self.lcdNumber_3.value()
		row = index.row()
		if self.pts[row][1]==5:
			Overtime(True, self, fouls=True, teams=[list(self.data.keys())[0],list(self.data.keys())[1]]).exec_()
		else:
			jug_info=jug_info[row]
			Accion(True,jug_info, self.jueg_id, qtr, self).exec_()

	@QtCore.pyqtSlot(QtCore.QModelIndex)
	def accion_visit(self, index):
		db = Data()
		jug_info = db.get_roster(list(self.data.values())[1])
		qtr=self.lcdNumber_3.value()
		row = index.row()
		if self.pts_2[row][1]==5:
			Overtime(False, self, fouls=True,teams=[list(self.data.keys())[0],list(self.data.keys())[1]]).exec_()
		else:
			jug_info=jug_info[row]
			Accion(False,jug_info, self.jueg_id, qtr, self).exec_()

	def actualizar_tablas(self):
		db = Data()
		self.jug[0]=[]
		jugs = db.get_roster(list(self.data.values())[0])
		self.pts=db.get_score(list(self.data.values())[0],self.jueg_id)
		self.tableWidget.setRowCount(len(jugs))
		for i,juga in enumerate(jugs):
			for k in range(len(juga)+1):
				item = QtWidgets.QTableWidgetItem()
				self.tableWidget.setItem(i, k, item)
				item = self.tableWidget.item(i, k)
				if k<2:
					item.setText(str(juga[k+1]))
				elif k==2:
					item.setText(str(self.pts[i][0]))
				elif k==3:
					item.setText(str(self.pts[i][1]))
					if self.pts[i][1] ==5:
						item.setBackground(QtGui.QColor(204, 0, 0))
			self.jug[0].append(juga[0])

		self.jug[1]=[]
		jugs = db.get_roster(list(self.data.values())[1])
		self.pts_2=db.get_score(list(self.data.values())[1],self.jueg_id)
		self.tableWidget_2.setRowCount(len(jugs))
		for i,juga in enumerate(jugs):
			for k in range(len(juga)+1):
				item = QtWidgets.QTableWidgetItem()
				self.tableWidget_2.setItem(i, k, item)
				item = self.tableWidget_2.item(i, k)
				if k<2:
					item.setText(str(juga[k+1]))
				elif k==2:
					item.setText(str(self.pts_2[i][0]))
				elif k==3:
					item.setText(str(self.pts_2[i][1]))
					if self.pts_2[i][1] ==5:
						item.setBackground(QtGui.QColor(204, 0, 0))
			self.jug[1].append(juga[0])

	def next_qt(self):
		self.qt+=1
		if self.qt>4:
			if self.pt_local == self.pt_visit:
				Overtime(True,ventana=self).exec_()
				self.lcdNumber_3.setDigitCount(2)
				self.lcdNumber_3.display("PE")
			else:
				ganador=0
				if self.pt_local>self.pt_visit:
					ganador=self.eq_id[0]
				else:
					ganador=self.eq_id[1]
				Overtime(False, self, teams=[list(self.data.keys())[0],list(self.data.keys())[1]], ganador=ganador, juego_id=self.jueg_id).exec_()
		else:
			self.lcdNumber_3.display(self.qt)
		self.reinicia_fouls()

	def next_qt_f(self):
		self.qt+=5
		if self.qt>4:
			if self.pt_local == self.pt_visit:
				Overtime(True,ventana=self).exec_()
				self.lcdNumber_3.setDigitCount(2)
				self.lcdNumber_3.display("PE")
			else:
				ganador=0
				if self.pt_local>self.pt_visit:
					ganador=self.eq_id[0]
				else:
					ganador=self.eq_id[1]
				Overtime(False, self, teams=[list(self.data.keys())[0],list(self.data.keys())[1]], ganador=ganador, juego_id=self.jueg_id).exec_()
		else:
			self.lcdNumber_3.display(self.qt)
		self.reinicia_fouls()

	def prev_qt(self):
		self.qt-=1
		if self.qt<1:
			self.qt=1
		self.lcdNumber_3.display(self.qt)

	def reinicia_fouls(self):
		self.foul_l=0
		self.foul_v=0
		self.lcdNumber_4.display(self.foul_l)
		self.lcdNumber_5.display(self.foul_v)
		self.lcdNumber_4.setStyleSheet("color: rgb(0, 0, 0);")
		self.lcdNumber_5.setStyleSheet("color: rgb(0, 0, 0);")
		
if __name__ == "__main__":
	app=QApplication(sys.argv)
	win=Boxscore()
	win.show()
	sys.exit(app.exec())