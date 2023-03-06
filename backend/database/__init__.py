import sys
import pandas as pd
import streamlit as st
# import sqlite3
# import pymysql
# import MySQLdb
# import mysql.connector
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db


class MySqlInitConnection:

    # just to declare to methods recieve general orm model

    def __init__(self, engine=None) -> None:
        if engine is None:
            self.engine = self.__init_connection()
        else:
            self.engine = engine
        self.Session = sessionmaker(bind=self.engine)

    @staticmethod
    @st.cache_resource
    def __init_connection():
        LSCT = list(st.secrets["mysql"].values())
        str_connection = f'mysql://{LSCT[-2]}:{LSCT[-1]}@{LSCT[0]}/{LSCT[-3]}'
        return create_engine(str_connection)
        # return mysql.connector.connect(**st.secrets["mysql"])
        # return MySQLdb.Connection(**st.secrets["mysql"])

    def create_table_sql(self, df, tbname):
        # Generate a SQL schema string based on the DataFrame columns
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        # df, tbname, con=self.conn).replace('"', '`')

        schema = pd.io.sql.get_schema(
            df, tbname, con=self.engine).replace('"', '`')
        schema = schema.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS ')
        with self.engine.connect() as conn:
            conn.execute(text(schema))

    def run_query(self, query, *args):
        """run query with self.engine, it's select stuff...
        - Select statements
        Args:
            query (_type_): _description_

        Returns:
            _type_: _description_
        """
        with self.engine.connect() as conn:
            results = conn.execute(text(query), *args)
            return results.fetchall()

    def commit_text_query(self, query, *args):
        """### INSERT, UPDATE, DELETE

        Args:
            query (string): the query to insert update or delete
        """
        with self.engine.connect() as conn:
            conn.execute(text(query), *args)
            conn.commit()

    def call_procedure(self, query, args):
        with self.engine.connect() as conn:
            results = conn.execute(text("CALL " + query), *args)
            return [result.fetchall() for result in results]

    def pd_read_sql(self, query) -> pd.read_sql:
        return pd.read_sql(text(query), self.engine.connect())

    def pd_sql_query_select(self, *fields):
        with self.engine.connect() as conn:
            df = pd.read_sql_query(
                db.select(
                    *fields
                ), conn

            )
            return df

    def pd_insert_df_to_mysql(self, df: pd.DataFrame, tb_name: str, if_exists="replace"):
        """this method inserts Dataframe into mysql
        Args:
            df (pd.DataFrame): pandas Dataframe that is going to be created in mysql
            tb_name (str): table name to be created before, it'll be created only if not exists
            if_exists (str, optional): if_exists pd.to_sql argument. Defaults to "replace".
        """
        self.create_table_sql(df, tb_name)

        df.to_sql(name=tb_name, con=self.engine,
                  if_exists=if_exists, index=False)
