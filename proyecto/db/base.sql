BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `Torneos` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`nombre`	text,
	`catg_id`	INTEGER NOT NULL,
	FOREIGN KEY(`catg_id`) REFERENCES `Categorias`(`id`)
);
CREATE TABLE IF NOT EXISTS `Rosters` (
	`jugador_id`	integer NOT NULL,
	`juego_id`	integer PRIMARY KEY AUTOINCREMENT,
	FOREIGN KEY(`jugador_id`) REFERENCES `Jugadores`(`id`)
);
CREATE TABLE IF NOT EXISTS `Jugadores` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`nombre`	text,
	`nro`	integer,
	`eq_id`	integer NOT NULL,
	FOREIGN KEY(`eq_id`) REFERENCES `Torneos`(`id`)
);
CREATE TABLE IF NOT EXISTS `Juegos_info` (
	`id`	integer PRIMARY KEY AUTOINCREMENT,
	`eq_local_id`	integer NOT NULL,
	`eq_visit_id`	integer NOT NULL,
	`ganador_id`	integer,
	`lugar`	text,
	`time`	datetime,
	FOREIGN KEY(`eq_visit_id`) REFERENCES `Equipos`(`id`),
	FOREIGN KEY(`eq_local_id`) REFERENCES `Equipos`(`id`),
	FOREIGN KEY(`ganador_id`) REFERENCES `Equipos`(`id`)
);
CREATE TABLE IF NOT EXISTS `Equipos` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`nombre`	text,
	`torn_id`	integer NOT NULL,
	FOREIGN KEY(`torn_id`) REFERENCES `Torneos`(`id`)
);
CREATE TABLE IF NOT EXISTS `Categorias` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`nombre`	text NOT NULL
);
CREATE TABLE IF NOT EXISTS `Boxscore` (
	`jugador_id`	integer NOT NULL,
	`juego_id`	integer PRIMARY KEY AUTOINCREMENT,
	`pt`	integer NOT NULL,
	`falta`	integer NOT NULL,
	`qt`	integer NOT NULL,
	FOREIGN KEY(`jugador_id`) REFERENCES `Jugadores`(`id`),
	FOREIGN KEY(`juego_id`) REFERENCES `Juegos_info`(`id`)
);
COMMIT;
