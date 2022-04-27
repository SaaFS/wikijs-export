import argparse
import os
import sqlite3
import sys

import psycopg2
from psycopg2._psycopg import cursor, connection

from .config import Settings, BASE_DIR
from .parser import PageParser

parser = argparse.ArgumentParser()

parser.add_argument("--backend", default="postgres", help="Select the backend database for dumping sqlite|postgres"
                                                          "Default: postgres")
parser.add_argument("-i", "--input", default="../blog_data/og_wiki.sqlite",
                    help="Required when backend is set to sqlite"
                         "Default: ../blog_data/og_wiki.sqlite")

args = parser.parse_args()

if __name__ == "__main__":
   settings = Settings()
   conn: connection | sqlite3.Connection

   match args.backend:
      case "postgres":
         print("Setting backend to PostgreSQL")
         conn = psycopg2.connect(
            host=settings.db_host,
            dbname=settings.db_database,
            user=settings.db_user,
            password=settings.db_password,
            port=settings.db_port,
         )

      case "sqlite":
         print("Setting backend to sqlite")
         database_path = (BASE_DIR / args.input).resolve()
         if os.path.exists(database_path):
            try:
               conn = sqlite3.connect(database_path)
            except sqlite3.OperationalError as exc:
               print(f"SQLite DB connection error: Error: {exc} Path: {database_path}")
               sys.exit(1)
         else:
            print(f"Database at {database_path} does not exist")
            sys.exit(1)

   if conn:
      cur: cursor = conn.cursor()

      cur.execute("SELECT * FROM pages;")

      pages = cur.fetchall()

      cur.execute("SELECT * FROM users;")

      users = cur.fetchall()

      parser = PageParser(pages, users)

   else:
      print("Failed to connect to backend database")
