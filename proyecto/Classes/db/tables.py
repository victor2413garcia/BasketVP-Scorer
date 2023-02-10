tables = ["""CREATE TABLE IF NOT EXISTS `Categorias` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`nombre`	TEXT NOT NULL UNIQUE
);""",
"""CREATE TABLE IF NOT EXISTS `Torneos` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`nombre`	TEXT NOT NULL,
	`lugar`	TEXT,
	`catg_id`	INTEGER NOT NULL,
	FOREIGN KEY(`catg_id`) REFERENCES `Categorias`(`id`)
);""",
"""CREATE TABLE IF NOT EXISTS `Equipos` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`nombre`	TEXT NOT NULL,
	`torn_id`	INTEGER NOT NULL,
	FOREIGN KEY(`torn_id`) REFERENCES `Torneos`(`id`)
);""",
"""CREATE TABLE IF NOT EXISTS `Jugadores` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`nombre`	TEXT NOT NULL,
	`nro`	INTEGER NOT NULL,
	`eq_id`	INTEGER NOT NULL,
	FOREIGN KEY(`eq_id`) REFERENCES `Equipos`(`id`)
);""",
"""CREATE TABLE IF NOT EXISTS `Rosters` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`juego_id`	INTEGER NOT NULL,
	`jugador_id`	INTEGER NOT NULL,
	FOREIGN KEY(`jugador_id`) REFERENCES `Jugadores`(`id`),
	FOREIGN KEY(`juego_id`) REFERENCES `Juegos_info`(`id`)
);""",
"""CREATE TABLE IF NOT EXISTS `Juegos_info` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`eq_local_id`	INTEGER NOT NULL,
	`eq_visit_id`	INTEGER NOT NULL,
	`ganador_id`	INTEGER,
	`lugar`	TEXT,
	`time`	TEXT,
	`torn_id`	INTEGER,
	FOREIGN KEY(`eq_visit_id`) REFERENCES `Equipos`(`id`),
	FOREIGN KEY(`eq_local_id`) REFERENCES `Equipos`(`id`),
	FOREIGN KEY(`ganador_id`) REFERENCES `Equipos`(`id`),
	FOREIGN KEY(`torn_id`) REFERENCES `Torneos`(`id`)
);""",
"""CREATE TABLE IF NOT EXISTS `Boxscore` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`jugador_id`	INTEGER NOT NULL,
	`juego_id`	INTEGER NOT NULL,
	`pt`	INTEGER NOT NULL,
	`falta`	INTEGER NOT NULL,
	`qt`	INTEGER NOT NULL,
	FOREIGN KEY(`jugador_id`) REFERENCES `Jugadores`(`id`),
	FOREIGN KEY(`juego_id`) REFERENCES `Juegos_info`(`id`)
);""",
"""CREATE TABLE IF NOT EXISTS `test` (
	`id`	INTEGER
);"""]