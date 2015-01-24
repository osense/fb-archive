# -*- coding: utf-8 -*-

## This file is part of fb-archive.

## fb-archive is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## fb-archive is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with fb-archive.  If not, see <http://www.gnu.org/licenses/>.

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
                                                  concert_id INTEGER NOT NULL, \
                                                  work_id INTEGER NOT NULL, \
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

    def remove_soloists_for_concert(self, concert_id):
        self.cursor.execute("DELETE FROM soloists WHERE concert_id = ?", (concert_id,))
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

    def remove_festival(self, id):
        self.cursor.execute("DELETE FROM festivals WHERE id = ?", (id,))
        self.conn.commit()

    ### ADDING DATA #############################################################################################################################

    def add_work(self, concert_id, composer, work):
        self.cursor.execute("INSERT INTO works(concert_id, composer, work) VALUES (?, ?, ?)", (concert_id, composer, work))
        self.conn.commit()
        return self.last_id()

    def add_soloist(self, concert_id, work_id, name):
        self.cursor.execute("INSERT INTO soloists(concert_id, work_id, name) VALUES (?, ?, ?)", (concert_id, work_id, name))
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

    def update_concert(self, concert_id, name, festival_id, date_from, date_to, state, city, hall, type, note):
        self.cursor.execute("UPDATE concerts SET name = ?, "
                                                "festival_id = ?, "
                                                "date_from = ?, "
                                                "date_to = ?, "
                                                "state = ?, "
                                                "city = ?, "
                                                "hall = ?, "
                                                "type = ?, "
                                                "note = ? "
                                                "WHERE id=?", (name, festival_id, date_from, date_to, state, city, hall, type, note, concert_id))
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
        self.cursor.execute("SELECT id, composer, work FROM works WHERE concert_id=? ORDER BY composer", (concert_id,))
        return self.cursor.fetchall()

    def get_soloists_for_concert(self, concert_id):
        self.cursor.execute("SELECT name FROM soloists WHERE concert_id=? ORDER BY name", (concert_id,))
        return self.cursor.fetchall()

    def get_soloists_for_work(self, work_id):
        self.cursor.execute("SELECT id, name FROM soloists WHERE work_id=? ORDER BY name", (work_id,))
        return self.cursor.fetchall()

    def get_dirigents(self, concert_id):
        self.cursor.execute("SELECT id, name FROM dirigents WHERE concert_id=? ORDER BY name", (concert_id,))
        return self.cursor.fetchall()

    def get_choirs(self, concert_id):
        self.cursor.execute("SELECT id, name FROM choirs WHERE concert_id=? ORDER BY name", (concert_id,))
        return self.cursor.fetchall()

    ## TODO: Intersection of concert_ids
    def find_concerts(self, params):
        joins = ""
        if ("festival" in params):
            joins += "LEFT JOIN festivals f"
        query = ("SELECT c.id, c.date_from as 'x [timestamp]', c.date_to as 'x [timestamp]', c.name, c.state, c.city, c.hall, c.type, c.note, f.name as festival, c.festival_id "
                "FROM concerts c "
                "LEFT JOIN festivals f ON f.id = c.festival_id "
                "WHERE ")

        concert_ids = set()
        for k in params:
            if (k in ["name", "state", "city", "hall", "type"]):
                query += "(c.{} LIKE '{}%') AND ".format(k, params[k])
            elif (k is "note"):
                query += "(c.note LIKE '%{}%') AND ".format(params[k])

            elif (k is "composer"):
                self.cursor.execute("SELECT concert_id FROM works WHERE composer LIKE ?", (params[k] + '%',))
                ids = self.cursor.fetchall()
                if (ids):
                    [concert_ids.add(x[0]) for x in ids]
            elif (k is "work"):
                self.cursor.execute("SELECT concert_id FROM works WHERE work LIKE ?", (params[k] + '%',))
                ids = self.cursor.fetchall()
                if (ids):
                    [concert_ids.add(x[0]) for x in ids]
            elif (k is "soloist"):
                self.cursor.execute("SELECT concert_id FROM soloist WHERE name LIKE ?", (params[k] + '%',))
                ids = self.cursor.fetchall()
                if (ids):
                    [concert_ids.add(x[0]) for x in ids]
            elif (k is "dirigent"):
                self.cursor.execute("SELECT concert_id FROM dirigents WHERE name LIKE ?", (params[k] + '%',))
                ids = self.cursor.fetchall()
                if (ids):
                    [concert_ids.add(x[0]) for x in ids]
            elif (k is "choir"):
                self.cursor.execute("SELECT concert_id FROM choirs WHERE name LIKE ?", (params[k] + '%',))
                ids = self.cursor.fetchall()
                if (ids):
                    [concert_ids.add(x[0]) for x in ids]

        if (("date_from" in params) and ("date_to" in params)):
            query += "(date_from >= datetime('{}') AND date_to <= datetime('{}')) AND ".format(params["date_from"], params["date_to"])

        if ("festival" in params):
            self.cursor.execute("SELECT id FROM festivals WHERE name LIKE ?", (params["festival"] + '%',))
            ids = self.cursor.fetchall()
            if (ids):
                ids = [x[0] for x in ids]
                query += "(c.festival_id IN ({})) AND ".format(str(ids)[1:-1])

        if not (concert_ids == set()):
            print(concert_ids)
            query += "(c.id IN ({})) AND ".format(str(concert_ids)[1:-1])

        if (query.endswith(" AND ")):
            query = query[:-5]

        print(query)
        self.cursor.execute(query + " ORDER BY c.date_from DESC")
        return self.cursor.fetchall()

    def universal_search(self, params):
        query = ("SELECT DISTINCT c.id, "
                        "c.date_from as 'x [timestamp]', "
                        "c.date_to as 'x [timestamp]', "
                        "c.name, "
                        "c.state, "
                        "c.city, "
                        "c.hall, "
                        "c.type, "
                        "c.note, "
                        "f.name as festival, "
                        "c.festival_id "
                 "FROM concerts c "
                 "LEFT JOIN festivals f ON f.id = c.festival_id "
                 "LEFT JOIN dirigents d ON d.concert_id = c.id "
                 "LEFT JOIN choirs ch ON ch.concert_id = c.id "
                 "LEFT JOIN works w ON w.concert_id = c.id "
                 "LEFT JOIN soloists s ON s.work_id = w.id "
                 "WHERE ")
        # Parsing params
        if 'date_from' in params.keys():
            query += "c.date_from >= datetime('{}') AND c.date_to <= datetime('{}') AND ".format(params['date_from'], params['date_to'])
        if 'name' in params.keys():
            query += "c.name LIKE '{}%' AND ".format(params['name'])
        if 'state' in params.keys():
            query += "c.state LIKE '{}%' AND ".format(params['state'])
        if 'city' in params.keys():
            query += "c.city LIKE '{}%' AND ".format(params['city'])
        if 'hall' in params.keys():
            query += "c.hall LIKE '{}%' AND ".format(params['hall'])
        if 'type' in params.keys():
            query += "c.type LIKE '{}%' AND ".format(params['type'])
        if 'festival' in params.keys():
            query += "c.festival_id = {} AND ".format(params['festival'])
        if 'composer' in params.keys():
            query += "w.composer LIKE '{}%' AND ".format(params['composer'])
        if 'work' in params.keys():
            query += "w.work LIKE '{}%' AND ".format(params['work'])
        if 'soloist' in params.keys():
            query += "s.name LIKE '{}%' AND ".format(params['soloist'])
        if 'dirigent' in params.keys():
            query += "d.name LIKE '{}%' AND ".format(params['dirigent'])
        if 'choir' in params.keys():
            query += "ch.name LIKE '{}%' AND ".format(params['choir'])
        if 'note' in params.keys():
            query += "c.note LIKE '%{}%' AND ".format(params['note'])

        query += "1 "
        query += "ORDER BY c.date_from DESC"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    ### FESTIVALS ###################################################################################################################################

    def get_all_festivals(self):
        self.cursor.execute("SELECT id, name FROM festivals ORDER BY name")
        return self.cursor.fetchall()

    def add_festival(self, name):
        self.cursor.execute("INSERT INTO festivals(name) VALUES (?)", (name,))
        self.conn.commit()
        return self.last_id()

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
