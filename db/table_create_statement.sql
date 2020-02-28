CREATE TABLE IF NOT EXISTS user 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username varchar(20) UNIQUE NOT NULL,
    email varchar(50) UNIQUE NOT NULL,
    password varchar(80) NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE);
