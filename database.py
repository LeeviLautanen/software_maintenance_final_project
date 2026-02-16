import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ims.db")


def connect():
    return sqlite3.connect(DB_PATH)


def fetchall(query, params=()):
    con = connect()
    cur = con.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    con.close()
    return rows


def execute(query, params=()):
    con = connect()
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    con.close()
