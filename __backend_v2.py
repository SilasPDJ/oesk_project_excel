# from default.interact import press_key_b4
# from pgdas_fiscal_oesk.ginfess_excel_values import ExcelValuesPreensh
# from pgdas_fiscal_oesk.rotina_dividas_v3 import dividas_ativas_complete as rotina_dividas
# from pgdas_fiscal_oesk.send_dividas import SendDividas
# from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
# from pgdas_fiscal_oesk.silas_abre_g5_loop_v10 import G5
# # from pgdas_fiscal_oesk.silas_abre_g5_loop_v9_iss import G5
# from pgdas_fiscal_oesk.gias import GIA

from backend.database import MySqlInitConnection
from backend.models import SqlAchemyOrms
from default.sets import InitialSetting
import pandas as pd
import sys
from backend.database.db_create import TablesCreationInDBFromPandas
from backend.database.db_interface import DBInterface
from default.sets import calc_date_compt_offset, get_compt, compt_to_date_obj
from default.sets import get_all_valores

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
# from pgdas_fiscal_oesk.rotina_pgdas_v3 import PgdasDeclaracao as PgdasDeclaracaoFull
# from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
# from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui
# from selenium.common.exceptions import UnexpectedAlertPresentException
# from pgdas_fiscal_oesk.silas_jr import JR


GIAS_GISS_COMPT = get_compt(int(sys.argv[2])) if len(
    sys.argv) > 2 else get_compt(-2)
IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']
# TODO: GUI para impostos possiveis


class Rotinas:
    def _create_all_datas_using_sheets(self, compt_inicial='07-2021'):
        tables_creation_obj = TablesCreationInDBFromPandas(
            get_compt(-1), compt_inicial)
        tables_creation_obj.init_db_with_excel_data()

    def consultar_para_main_application():
        pass


# Rotinas()._create_all_datas_using_sheets()


class ComptManager(DBInterface):
    # ----  class attributes
    # Consulta junta... DBInterface
    conn_obj = MySqlInitConnection()
    # Session = conn_obj.Session

    db_interface = DBInterface(conn_obj)
    EMPRESAS_ORM_OPERATIONS = db_interface.EmpresasOrmOperations(
        db_interface.conn_obj)
    COMPT_ORM_OPERATIONS = db_interface.ComptOrmOperations(
        db_interface.conn_obj)

    EMPRESAS_DADOS = EMPRESAS_ORM_OPERATIONS.generate_df_v2(None, None)

    def __init__(self, compt: str):
        # ---- instance attributes...
        self.compt = compt
        self.compt_as_date = compt_to_date_obj(compt)

        super().__init__(self.conn_obj)
        self.engine = self.conn_obj.engine
        self.session = self.conn_obj.Session

        self.DADOS_COMPT = self.COMPT_ORM_OPERATIONS.filter_all_by_compt(
            self.compt_as_date)
        self.DADOS_COMPT = self.COMPT_ORM_OPERATIONS.generate_df_query_results_all(
            self.DADOS_COMPT)

    def call_simples_nacional(self):
        merged_df = self.main_generate_dados()
        attributes_required = ['razao_social', 'cnpj', 'cpf',
                               'codigo_simples', 'valor_total', 'ha_procuracao_ecac']
        tres_valores = ['com_retencao', 'sem_retencao', 'valor_total']

        required_df = merged_df.loc[:, attributes_required+tres_valores]

        SEP_INDX = len(attributes_required)
        for client_row in self._yield_rows(required_df):
            print(client_row)

            all_valores = [float(v) for v in client_row[SEP_INDX:]]

            PgdasDeclaracao(*client_row[:SEP_INDX],
                            compt=self.compt, all_valores=all_valores)

            # TODO: set row.at[..., declaracao] = True
            # Como vou atualizar um DF? atualizar pelo ID...
            # ... Ler gui.py TODO: #

            # self.conn_obj.update_df_to_db()
            # do that for me please
            pass

    def main_generate_dados(self) -> None:
        df_compt = self.DADOS_COMPT
        df_padrao = self.EMPRESAS_DADOS

        merged_df = pd.merge(df_padrao, df_compt,
                             left_on='id', right_on='main_empresa_id')
        return merged_df

    def _yield_rows(self, df: pd.DataFrame):
        variables = df.columns.to_list()
        for row in df.itertuples(False):
            yield [getattr(row, var) for var in variables]

    def generate_compts_to_gui(self):
        InitialSetting.ate_atual_compt()
        pass

        # TODO: Get Data to pass to selenium apps methods
        # backend.py, setting new gui.py

        # clients_list = EMPRESAS.iloc[:, 0].to_list()

        # EMPRESAS_ORM_OPERATIONS.
