import logging
import sqlite3

from db_data import bakery, types


class DB_BakeryProducts:
    conn = sqlite3.connect("bakery.db")
    cur = conn.cursor()

    def create_table(self):
        self.cur.executescript("""
        CREATE TABLE IF NOT EXISTS types(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
         );
        CREATE TABLE IF NOT EXISTS bakery(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            path_photo TEXT NOT NULL,
            type_id INTEGER NOT NULL,
            FOREIGN KEY (type_id) REFERENCES types(id)
        );
        """)

    def add_data(self, name_table, data):
        elm = "?, " * (len(data[0]) - 1)
        self.cur.executemany(f"INSERT OR IGNORE INTO {name_table} VALUES({elm}?);", data)

    def get_cake_descr_path(self, name_bakery):
        try:
            get_position = ''f'SELECT description, path_photo FROM bakery WHERE name = "{name_bakery}"'''
            res = self.cur.execute(get_position)
            row = res.fetchone()
            return row
        except TypeError:
            logging.info(f"{name_bakery} нет в базе")

    def save_close(self):
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    db = DB_BakeryProducts()
    db.create_table()
    db.add_data("types", types)
    db.add_data("bakery", bakery)
    db.save_close()
