
from scripts.init_database import engine_alc_str
import MySQLdb
from sqlalchemy import create_engine
from default.interact import press_key_b4
from pgdas_fiscal_oesk.ginfess_excel_values import ExcelValuesPreensh
from pgdas_fiscal_oesk.rotina_dividas_v3 import dividas_ativas_complete as rotina_dividas
from pgdas_fiscal_oesk.send_dividas import SendDividas
from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
from pgdas_fiscal_oesk.silas_abre_g5_loop_v10 import G5
# from pgdas_fiscal_oesk.silas_abre_g5_loop_v9_iss import G5
from pgdas_fiscal_oesk.gias import GIA

from default.sets import get_compt
from default.sets import Initial
from default.sets import get_all_valores

# from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
# from pgdas_fiscal_oesk.rotina_pgdas_v3 import PgdasDeclaracao as PgdasDeclaracaoFull
# from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
# from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui
# from selenium.common.exceptions import UnexpectedAlertPresentException
# from pgdas_fiscal_oesk.silas_jr import JR

import sys
import pandas as pd
import streamlit as st
# import mysql.connector
import sqlite3
import pymysql
# import MySQLdb
import mysql.connector
from sqlalchemy import create_engine, text


class SqlInit:
    def __init__(self) -> None:
        self.mysql_conn = self.__init_connection()
        self.engine_alc = self.__create_alc_engine()
    # self.conn.commit()

    @staticmethod
    @st.experimental_singleton
    def __init_connection():
        # return mysql.connector.connect(**st.secrets["mysql"])
        return MySQLdb.Connection(**st.secrets["mysql"])

    @staticmethod
    @st.experimental_singleton
    def __create_alc_engine() -> create_engine:
        import mysql.connector
        LSCT = list(st.secrets["mysql"].values())  # ListSeCreTs
        # sqlachemy connection
        str_connection = f'mysql://{LSCT[-2]}:{LSCT[-1]}@{LSCT[0]}/{LSCT[-3]}'
        return create_engine(str_connection)

    def create_table_sql(self, df, tbname):
        # Generate a SQL schema string based on the DataFrame columns
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        # df, tbname, con=self.conn).replace('"', '`')

        schema = pd.io.sql.get_schema(
            df, tbname, con=self.engine_alc).replace('"', '`')
        schema = schema.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS ')
        cursor = self.mysql_conn.cursor()
        cursor.execute(schema)

    def run_query(self, query, *args):
        """run query with self.mysql_conn, it's select stuff...

        Args:
            query (_type_): _description_

        Returns:
            _type_: _description_
        """
        with self.mysql_conn.cursor() as cur:
            cur.execute(query, *args)
            return cur.fetchall()

    def commit_query(self, query, *args):
        with self.mysql_conn.cursor() as cur:
            cur.execute(query, *args)
            self.mysql_conn.commit()

    def call_procecure(self, query, args):
        with self.mysql_conn.cursor() as cur:
            cur.callproc(query, args)

            return [result.fetchall() for result in cur.stored_results()]

    def pd_read_sql(self, query) -> pd.read_sql:
        # s_settings_df = pd.DataFrame(
        #     self.engine_alc.connect().execute(text(query)))
        return pd.read_sql(text(query), self.engine_alc.connect())

    def pd_insert_df_to_mysql(self, df: pd.DataFrame, tb_name: str, if_exists="replace"):
        """this method inserts Dataframe into mysql
        Args:
            df (pd.DataFrame): pandas Dataframe that is going to be created in mysql
            tb_name (str): table name to be created before, it'll be created only if not exists
            if_exists (str, optional): if_exists pd.to_sql argument. Defaults to "replace".
        """
        self.__create_table_sql(df, tb_name)

        df.to_sql(name=tb_name, con=self.engine_alc,
                  if_exists=if_exists, index=False)


class Consulta(Initial, SqlInit):
    # mysql_conn = init_connection()
    import pymysql

    def __init__(self, compt=None) -> None:
        super().__init__()
        self.compt = compt
        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='main'"
        # Create SQLAlchemy engine using the connection string

        df = self.pd_read_sql(query)

        # s_settings_df = pd.DataFrame(self.engine.connect().execute(text(query)))
        # pd.read_sql(query, self.mysql_conn)

    def __creation_of_db(self):
        compt = self.compt
        self.MAIN_FOLDER = self.getset_folderspath()
        self.MAIN_FILE = self.getset_folderspath(False)
        self.ATUAL_COMPT = get_compt(m_cont=-1) if compt is None else compt

        self.__DADOS_PADRAO = pd.read_excel(
            self.MAIN_FILE, sheet_name='DADOS_PADRÃO')
        self.DADOS_compt_atual = pd.read_excel(
            self.MAIN_FILE, sheet_name=self.ATUAL_COMPT, dtype=str)
        self.__DADOS_PADRAO, self.DADOS_compt_atual = self.consuldream()
        df1, df2 = self.consuldream()

        self.pd_insert_df_to_mysql(df1, 'main')
        self.pd_insert_df_to_mysql(df2, self.ATUAL_COMPT)
        # df1.columns = [col.lower().replace(" ", "_") for col in df1.columns]
        # df2.columns = [col.lower().replace(" ", "_") for col in df1.columns]

        # cursor.execute("CREATE TABLE my_table (name VARCHAR(255), age INT, gender CHAR(1))")

    def consuldream(self):
        # não preciso ficar ordenando no excel que nem maluco

        df = self.DADOS_compt_atual
        dpadrao = self.__DADOS_PADRAO

        df = df.sort_values(by=["Imposto a calcular", 'Razão Social'])
        df = df.set_index('Razão Social')
        dpadrao = dpadrao.set_index('Razão Social')
        dpadrao = dpadrao.reindex(df.index)

        dpadrao = dpadrao.reset_index()
        df = df.reset_index()
        # pd.set_option('display.max_rows', None)
        return dpadrao, df


COMPT = get_compt(int(sys.argv[1])) if len(sys.argv) > 1 else get_compt(-1)
GIAS_GISS_COMPT = get_compt(int(sys.argv[2])) if len(
    sys.argv) > 2 else get_compt(-2)

CONS = Consulta(COMPT)

# consultar_geral = CONS.consultar_geral
# consultar_compt = CONS.consultar_compt
# getfieldnames = CONS.get_fieldnames

# main_folder = CONS.MAIN_FOLDER
# main_file = CONS.MAIN_FILE
# TOTAL_CLIENTES = len(list(consultar_compt()))
# IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']
# TODO: GUI para impostos possiveis
# IMPOSTOS_POSSIVEIS.clear()
# addentry vai virar um objeto p/ funcionar corretamente c/ outras entry_row
