# business.py
import os
from dotenv import load_dotenv
import psycopg2

# Load values from .env file (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "in450db")
DB_USER = os.getenv("DB_USER", "app_user")
DB_PASS = os.getenv("DB_PASS", "")


class BusinessLayer:
    """
    Business layer class responsible for all database interactions.
    All GUI / presentation code should call methods in this class
    instead of talking to the database directly.
    """

    def __init__(self):
        self._conn = None

    def connect(self):
        """Open the database connection if it is not already open."""
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
            )

    def close(self):
        """Close the database connection cleanly."""
        if self._conn and not self._conn.closed:
            self._conn.close()

    # ---------------- in450a ----------------

    def get_in450a_count(self):
        """
        Return the number of rows in table app.in450a.
        Used by the GUI button that shows the row count.
        """
        self.connect()
        with self._conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM app.in450a;")
            (count,) = cur.fetchone()
            return count

    def get_in450a_rows(self, limit=100):
        """
        Return raw rows from app.in450a.
        Each row is a tuple: (col1, col2, col3, col4, col5, col6)
        """
        self.connect()
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT col1, col2, col3, col4, col5, col6
                FROM app.in450a
                LIMIT %s;
                """,
                (limit,),
            )
            return cur.fetchall()

    # ---------------- in450b ----------------

    def get_in450b_names(self, limit=None):
        """
        Return a list of (first_name, last_name) tuples from app.in450b.
        This is used by the GUI button that shows first and last names.
        """
        self.connect()
        with self._conn.cursor() as cur:
            if limit is None:
                cur.execute(
                    "SELECT first_name, last_name FROM app.in450b;"
                )
            else:
                cur.execute(
                    "SELECT first_name, last_name FROM app.in450b LIMIT %s;",
                    (limit,),
                )
            rows = cur.fetchall()
            return rows

    def get_in450b_rows(self, limit=100):
        """
        Return full rows from app.in450b.
        Each row is: (first_name, last_name, email, source, destination)
        """
        self.connect()
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT first_name, last_name, email, source, destination
                FROM app.in450b
                LIMIT %s;
                """,
                (limit,),
            )
            return cur.fetchall()

    # ---------------- in450c  ----------------

    def get_in450c_rows(self, limit=100):
        """
        Return full rows from app.in450c.
        Each row is: (AppID, AppName, AppVersion, source, destination, DigSig)
        """
        self.connect()
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT AppID, AppName, AppVersion, source, destination, DigSig
                FROM app.in450c
                LIMIT %s;
                """,
                (limit,),
            )
            return cur.fetchall()


if __name__ == "__main__":
    # Simple test when you run this file directly from the terminal
    b = BusinessLayer()
    try:
        print("in450a count:", b.get_in450a_count())
        print("First 5 names from in450b:", b.get_in450b_names(limit=5))
    finally:
        b.close()
