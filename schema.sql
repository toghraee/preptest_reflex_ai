
CREATE TABLE localauthsession (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	session_id LONGTEXT NOT NULL, 
	expiration TEXT NOT NULL, 
	PRIMARY KEY (id)
)ENGINE=InnoDB COLLATE utf8mb4_0900_ai_ci DEFAULT CHARSET=utf8mb4



CREATE TABLE localuser (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	username LONGTEXT NOT NULL, 
	password_hash BLOB NOT NULL, 
	enabled BIGINT NOT NULL, 
	PRIMARY KEY (id)
)ENGINE=InnoDB COLLATE utf8mb4_0900_ai_ci DEFAULT CHARSET=utf8mb4



CREATE TABLE student_topics (
	student_id INTEGER, 
	level VARCHAR(255), 
	subject VARCHAR(45), 
	examboard VARCHAR(45), 
	examcode VARCHAR(45), 
	examdate VARCHAR(45)
)ENGINE=InnoDB COLLATE utf8mb4_0900_ai_ci DEFAULT CHARSET=utf8mb4



CREATE TABLE subjects (
	id INTEGER NOT NULL, 
	level VARCHAR(45), 
	board VARCHAR(45), 
	subject VARCHAR(45), 
	examcode VARCHAR(45), 
	description VARCHAR(45), 
	examdate VARCHAR(45), 
	PRIMARY KEY (id)
)ENGINE=InnoDB COLLATE utf8mb4_0900_ai_ci DEFAULT CHARSET=utf8mb4



CREATE TABLE topics (
	id INTEGER NOT NULL, 
	subjectid INTEGER, 
	topic VARCHAR(255), 
	size VARCHAR(45), 
	hours INTEGER, 
	PRIMARY KEY (id)
)ENGINE=InnoDB COLLATE utf8mb4_0900_ai_ci DEFAULT CHARSET=utf8mb4



CREATE TABLE userinfo (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	email LONGTEXT NOT NULL, 
	user_id INTEGER NOT NULL, 
	created_at TEXT NOT NULL, 
	updated_at TEXT NOT NULL, 
	PRIMARY KEY (id)
)ENGINE=InnoDB COLLATE utf8mb4_0900_ai_ci DEFAULT CHARSET=utf8mb4

