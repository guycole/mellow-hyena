"""mellow hyena sqlite3 support"""

import sqlite3
from sqlite3 import Error

from typing import Dict

class SqlLite:
    """mellow hyena sqlite3 support"""

    db_connection = None

    def __init__(self, db_connection: sqlite3.Connection):
        self.db_connection = db_connection
        print(self.db_connection)

    def load_log_insert(self, args: Dict[str, str]):
        """load_log insert row"""

        sql = "insert into hyena_loadlog (file_name, load_time, obs_time, population) values (?, ?, ?, ?)"
        values = (args["file_name"], args["load_time"], args["obs_time"], args["population"])

#        , ('{args['file_name']}', '{args['load_time']}', '{args['obs_time']}', {args['population']})"
        print(sql)
        print(values)

        cursor = self.db_connection.cursor()
        print(cursor)
        cursor.execute(sql, values)
        self.db_connection.commit()

    def load_log_select(self, file_name: str):
        """load_log select row"""

        cursor = self.db_connection.cursor()
        rows = cursor.execute("select id, file_name, load_time, obs_time, population from hyena_loadlog where file_name = ?", (file_name,)).fetchall()
        print(rows)