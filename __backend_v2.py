# from default.interact import press_key_b4
# from pgdas_fiscal_oesk.ginfess_excel_values import ExcelValuesPreensh
# from pgdas_fiscal_oesk.rotina_dividas_v3 import dividas_ativas_complete as rotina_dividas
# from pgdas_fiscal_oesk.send_dividas import SendDividas
# from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
# from pgdas_fiscal_oesk.silas_abre_g5_loop_v10 import G5
# # from pgdas_fiscal_oesk.silas_abre_g5_loop_v9_iss import G5
# from pgdas_fiscal_oesk.gias import GIA

from default.sets import calc_date_compt_offset, get_compt, compt_to_date_obj
from default.sets import get_all_valores

# from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
# from pgdas_fiscal_oesk.rotina_pgdas_v3 import PgdasDeclaracao as PgdasDeclaracaoFull
# from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
# from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui
# from selenium.common.exceptions import UnexpectedAlertPresentException
# from pgdas_fiscal_oesk.silas_jr import JR
from pgdas_fiscal_oesk import Consulta_DB as Consulta_DB

import sys
import pandas as pd

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Numeric, Date
from scripts.init_database import MySqlInitConnection
from default.sets import InitialSetting


class SqlAchemyOrms(MySqlInitConnection):
    Base = declarative_base()

    class MainEmpresas(Base):
        __tablename__ = 'main_empresas'

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
        ha_procuracao_ecac = Column(String(15))

        clients_compts = relationship(
            "ClientsCompts", back_populates="main_empresas")

    class ClientsCompts(Base):
        __tablename__ = 'clients_compts'

        id = Column(Integer, primary_key=True)
        main_empresa_id = Column(Integer, ForeignKey('main_empresas.id'))
        main_empresas = relationship(
            "MainEmpresas", back_populates="clients_compts")
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


class TablesCreationInDBFromPandas(Consulta_DB):
    def __init__(self, compt) -> None:
        super().__init__(compt)

    def _insert_dfs_into_db_init(self, str_compt: str):

        session = self.Session()
        dados_padrao, df_compt = self.consuldream()
        df_compt = df_compt.fillna('')
        for col in ['Valor Total', 'Sem retenção', 'Com Retenção']:
            df_compt[col] = df_compt[col].replace('zerou', 0)

        dados_padrao = dados_padrao.fillna('')
        dados_padrao = dados_padrao.drop_duplicates(['CNPJ'])

        # df_compt = df_compt.replace(np.nan, '')
        # Loop over the rows in dados_padrao DataFrame and create MainEmpresas instances

        for idx, row in dados_padrao.iterrows():
            main = SqlAchemyOrms.MainEmpresas(
                razao_social=row['Razão Social'],
                cnpj=row['CNPJ'],
                cpf=row['CPF'],
                codigo_simples=row['Código Simples'],
                email=row['email'],
                gissonline=row['GissOnline'],
                giss_login=row['Giss Login'],
                ginfess_cod=row['Ginfess Cód'],
                ginfess_link=row['Ginfess Link'],
                ha_procuracao_ecac=row['Há procuração ECAC']
            )
            existing_row = session.query(
                SqlAchemyOrms.MainEmpresas).filter_by(cnpj=row['CNPJ']).first()
            if existing_row is None:
                session.add(main)
        session.commit()
        # ---
        for idx, row in df_compt.iterrows():
            row['CNPJ']
            main_empresa_id = session.query(SqlAchemyOrms.MainEmpresas).filter_by(
                cnpj=row['CNPJ']).first().id

            padrao = SqlAchemyOrms.ClientsCompts(
                main_empresa_id=main_empresa_id,
                declarado=row['Declarado'],
                nf_saidas=row['NF Saídas'],
                entradas=row['Entradas'],
                sem_retencao=row['Sem retenção'] or 0,
                com_retencao=row['Com Retenção'] or 0,
                valor_total=row['Valor Total'] or 0,
                anexo=row['Anexo'],
                envio=row['ENVIO'],
                imposto_a_calcular=row['Imposto a calcular'],
                compt=compt_to_date_obj(str_compt)
                # TODO: check todos
            )
            existing_row = session.query(SqlAchemyOrms.ClientsCompts)\
                .filter_by(compt=compt_to_date_obj(str_compt))\
                .filter(SqlAchemyOrms.ClientsCompts.main_empresa_id == main_empresa_id)\
                .first()
            if not existing_row:
                session.add(padrao)
        # Commit the changes to the database
        session.commit()

    def insert_all_dfs_in_mysql(self):
        # tables_creation_obj = self
        # for compt in InitialSetting.ate_atual_compt(tables_creation_obj.MAIN_COMPT, '07-2021'):
        #     tables_creation_obj.insert_dfs_into_db_init(compt)
        for compt in InitialSetting.ate_atual_compt(self.MAIN_COMPT, '07-2021'):
            self._insert_dfs_into_db_init(compt)


alc = SqlAchemyOrms()
alc.Base.metadata.create_all(alc.engine)


COMPT = get_compt(int(sys.argv[1])) if len(sys.argv) > 1 else get_compt(-1)
GIAS_GISS_COMPT = get_compt(int(sys.argv[2])) if len(
    sys.argv) > 2 else get_compt(-2)
IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']
# TODO: GUI para impostos possiveis

tables_creation_obj = TablesCreationInDBFromPandas(COMPT)
# tables_creation_obj.insert_all_dfs_in_mysql()


# session = alc.Session


# IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']
# TODO: GUI para impostos possiveis
# IMPOSTOS_POSSIVEIS.clear()
# addentry vai virar um objeto p/ funcionar corretamente c/ outras entry_row
