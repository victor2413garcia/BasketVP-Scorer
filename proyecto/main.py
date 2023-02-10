from Classes import principal
from Classes.db import utils
from PyQt5.QtWidgets import *
import sys

if __name__=="__main__":
	#Database
	data=utils.Data()
	data.init()
	data.desconectar()
	
	#interface
	app=QApplication(sys.argv)
	win=principal.Interfaz()
	win.show()
	sys.exit(app.exec())