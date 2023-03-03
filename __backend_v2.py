
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

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
from pgdas_fiscal_oesk.rotina_pgdas_v3 import PgdasDeclaracao as PgdasDeclaracaoFull
from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui
from selenium.common.exceptions import UnexpectedAlertPresentException
from pgdas_fiscal_oesk.silas_jr import JR

import sys
import pandas as pd
import streamlit as st
import mysql.connector
import sqlite3

def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])


def init_connection_alchemy():
    from sqlalchemy import create_engine
    import mysql.connector
    LSCT = list(st.secrets["mysql"].values())  # ListSeCreTs
    # sqlachemy connection
    str_connection = f'mysql://{LSCT[-2]}:{LSCT[-1]}@{LSCT[0]}/{LSCT[-3]}'
    return create_engine(str_connection)


def init_connection():
    conn = sqlite3.connect('.streamlit/database.db')
    return conn
    #  mysql -uroot -p


class Consulta(Initial):
    engine = init_connection()

    def __init__(self, compt=None) -> None:
        super().__init__()
        self.conn = init_connection()
        self.cursor = self.conn.cursor()

        self.MAIN_FOLDER = self.getset_folderspath()
        self.MAIN_FILE = self.getset_folderspath(False)
        self.ATUAL_COMPT = get_compt(m_cont=-1) if compt is None else compt

        self.__DADOS_PADRAO = pd.read_excel(
            self.MAIN_FILE, sheet_name='DADOS_PADRÃO')
        self.DADOS_compt_atual = pd.read_excel(
            self.MAIN_FILE, sheet_name=self.ATUAL_COMPT, dtype=str)
        self.__DADOS_PADRAO, self.DADOS_compt_atual = self.consuldream()
        df1, df2 = self.consuldream()
        # df1.columns = [col.lower().replace(" ", "_") for col in df1.columns]
        # df2.columns = [col.lower().replace(" ", "_") for col in df1.columns]

        # cursor.execute("CREATE TABLE my_table (name VARCHAR(255), age INT, gender CHAR(1))")
        self.create_table_sql(df1, 'main')
        self.create_table_sql(df2, self.ATUAL_COMPT)

        # df1.to_sql(name="tb_name", con=self.conn,
        df1.to_sql(name="main", con=self.engine,
                   if_exists="append", index=False)
        df2.to_sql(name=self.ATUAL_COMPT, con=self.engine,
                   if_exists="append", index=False)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

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

    def create_table_sql(self, df, tbname):
        # Generate a SQL schema string based on the DataFrame columns
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        # df, tbname, con=self.conn).replace('"', '`')
        schema = pd.io.sql.get_schema(
            df, tbname, con=self.engine).replace('"', '`')
        self.cursor.execute(f"DROP TABLE IF EXISTS `{tbname}`;")
        self.cursor.execute(schema)
        self.conn.commit()


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
