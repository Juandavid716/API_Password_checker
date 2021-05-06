
from __future__ import print_function
import sqlite3
from sqlite3 import connect
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database, specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = connect(db_file)
        print("connected to database")
    except Error as e:
        print(e)

    return conn


# curs.execute("SELECT firstname, lastname FROM employees;")
# for firstname, lastname in curs.fetchall():
#     print(firstname, lastname)

# conn.close()