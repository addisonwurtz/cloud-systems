"""
A simple guestbook flask app.
Data is stored in a SQLite database that looks something like the following:

+------------+------------------+------------+----------------+
| Name       | Email            | signed_on  | message        |
+============+==================+============+----------------+
| John Doe   | jdoe@example.com | 2012-05-28 | Hello world    |
+------------+------------------+------------+----------------+

This can be created with the following SQL (see bottom of this file):

    create table guestbook (name text, email text, signed_on date, message);

"""
from datetime import date
from .Model import Model
import sqlite3

DB_FILE = 'entries.db'  # file for our Database


class model(Model):
    def __init__(self):
        # Make sure our database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from quotebook")
        except sqlite3.OperationalError:
            cursor.execute("create table quotebook (quote text, attribution text, rating number, date_added date)")
        cursor.close()

    def select(self):
        """
        Gets all rows from the database
        Each row contains: quote, attribution, rating, date_added
        :return: List of lists containing all rows of database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM quotebook")
        return cursor.fetchall()

    def insert(self, quote, attribution, rating):
        """
        Inserts entry into database
        :param quote: String
        :param attribution: String
        :param rating: float
        :return: True
        :raises: Database errors on connection and insertion
        """
        params = {'quote': quote, 'attribution': attribution, 'rating': rating, 'date_added': date.today()}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute(
            "insert into quotebook (quote, attribution, rating, date_added) VALUES (:quote, :attribution, :rating, :date_added)",
            params)

        connection.commit()
        cursor.close()
        return True
