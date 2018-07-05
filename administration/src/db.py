import sqlite3
from .config import DATABASE_URI


class SqliteManager:
    @staticmethod
    def get_db():
        print(DATABASE_URI)
        db = sqlite3.connect(database=DATABASE_URI, timeout=5)
        return db

    @staticmethod
    def close_connection(db):
        if db is not None:
            db.close()

    @staticmethod
    def db_init():
        db = SqliteManager.get_db()
        db.executescript('''
            DROP TABLE IF EXISTS UserSession;
            DROP TABLE IF EXISTS AuthUser;
            DROP TABLE IF EXISTS Session;
            DROP TABLE IF EXISTS User;
            DROP TABLE IF EXISTS UserRole;
            DROP TABLE IF EXISTS ImageStore;
            DROP TABLE IF EXISTS Key;

            PRAGMA foreign_keys = "1";

            CREATE TABLE Key (
                id            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                tag_id        INTEGER UNIQUE,
                room_id       INTEGER NOT NULL,
                block_name    TEXT,
                sector_name   TEXT,
                floor         INTEGER NOT NULL,
                room_repr     TEXT NOT NULL
            );

            CREATE TABLE UserRole (
                id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                name       TEXT
            );

            CREATE TABLE ImageStore (
                id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                name        TEXT NOT NULL,
                location    TEXT NOT NULL,
                UNIQUE(name, location)
            );

            CREATE TABLE User (
                id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                tag_id          INTEGER NOT NULL UNIQUE,
                first_name      TEXT,
                last_name       TEXT,
                email           TEXT,
                role_id         INTEGER NOT NULL,
                pic_id          INTEGER NOT NULL,
                FOREIGN KEY (pic_id) REFERENCES ImageStore(id),
                FOREIGN KEY (role_id) REFERENCES UserRole(id)
            );

            CREATE TABLE AuthUser (
                id            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                user_id       INTEGER NOT NULL UNIQUE,
                password      TEXT,
                FOREIGN KEY (user_id) REFERENCES User(id)
            );

            CREATE TABLE UserSession (
                id            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                user_id       INTEGER NOT NULL UNIQUE,
                timestamp     TEXT,
                UNIQUE(user_id, timestamp),
                FOREIGN KEY (user_id) REFERENCES User(id)
            );

            CREATE TABLE Session (
                id                 INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                key_id             INTEGER NOT NULL,
                user_id            INTEGER NOT NULL,
                started_on         TEXT,
                closed_on          TEXT,
                UNIQUE(key_id, user_id, started_on),
                FOREIGN KEY(key_id) REFERENCES Key(id),
                FOREIGN KEY(user_id) REFERENCES User(id)
            );

            INSERT INTO UserRole (name) VALUES ("admin");
            INSERT INTO UserRole (name) VALUES ("profesor");
            INSERT INTO UserRole (name) VALUES ("student");
            INSERT INTO ImageStore (name, location) VALUES ('/static/images/default.png', 'default');
            ''')
        db.commit()
        SqliteManager.close_connection(db)
