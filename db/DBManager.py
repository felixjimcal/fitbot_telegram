import sqlite3
import sys

DB_PATH = './db/db_fbw.db'


class DBManager:
    conn = None
    cursorObj = None

    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursorObj = conn.cursor()
        cursorObj.execute('CREATE TABLE IF NOT EXISTS "customers" ("telegram_id" INTEGER NOT NULL UNIQUE, "name" INTEGER NOT NULL,	"email"	TEXT NOT NULL UNIQUE, "date_signup"	INTEGER NOT NULL, PRIMARY KEY("telegram_id"));').fetchall()
        cursorObj.execute('CREATE TABLE IF NOT EXISTS "routines" ("telegram_id" INTEGER NOT NULL UNIQUE, "routine" INTEGER NOT NULL UNIQUE, PRIMARY KEY("teelgram_id"));').fetchall()
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('Fail in DBManager:', ex.args, 'line:', exc_tb.tb_lineno)
        conn.close()

    @classmethod
    def connect_to_db(cls):
        try:
            cls.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cls.cursorObj = cls.conn.cursor()
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print('Fail in DBManager:', ex.args, 'line:', exc_tb.tb_lineno)
            cls.conn.close()

    @classmethod
    def is_customer_in_db(cls, user_id):
        try:
            if cls.conn is None:
                cls.connect_to_db()
            result = cls.cursorObj.execute('SELECT * FROM customers WHERE telegram_id =' + str(user_id) + ';').fetchall()
            return True if len(result) > 0 else False
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print('Fail in DBManager:', ex.args, 'line:', exc_tb.tb_lineno)
            cls.conn.close()

    @classmethod
    def insert_customer(cls, telegram_id, customer_name, contact_email, charge_date):
        try:
            if cls.conn is None:
                cls.connect_to_db()
            cls.cursorObj.execute('INSERT INTO customers VALUES (' + str(telegram_id) + ',"' + customer_name + '","' + contact_email + '",' + str(charge_date) + ');')
            cls.conn.commit()
            return True if cls.cursorObj.lastrowid == telegram_id else False
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print('Fail in DBManager:', ex.args, 'line:', exc_tb.tb_lineno)
            cls.conn.close()

    @classmethod
    def load_customer_routine(cls, telegram_id):
        try:
            if cls.conn is None:
                cls.connect_to_db()
            result = cls.cursorObj.execute('SELECT routine FROM routines WHERE telegram_id =' + str(telegram_id) + ';').fetchall()
            return result
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print('Fail in DBManager:', ex.args, 'line:', exc_tb.tb_lineno)
            cls.conn.close()
