# -*- coding: utf-8 -*-

import sqlite3
import os

class Database:
    def __init__(self, dbpath):
        database_exists = os.path.exists(dbpath)
        self.conn = sqlite3.connect(dbpath)
        self.cursor = self.conn.cursor()
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

    def add_work(self, concert_id, composer, work):
        id = self.get_next_id("works")
        self.cursor.execute("INSERT INTO works VALUES (?, ?, ?, ?)", (id, concert_id, composer, work))
        self.conn.commit()

    def add_soloist(self, concert_id, name):
        id = self.get_next_id("soloists")
        self.cursor.execute("INSERT INTO soloists VALUES (?, ?, ?)", (id, concert_id, name))
        self.conn.commit()

    def add_festival(self, name):
        id = self.get_next_id("festivals")
        self.cursor.execute("INSERT INTO festivals VALUES (?, ?)", (id, name))
        self.conn.commit()

    def add_dirigent(self, concert_id, name):
        id = self.get_next_id("dirigents")
        self.cursor.execute("INSERT INTO dirigents VALUES (?, ?, ?)", (id, concert_id, name))
        self.conn.commit()

    def add_concert(self, festival_id, date, state, city, hall, type, note):
        id = self.get_next_id("concerts")

        self.cursor.execute("INSERT INTO concerts VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, festival_id, date, state, city, hall, type, note))
        self.conn.commit()
        return id

    def get_next_id(self, table):
        self.cursor.execute("SELECT MAX(id) FROM {0}".format(table))
        id = self.cursor.fetchone()
        if (id[0] is None):
            id = 0
        else:
            id = id[0] + 1
        return id

    ### AUTO COMPLETION #############################################################################################################################

    def get_completion_for_state(self, text):
        self.cursor.execute("SELECT DISTINCT state FROM concerts WHERE state LIKE '{}%' LIMIT 7".format(text))
        return self.cursor.fetchall()

    def get_completion_for_city(self, text):
        self.cursor.execute("SELECT DISTINCT city FROM concerts WHERE city LIKE '{}%' LIMIT 7".format(text))
        return self.cursor.fetchall()

    def get_completion_for_hall(self, text):
        self.cursor.execute("SELECT DISTINCT hall FROM concerts WHERE hall LIKE '{}%' LIMIT 7".format(text))
        return self.cursor.fetchall()

    def get_completion_for_type(self, text):
        self.cursor.execute("SELECT DISTINCT type FROM concerts WHERE type LIKE '{}%' LIMIT 7".format(text))
        return self.cursor.fetchall()

    def get_completion_for_composer(self, text):
        self.cursor.execute("SELECT DISTINCT composer FROM works WHERE composer LIKE '{}%' LIMIT 7".format(text))
        return self.cursor.fetchall()

    def get_completion_for_work(self, text):
        self.cursor.execute("SELECT DISTINCT work FROM works WHERE work LIKE '{}%' LIMIT 7".format(text))
        return self.cursor.fetchall()

    def get_completion_for_dirigent(self, text):
        self.cursor.execute("SELECT DISTINCT name FROM dirigents WHERE name LIKE '{}%' LIMIT 7".format(text))
        return self.cursor.fetchall()

    def get_completion_for_soloist(self, text):
        self.cursor.execute("SELECT DISTINCT name FROM soloists WHERE name LIKE '{}%' LIMIT 7".format(text))
        return self.cursor.fetchall()

    ### OTHER #######################################################################################################################################

    def debug_print(self):
        self.cursor.execute("SELECT * FROM works")
        print(self.cursor.fetchall())
        self.cursor.execute("SELECT * FROM soloists")
        print(self.cursor.fetchall())
        self.cursor.execute("SELECT * FROM festivals")
        print(self.cursor.fetchall())
        self.cursor.execute("SELECT * FROM dirigents")
        print(self.cursor.fetchall())
        self.cursor.execute("SELECT * FROM concerts")
        print(self.cursor.fetchall())

    def close(self):
        self.conn.close()
