# business.py
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

class BusinessLayerError(Exception):
    """Safe error type for business-layer failures."""
    pass


class BusinessLayer:
    """
    Business layer class responsible for all database interactions.
    The GUI passes the connection info (server, database, user, password)
    into this class when it is created.
    """

    def __init__(self, host, dbname, user, password, port="5432"):
        """
        Constructor accepts the four items used to build the connection string.
        (Server = host, database = dbname, user, password, plus port.)
        """
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self._conn = None

    def connect(self):
        """Open the database connection if it is not already open."""
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
            )
            self._conn.autocommit = True

    def close(self):
        """Close the database connection cleanly."""
        if self._conn and not self._conn.closed:
            self._conn.close()

    # ---------- IN450a ----------

    def get_in450a_count(self):
        """Return the number of rows in table app.in450a."""
        try:
            self.connect()
            with self._conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM app.in450a;")
                (count,) = cur.fetchone()
                return count
        except Exception as e:
            raise BusinessLayerError(
                "Database operation failed. Please verify your login and permissions."
            ) from e


    def get_in450a_rows(self, limit=100):
        """Return some rows from in450a (col1..col6)."""
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

    # ---------- IN450b ----------

    def get_in450b_names(self, limit=None):
        """Return (first_name, last_name) from in450b."""
        self.connect()
        with self._conn.cursor() as cur:
            if limit is None:
                cur.execute("SELECT first_name, last_name FROM app.in450b;")
            else:
                cur.execute(
                    "SELECT first_name, last_name FROM app.in450b LIMIT %s;",
                    (limit,),
                )
            return cur.fetchall()

    def get_in450b_rows(self, limit=100):
        """Return (first_name, last_name, email, source, destination) from in450b."""
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

    # ---------- IN450c ----------

    def get_in450c_count(self):
        """Return the number of rows in table app.in450c."""
        self.connect()
        with self._conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM app.in450c;")
            (count,) = cur.fetchone()
            return count

    def get_in450c_rows(self, limit=100):
        """Optional helper: return rows from in450c."""
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
