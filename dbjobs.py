# -*- coding: utf-8 -*-

import sqlite3
import os


class Database:
    def __init__(self, dbpath):
        database_exists = os.path.exists(dbpath)
        self.conn = sqlite3.connect(dbpath, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.cursor = self.conn.cursor()
        if not database_exists:
            print("Creating database")
            self.create_db()

    def last_id(self):
        self.cursor.execute("SELECT last_insert_rowid()")
        return self.cursor.fetchone()[0]

    def create_db(self):
        self.conn.execute("CREATE TABLE works (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                                               concert_id INTEGER NOT NULL, \
                                               composer TEXT NOT NULL, \
                                               work TEXT NOT NULL)")

        self.conn.execute("CREATE TABLE soloists (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                                                  work_id TEXT NOT NULL, \
                                                  name TEXT NOT NULL)")

        self.conn.execute("CREATE TABLE festivals (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                                                   name TEXT NOT NULL)")

        self.conn.execute("CREATE TABLE dirigents (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                                                   concert_id INTEGER NOT NULL, \
                                                   name TEXT NOT NULL)")

        self.conn.execute("CREATE TABLE choirs (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                                                   concert_id INTEGER NOT NULL, \
                                                   name TEXT NOT NULL)")

        self.conn.execute("CREATE TABLE concerts (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                                                  name TEXT, \
                                                  festival_id INTEGER, \
                                                  date_from TIMESTAMP NOT NULL, \
                                                  date_to TIMESTAMP NOT NULL, \
                                                  state TEXT NOT NULL, \
                                                  city TEXT NOT NULL, \
                                                  hall TEXT NOT NULL, \
                                                  type TEXT, \
                                                  note TEXT)")
        self.conn.commit()
        print("Database successfuly created")

    ### REMOVING DATA ###########################################################################################################################

    def remove_concert(self, id):
        self.cursor.execute("DELETE FROM concerts WHERE id = ?", (id,))
        self.conn.commit()

    def remove_soloists_for_work(self, work_id):
        self.cursor.execute("DELETE FROM soloists WHERE work_id = ?", (work_id,))
        self.conn.commit()

    def remove_dirigents_for_concert(self, id):
        self.cursor.execute("DELETE FROM dirigents WHERE concert_id = ?", (id,))
        self.conn.commit()

    def remove_choirs_for_concert(self, id):
        self.cursor.execute("DELETE FROM choirs WHERE concert_id = ?", (id,))
        self.conn.commit()

    def remove_works_for_concert(self, id):
        self.cursor.execute("DELETE FROM works WHERE concert_id = ?", (id,))
        self.conn.commit()

    ### ADDING DATA #############################################################################################################################

    def add_work(self, concert_id, composer, work):
        self.cursor.execute("INSERT INTO works(concert_id, composer, work) VALUES (?, ?, ?)", (concert_id, composer, work))
        self.conn.commit()

    def add_soloist(self, work_id, name):
        self.cursor.execute("INSERT INTO soloists(work_id, name) VALUES (?, ?)", (work_id, name))
        self.conn.commit()

    def add_festival(self, name):
        self.cursor.execute("INSERT INTO festivals(name) VALUES (?)", (name,))
        self.conn.commit()

    def add_dirigent(self, concert_id, name):
        self.cursor.execute("INSERT INTO dirigents(concert_id, name) VALUES (?, ?)", (concert_id, name))
        self.conn.commit()

    def add_choir(self, concert_id, name):
        self.cursor.execute("INSERT INTO choirs(concert_id, name) VALUES (?, ?)", (concert_id, name))
        self.conn.commit()

    def add_concert(self, name, festival_id, date_from, date_to, state, city, hall, type, note):
        self.cursor.execute("INSERT INTO concerts(name, festival_id, date_from, date_to, state, city, hall, type, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, festival_id, date_from, date_to, state, city, hall, type, note))
        self.conn.commit()
        return self.last_id()

    ### UPDATING DATA #############################################################################################################################

    def update_concert(self, id, name, festival_id, date_from, date_to, state, city, hall, type, note):
        self.cursor.execute("UPDATE concerts SET(name, festival_id, date_from, date_to, state, city, hall, type, note) WHERE id=?", (name, festival_id, date, state, city, hall, type, note))
        self.conn.commit()
        return self.last_id()

    ### FETCHING DATA #############################################################################################################################

    def get_all_concerts(self):
        self.cursor.execute("SELECT c.id, c.date_from as 'x [timestamp]', c.date_to as 'x [timestamp]', c.name, c.state, c.city, c.hall, c.type, c.note, f.name as festival, c.festival_id "
                            "FROM concerts c "
                            "LEFT JOIN festivals f ON f.id = c.festival_id "
                            "ORDER BY c.date_from DESC")
        return self.cursor.fetchall()

    def get_works(self, concert_id):
        self.cursor.execute("SELECT composer, work FROM works WHERE concert_id=?", (concert_id,))
        return self.cursor.fetchall()

    def get_soloists(self, work_id):
        self.cursor.execute("SELECT name FROM soloists WHERE work_id=?", (work_id,))
        return self.cursor.fetchall()

    def get_dirigents(self, concert_id):
        self.cursor.execute("SELECT name FROM dirigents WHERE concert_id=?", (concert_id,))
        return self.cursor.fetchall()

    def get_choirs(self, concert_id):
        self.cursor.execute("SELECT name FROM choirs WHERE concert_id=?", (concert_id,))
        return self.cursor.fetchall()

    def find_concerts(self, params):
        query = "SELECT name, festival_id, date_from, date_to, state, city, hall, type, note FROM concerts WHERE "
        i = 1
        for k in params:
            if (k in ["date_from", "date_to"]):
                continue
            #query += "({}={})".format(k, params[k])
            #if (i < len(params)):
                #query += " AND "
                #i = i + 1

            if (k == "name"):
                query += "(name='{}')".format(params[k])
            elif (k == "festival_id"):
                query += "(festival_id={})".format(params[k])
            elif (k == "state"):
                query += "(state='{}')".format(params[k])
            elif (k == "city"):
                query += "(city='{}')".format(params[k])
            elif (k == "hall"):
                query += "(hall='{}')".format(params[k])
            elif (k == "type"):
                query += "(type='{}')".format(params[k])
            elif (k == "note"):
                query += "(note='{}')".format(params[k])

            if (i < len(params)):
                query += " AND "
                i = i + 1

        if (("date_from" in params) and ("date_to" in params)):
            query += "(date_from >= {} AND date_to <= {})".format(params["date_from"], params["date_to"])

        print(query)


    ### FESTIVALS ###################################################################################################################################

    def get_all_festivals(self):
        self.cursor.execute("SELECT id, name FROM festivals ORDER BY name")
        return self.cursor.fetchall()

    def add_festival(self, name):
        self.cursor.execute("INSERT INTO festivals(name) VALUES (?)", (name,))
        self.conn.commit()
        return self.last_id()

    def remove_festival(self, id):
        self.cursor.execute("DELETE FROM festivals WHERE id = ?", (id,))
        self.conn.commit()

    ### AUTO COMPLETION #############################################################################################################################

    def get_completion_for_name(self, text):
        self.cursor.execute("SELECT DISTINCT name FROM concerts WHERE name LIKE '{}%' LIMIT 7".format(text))
        return self.cursor.fetchall()

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

    def get_completion_for_choir(self, text):
        self.cursor.execute("SELECT DISTINCT name FROM choirs WHERE name LIKE '{}%' LIMIT 7".format(text))
        return self.cursor.fetchall()

    def get_completion_for_soloist(self, text):
        self.cursor.execute("SELECT DISTINCT name FROM soloists WHERE name LIKE '{}%' LIMIT 7".format(text))
        return self.cursor.fetchall()

    def get_completion_for_festival(self, text):
        self.cursor.execute("SELECT DISTINCT name FROM festivals WHERE name LIKE '{}%' LIMIT 7".format(text))
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
        self.cursor.execute("SELECT * FROM choirs")
        print(self.cursor.fetchall())
        self.cursor.execute("SELECT * FROM concerts")
        print(self.cursor.fetchall())

    def close(self):
        self.conn.close()

# End of dbjobs.py
