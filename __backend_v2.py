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

from default.sets import InitialSetting
from backend.models import SqlAchemyOrms


class TablesCreationInDBFromPandas(Consulta_DB):
    def __init__(self, compt) -> None:
        self.COMPT = compt

    @staticmethod
    def get_money_as_decimal(money) -> float:
        str_money = str(money).upper().strip()
        if str_money == '' or str_money == '0' or str_money == "DAS_PEND":
            return 0.0
        else:
            try:
                return float(money)
            except ValueError:
                return money

    def main_insert_dfs_into_db_init(self, str_compt: str):
        super().__init__(str_compt)

        session = self.Session()
        compt_as_date = compt_to_date_obj(str_compt)
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
            main_empresa_id = session.query(SqlAchemyOrms.MainEmpresas).filter_by(
                cnpj=row['CNPJ']).first().id

            possui_das_pend = True if row['Valor Total'].upper(
            ).strip() == "DAS_PEND" else False
            # possui das pendentes?

            row['Sem retenção'] = self.get_money_as_decimal(
                row['Sem retenção'])
            row['Com Retenção'] = self.get_money_as_decimal(
                row['Com Retenção'])
            row['Valor Total'] = self.get_money_as_decimal(row['Valor Total'])

            padrao = SqlAchemyOrms.ClientsCompts(
                main_empresa_id=main_empresa_id,
                declarado=row['Declarado'],
                nf_saidas=row['NF Saídas'],
                nf_entradas=row['Entradas'],
                sem_retencao=row['Sem retenção'],
                com_retencao=row['Com Retenção'],
                valor_total=row['Valor Total'],
                anexo=row['Anexo'],
                envio=row['ENVIO'],
                imposto_a_calcular=row['Imposto a calcular'],
                possui_das_pendentes=possui_das_pend,
                compt=compt_as_date
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


alc = SqlAchemyOrms()
alc.Base.metadata.create_all(alc.engine)


COMPT = get_compt(int(sys.argv[1])) if len(sys.argv) > 1 else get_compt(-1)
GIAS_GISS_COMPT = get_compt(int(sys.argv[2])) if len(
    sys.argv) > 2 else get_compt(-2)
IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']
# TODO: GUI para impostos possiveis


tables_creation_obj = TablesCreationInDBFromPandas(COMPT)

for compt in InitialSetting.ate_atual_compt(tables_creation_obj.COMPT, '07-2021'):
    tables_creation_obj.main_insert_dfs_into_db_init(compt)

# session = alc.Session


# IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']
# TODO: GUI para impostos possiveis
# IMPOSTOS_POSSIVEIS.clear()
# addentry vai virar um objeto p/ funcionar corretamente c/ outras entry_row
