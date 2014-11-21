# -*- coding: utf-8 -*-

import sqlite3
import os

class Database:
    def __init__(self, dbpath):
        database_exists = os.path.exists(dbpath)
        self.conn = sqlite3.connect(dbpath)
        if not database_exists:
            print("Creating database")
            self.create_db()

    def create_db(self):
        self.conn.execute("CREATE TABLE works (id INTEGER NOT NULL, \
                                               concert_id INTEGER NOT NULL, \
                                               composer TEXT NOT NULL, \
                                               work TEXT NOT NULL)")
 
        self.conn.execute("CREATE TABLE soloists (id INTEGER NOT NULL, \
                                                  concert_id TEXT NOT NULL, \
                                                  name TEXT NOT NULL)")
 
        self.conn.execute("CREATE TABLE festivals (id INTEGER NOT NULL, \
                                                   name TEXT NOT NULL)")
 
        self.conn.execute("CREATE TABLE dirigents (id INTEGER NOT NULL, \
                                                   concert_id INTEGER NOT NULL, \
                                                   name TEXT NOT NULL)")
 
        self.conn.execute("CREATE TABLE concerts (id INTEGER NOT NULL, \
                                                  festival_id INTEGER, \
                                                  date TEXT NOT NULL, \
                                                  state TEXT NOT NULL, \
                                                  city TEXT NOT NULL, \
                                                  hall TEXT NOT NULL, \
                                                  type TEXT, \
                                                  note TEXT)")
        self.conn.commit()
        print("Database successfuly created")

    def close(self):
        self.conn.close()