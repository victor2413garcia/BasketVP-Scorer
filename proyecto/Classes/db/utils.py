import sqlite3
from datetime import datetime
from Classes.db.tables import *

class Data(object):
	"""docstring for Data"""

	def __init__(self):
		self._name = "db/data.db"
		self.conectar()

	def conectar(self):
		self.conexion=sqlite3.connect(self._name)

	def desconectar(self):
		self.conexion.close()

	def init(self):
		try:
			for i,tabla in enumerate(tables):
				self.conexion.execute(tabla)
			self.conexion.commit()                      
		except sqlite3.OperationalError:
			pass

	def set_categoria(self, nombre):
		try:
			self.conexion.execute("INSERT INTO Categorias(nombre) VALUES (?)",([nombre.upper()]))
			self.conexion.commit()
		except sqlite3.IntegrityError:
			pass

	def get_categoria(self):
		cats=[]
		for cat in self.conexion.execute('SELECT * FROM Categorias'):
			cats.append(cat)
		return cats

	def set_torneo(self, nombre, catg_id):
		try:
			tor=self.get_torneo(catg_id)
			if len(tor)==0:
				self.conexion.execute("INSERT INTO Torneos(nombre, catg_id) VALUES (?,?)",([nombre.upper(), catg_id]))
				self.conexion.commit()
			else:
				#lista con los nombres registrados
				nombres=[i[1] for i in tor]
				if nombre.upper() not in nombres:
					self.conexion.execute("INSERT INTO Torneos(nombre, catg_id) VALUES (?,?)",([nombre.upper(), catg_id]))
					self.conexion.commit()
		except sqlite3.IntegrityError:
			pass

	def get_torneo(self, catg_id):
		tors=[]
		try:
			for tor in self.conexion.execute('SELECT id,nombre FROM Torneos WHERE catg_id=?',[catg_id]):
				tors.append(tor)
		except sqlite3.InterfaceError:
			pass
		return tors

	def get_torneos(self):
		tors=[]
		try:
			for tor in self.conexion.execute('SELECT id,nombre FROM Torneos'):
				tors.append(tor)
		except sqlite3.InterfaceError:
			pass
		return tors

	def set_equipo(self, nombre, torn_id):
		try:
			eqs=self.get_equipo(torn_id)
			if len(eqs)==0:
				self.conexion.execute("INSERT INTO Equipos(nombre, torn_id) VALUES (?,?)",([nombre.title(), torn_id]))
				self.conexion.commit()
			else:
				nombres=[i[1] for i in eqs]
				if nombre.title() not in nombres:
					self.conexion.execute("INSERT INTO Equipos(nombre, torn_id) VALUES (?,?)",([nombre.title(), torn_id]))
					self.conexion.commit()
		except sqlite3.IntegrityError:
			pass

	def get_equipo(self, torn_id):
		eqs=[]
		if type(torn_id) != list:
			try:
				for eq in self.conexion.execute("SELECT id,nombre FROM Equipos WHERE torn_id=?",[torn_id]):
					eqs.append(eq)
			except sqlite3.InterfaceError:
				pass
		else:
			try:
				cond="OR (id=?)" * (len(torn_id)-1)
				sentence="SELECT id,nombre FROM Equipos WHERE (id=?) "+cond
				for eq in self.conexion.execute(sentence,torn_id):
					eqs.append(eq)
			except sqlite3.InterfaceError:
				pass
		return eqs

	def set_juego(self, eq_local_id, eq_visit_id, lugar, time, torn_id):
		try:
			self.conexion.execute("INSERT INTO Juegos_info(eq_local_id, eq_visit_id, lugar, time, torn_id) VALUES(?,?,?,?,?)",([eq_local_id,eq_visit_id,lugar,time, torn_id]))
			self.conexion.commit()
		except sqlite3.IntegrityError:
			pass

	def get_juego(self, time):
		id=[]
		try:
			for i in self.conexion.execute("SELECT id FROM Juegos_info WHERE (time=?)",([time])):
				id.append(i)
		except sqlite3.InterfaceError:
			pass
		return id

	def get_jugadores(self, eq_id):
		jugs=[]
		try:
			for jug in self.conexion.execute("SELECT id,nombre,nro FROM Jugadores WHERE eq_id=?",[eq_id]):
				jugs.append(jug)
		except sqlite3.InterfaceError:
			pass
		return jugs

	def get_all_jugadores(self, eq_id):
		jugs=[]
		try:
			cond="OR (eq_id=?)" * (len(eq_id)-1)
			sentence="SELECT id,nombre,eq_id FROM Jugadores WHERE eq_id=?"+cond
			for jug in self.conexion.execute(sentence,(eq_id)):
				jugs.append(list(jug))
		except sqlite3.InterfaceError:
			pass
		return jugs

	def set_jugadores(self,nombre,nro,eq_id):
		try:
			jugs=self.get_jugadores(eq_id)
			if len(jugs)==0:
				self.conexion.execute("INSERT INTO Jugadores(nombre, nro, eq_id) VALUES(?,?,?)",([nombre.title(),nro,eq_id]))
				self.conexion.commit()
			else:
				nombres=[i[1] for i in jugs]
				nrs=[i[2] for i in jugs]
				if (nombre.title() not in nombres) and (int(nro) not in nrs):
					self.conexion.execute("INSERT INTO Jugadores(nombre, nro, eq_id) VALUES(?,?,?)",([nombre.title(),nro,eq_id]))
					self.conexion.commit()
		except sqlite3.IntegrityError:
			pass

	def set_roster(self, jueg_id, jug_id):
		try:
			self.conexion.execute("INSERT INTO Rosters(juego_id, jugador_id) VALUES(?,?)",([jueg_id, jug_id]))
			self.conexion.commit()
		except sqlite3.IntegrityError as e:
			print(e)

	def get_roster(self, ids):
		jugs=[]
		try:
			cond="OR (id=?)" * (len(ids)-1)
			sentence="SELECT id,nombre,nro FROM Jugadores WHERE (id=?) "+cond
			for jug in self.conexion.execute(sentence,(ids)):
				jugs.append(jug)
		except sqlite3.InterfaceError:
			pass
		return jugs

	def set_score(self, jug_id, jueg_id, pt, falta, qt):
		try:
			self.conexion.execute("INSERT INTO Boxscore(jugador_id, juego_id, pt, falta, qt) VALUES(?,?,?,?,?)",([jug_id, jueg_id, pt, falta, qt]))
			self.conexion.commit()
		except sqlite3.IntegrityError as e:
			print(e)

	def get_score(self, ids, juego_id):
		jugs=[]
		ids=ids.copy()
		try:
			sentence="SELECT SUM(pt), SUM(falta) FROM Boxscore WHERE (jugador_id=? AND juego_id=?)"
			for i in range(len(ids)):
				jug=self.conexion.execute(sentence,(ids[i],juego_id))
				jug=jug.fetchall()
				jug=list(jug[0])
				if jug[0] is None:
					jug[0]=0
				if jug[1] is None:
					jug[1]=0
				jugs.append(jug)
		except sqlite3.InterfaceError:
			pass
		return jugs

	def get_stats(self, ids):
		jugs=[]
		ids=ids.copy()
		try:
			sentence="SELECT SUM(pt), SUM(pt), SUM(falta), SUM(falta), COUNT(DISTINCT juego_id) FROM Boxscore WHERE (jugador_id=?)"
			for i,k in enumerate(ids):
				jug=self.conexion.execute(sentence,(ids[i],))
				jug=jug.fetchall()
				jug=list(jug[0])
				if jug[0] is None:
					jug[0]=0
				else:
					jug[0]=round(jug[0],1)
				if jug[1] is None:
					jug[1]=0
				else:
					jug[1]=round((jug[1]/jug[4]),1)
				if jug[2] is None:
					jug[2]=0
				else:
					jug[2]=round(jug[2],1)
				if jug[3] is None:
					jug[3]=0
				else:
					jug[3]=round((jug[3]/jug[4]),1)
				if jug[4] is None:
					jug[4]=0
				else:
					jug[4]=round(jug[4],1)
				jugs.append(jug)
		except sqlite3.InterfaceError:
			pass
		return jugs

	def get_plot(self, jugador_id):
		tors=[]
		times=[]
		play=[]
		try:
			for tor in self.conexion.execute('SELECT DISTINCT juego_id FROM Boxscore WHERE jugador_id=?',[jugador_id]):
				tors.append(tor[0])
		except sqlite3.InterfaceError:
			pass
		try:
			cond='OR id=?'*(len(tors)-1)
			sentence='SELECT time FROM Juegos_info WHERE id=?'+cond
			jug=self.conexion.execute(sentence,tors)
			jug=jug.fetchall()
			for i in range(len(tors)):
				times.append(datetime.strptime(jug[i][0],'%Y-%m-%d %H:%M:%S'))
		except sqlite3.InterfaceError:
			pass
		sentence="SELECT SUM(pt) FROM Boxscore WHERE (juego_id=?) and (jugador_id=?)"
		for i in tors:
			jug=self.conexion.execute(sentence,(i,jugador_id))
			jug=jug.fetchall()
			play.append(jug[0][0])
		tors=[times,play]
		return tors

	def get_plays(self, juego_id):
		jug=[]
		sentence='SELECT * FROM Boxscore WHERE juego_id=?'
		jug=self.conexion.execute(sentence,(juego_id,))
		jug=jug.fetchall()
		return jug

	def set_ganador(self, ganador_id, juego_id):
		sentence='UPDATE Juegos_info SET ganador_id={0} WHERE id=?'.format(ganador_id)
		jug=self.conexion.execute(sentence,(juego_id,))
		self.conexion.commit()

	def get_juegos(self, torn_id):
		jug=[]
		sentence='SELECT id, eq_local_id, eq_visit_id, ganador_id, lugar, time FROM Juegos_info WHERE torn_id=? AND ganador_id IS NOT NULL'
		jug=self.conexion.execute(sentence,(torn_id,))
		jug=jug.fetchall()
		return jug

	def get_len_torneos(self):
		jug=[]
		sentence='SELECT COUNT(id) FROM Torneos'
		jug=self.conexion.execute(sentence)
		jug=jug.fetchone()
		return jug

	def get_len_partidos(self):
		jug=[]
		sentence='SELECT COUNT(id) FROM Juegos_info'
		jug=self.conexion.execute(sentence)
		jug=jug.fetchone()
		return jug

	def get_len_equipos(self):
		jug=[]
		sentence='SELECT COUNT(id) FROM Equipos'
		jug=self.conexion.execute(sentence)
		jug=jug.fetchone()
		return jug

	def get_len_jugadores(self):
		jug=[]
		sentence='SELECT COUNT(id) FROM Jugadores'
		jug=self.conexion.execute(sentence)
		jug=jug.fetchone()
		return jug