# from default.interact import press_key_b4
# from pgdas_fiscal_oesk.ginfess_excel_values import ExcelValuesPreensh
# from pgdas_fiscal_oesk.rotina_dividas_v3 import dividas_ativas_complete as rotina_dividas
# from pgdas_fiscal_oesk.send_dividas import SendDividas
# from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
# from pgdas_fiscal_oesk.silas_abre_g5_loop_v10 import G5
# # from pgdas_fiscal_oesk.silas_abre_g5_loop_v9_iss import G5
# from pgdas_fiscal_oesk.gias import GIA

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

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column,ForeignKey
from sqlalchemy import  Integer, String, Numeric, Date
from scripts.init_database import MySqlInitConnection


class Consulta(Initial, MySqlInitConnection):
    # mysql_conn = init_connection()

    def __init__(self, compt=None) -> None:
        super().__init__()
        """
        Calls SqlInitConnection...
        """
        self.compt = compt
        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='main'"
        # Create SQLAlchemy engine using the connection string

        self.main_creation_of_db()
        self.consuldream()

        df = self.pd_read_sql(query)

        # s_settings_df = pd.DataFrame(self.engine.connect().execute(text(query)))
        # pd.read_sql(query, self.mysql_conn)

    def main_creation_of_db(self):
        compt = self.compt
        self.MAIN_FOLDER = self.getset_folderspath()
        self.MAIN_FILE = self.getset_folderspath(False)
        self.ATUAL_COMPT = get_compt(m_cont=-1) if compt is None else compt

        self.__DADOS_PADRAO = pd.read_excel(
            self.MAIN_FILE, sheet_name='DADOS_PADRÃO')
        self.DADOS_compt_atual = pd.read_excel(
            self.MAIN_FILE, sheet_name=self.ATUAL_COMPT, dtype=str)
        self.__DADOS_PADRAO, self.DADOS_compt_atual = self.consuldream()
        padrao, compt_atual = self.consuldream()

        # self.pd_insert_df_to_mysql(df_padrao, 'main')
        # self.pd_insert_df_to_mysql(df_compt_atual, self.ATUAL_COMPT)
        # to insert to mysql

    def consuldream(self):
        # não preciso ficar ordenando no excel que nem maluco

        df = self.DADOS_compt_atual
        dpadrao = self.__DADOS_PADRAO

        df = df.sort_values(by=["Imposto a calcular", 'Razão Social'])
        df = df.set_index('Razão Social')
        dpadrao = dpadrao.set_index('Razão Social')
        dpadrao = dpadrao.reindex(df.index)

        _df_compt_with_cnpj = pd.merge(df, dpadrao[['CNPJ']],
                                       left_index=True, right_index=True)

        merged_df = pd.merge(_df_compt_with_cnpj, dpadrao, on='CNPJ')

        dpadrao = dpadrao.reset_index()
        df = _df_compt_with_cnpj.reset_index()
        dpadrao = dpadrao.drop('Razão Social', axis=1)

        # dpadrao

        # pd.set_option('display.max_rows', None)
        return dpadrao, df


class SqlAchemyOrms(MySqlInitConnection):
    Base = declarative_base()

    class Main(Base):
        __tablename__ = 'main'

        id = Column(Integer, primary_key=True)
        razao_social = Column(String(255))
        cnpj = Column(String(18), unique=True)
        cpf = Column(String(14))
        codigo_simples = Column(String(12))
        email = Column(String(255))
        gissonline = Column(String(500))
        giss_login = Column(String(50))
        ginfess_cod = Column(String(100))
        ginfess_link = Column(String(500))
        ha_procuracao_ecac = Column(String(7))

        padraos = relationship("Padrao", back_populates="main")

    class Padrao(Base):
        __tablename__ = 'padrao'

        id = Column(Integer, primary_key=True)
        main_id = Column(Integer, ForeignKey('main.id'))
        main = relationship("Main", back_populates="padraos")
        # razao_social = Column(String(100))
        declarado = Column(String(5))
        nf_saidas = Column(String(10))
        entradas = Column(String(10))
        sem_retencao = Column(Numeric(precision=10, scale=2))
        com_retencao = Column(Numeric(precision=10, scale=2))
        valor_total = Column(Numeric(precision=10, scale=2))
        anexo = Column(String(3))
        envio = Column(String(3))
        imposto_a_calcular = Column(String(7))
        compt = Column(Date())

alc = SqlAchemyOrms()
alc.Base.metadata.create_all(alc.engine)
session = alc.Session




# COMPT = get_compt(int(sys.argv[1])) if len(sys.argv) > 1 else get_compt(-1)
# GIAS_GISS_COMPT = get_compt(int(sys.argv[2])) if len(
#     sys.argv) > 2 else get_compt(-2)

# CONS = Consulta(COMPT)

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
