DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS films;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE films (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user INTEGER NOT NULL REFERENCES users(id),
    title TEXT NOT NULL,
    tagline TEXT,
    director TEXT,
    poster TEXT,
    release_year INTEGER,
    genre TEXT,
    watched BOOLEAN,
    rating INTEGER,
    review TEXT
);