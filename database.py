import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = "ims.db"
DB_PATH = os.path.join(BASE_DIR, DB_NAME)


def connect(db_path=None):
    if db_path is None:
        db_path = DB_PATH
    return sqlite3.connect(db_path)


def fetchall(query, params=()):
    con = connect()
    try:
        cur = con.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        con.close()
    except Exception as e:
        con.close()
        raise e
    return rows


def execute(query, params=()):
    con = connect()
    try:
        cur = con.cursor()
        cur.execute(query, params)
        con.commit()
        con.close()
    except Exception as e:
        con.close()
        raise e


def initialize_db(db_name=None):
    if db_name is None:
        db_name = DB_NAME

    con = sqlite3.connect(database=db_name)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)"
    )
    con.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)"
    )
    con.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)"
    )
    con.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text, Supplier text,name text,price text,qty text,status text)"
    )
    con.commit()
    con.close()
