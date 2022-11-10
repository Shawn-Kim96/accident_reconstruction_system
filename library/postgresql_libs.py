import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("POSTGRESQL_HOST")
DBNAME = os.getenv("POSTGRESQL_DBNAME")
USER = os.getenv("POSTGRESQL_USER")
PW = os.getenv("POSTGRESQL_PW")


class PostgreSQL:
    def __init__(self, host=HOST, dbname=DBNAME, user=USER, pw=PW, port=5432):
        self.db = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=pw,
            port=port
        )
        self.cursor = self.db.cursor()  # allow python code to execute PostgreSQL command in a database session

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self, query, **args):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()

    def create_tables(self, sql_command_list):
        """create tables in PostgreSQL database"""
        try:
            for command in sql_command_list:
                self.cursor.execute(command)
            self.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert(self, schema, table, column: list, data: list, if_conflict_do_nothing=False, if_conflict_update=False):
        column_string = ', '.join(column)
        data_string = ', '.join([f"'{x}'" if (type(x) == str and x[-1] != ']') else str(x) for x in data])
        sql = f"INSERT INTO {schema}.{table} ({column_string}) VALUES ({data_string}) ;"
        if if_conflict_do_nothing:
            sql = f"INSERT INTO {schema}.{table} ({column_string}) VALUES ({data_string}) ON CONFLICT DO NOTHING;"
        if if_conflict_update:
            sql = f"INSERT INTO {schema}.{table} ({column_string}) VALUES ({data_string}) ON CONFLICT DO UPDATE;"
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(" insert DB err ", e)

    def read(self, schema, table, column):
        sql = f"SELECT {column} from {schema}.{table}"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            result = (" read DB err", e)
        return result

    def update(self, schema, table, column, value, condition):
        sql = f"UPDATE {schema}.{table} SET {column}='{value}' WHERE {column}='{condition}'"
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(" update DB err", e)

    def delete(self, schema, table, condition):
        sql = f" delete from {schema}.{table} where {condition} ; "
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("delete DB err", e)