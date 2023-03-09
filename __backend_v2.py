# from default.interact import press_key_b4
# from pgdas_fiscal_oesk.ginfess_excel_values import ExcelValuesPreensh
# from pgdas_fiscal_oesk.rotina_dividas_v3 import dividas_ativas_complete as rotina_dividas
# from pgdas_fiscal_oesk.send_dividas import SendDividas
# from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
from typing import List
from default.interact.autocomplete_entry import AutocompleteEntry
from pgdas_fiscal_oesk.silas_abre_g5_loop_v10 import G5
# # from pgdas_fiscal_oesk.silas_abre_g5_loop_v9_iss import G5
# from pgdas_fiscal_oesk.gias import GIA

from app import COMPT_ORM_OPERATIONS
from backend.database import MySqlInitConnection
from backend.models import SqlAchemyOrms
from default.sets import InitialSetting
import pandas as pd
import sys
from backend.database.db_create import TablesCreationInDBFromPandas
from backend.database.db_interface import DBInterface
from default.sets import calc_date_compt_offset, get_compt, compt_to_date_obj
# from default.sets import get_all_valores

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
# from pgdas_fiscal_oesk.rotina_pgdas_v3 import PgdasDeclaracao as PgdasDeclaracaoFull
# from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui
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

        __full_query_compts = self.COMPT_ORM_OPERATIONS.filter_all_by_compt(
            self.compt_as_date)
        self.DADOS_COMPT = self.COMPT_ORM_OPERATIONS.generate_df_query_results_all(
            __full_query_compts)

    def call_simples_nacional(self, specifics_list: List[AutocompleteEntry] = None):
        # simples_nacional procuradeclaracao_version
        # só vai chamar compts já criadas...
        # Como todas foram criadas 09-03-2023, tomar cuidado......

        merged_df = self.main_generate_dados()
        specifics = None

        if specifics_list[0].get() != "":
            # vem do gui.py...
            specifics = [cli.get() for cli in specifics_list]
            merged_df = merged_df[merged_df['razao_social'].isin(specifics)]

        attributes_required = ['razao_social', 'cnpj', 'cpf',
                               'codigo_simples', 'valor_total', 'ha_procuracao_ecac']
        anexo_valores = ['sem_retencao', 'com_retencao',  'anexo']

        required_df = merged_df.loc[:, attributes_required+anexo_valores]

        SEP_INDX = len(attributes_required)
        # for client_row in self._yield_rows(required_df):
        allowed_column_names = ['declarado']

        for row in merged_df.to_dict(orient='records'):
            client_row = [row[var] for var in required_df.columns.to_list()]
            print(client_row)

            _valores_padrao = [
                float(v) for v in client_row[SEP_INDX:-1]]+anexo_valores[-1:]

            anexo_valores = [
                _valores_padrao,
            ]
            # pois o argumento é uma lista... Próxima implementação, criar tabela específica?
            # se sim, vai ter que ..mergir.. os dataframes corretamente...
            # por enquanto só tem umvalor na lista
            prossegue = False
            if specifics:
                prossegue = True
            elif not row['declarado']:
                prossegue = True
            if prossegue:
                PgdasDeclaracao(*client_row[:SEP_INDX],
                                compt=self.compt, all_valores=anexo_valores)
                row['declarado'] = True

                COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt__dict(
                    row['cnpj'], row, allowed=allowed_column_names)

    def call_ginfess(self):
        merged_df = self.main_generate_dados()
        attributes_required = ['razao_social',
                               'cnpj', 'ginfess_cod', 'ginfess_link']
        required_df = merged_df.loc[:, attributes_required]

        allowed_column_names = ['sem_retencao', 'com_retencao',  'valor_total']

        for row in merged_df.to_dict(orient='records'):
            row_required = [row[var] for var in required_df.columns.to_list()]
            # all_valores = [float(v) for v in client_row[SEP_INDX:]]
            if row['ginfess_link'] != '':
                try:
                    dgg = DownloadGinfessGui(*row_required[:],
                                             compt=self.compt)
                except Exception as e:
                    pass
                    print(f'\033[1;31mErro com {row["razao_social"]}\033[m')
                else:
                    if dgg.ginfess_valores is not None:
                        for e, k in enumerate(allowed_column_names):
                            row[k] = dgg.ginfess_valores[e]
                        COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt__dict(
                            row['cnpj'], row, allowed=allowed_column_names)
                print(row)
                # row['declarado'] = True

    def call_g5(self):
        main_df = self.main_generate_dados()
        attributes_required = ['razao_social', 'cnpj', 'cpf',
                               'codigo_simples', 'valor_total', 'imposto_a_calcular', 'nf_saidas', 'nf_entradas']
        # anexo_valores = ['sem_retencao', 'com_retencao',  'anexo']
        # SEP_INDX = len(attributes_required)
        # -------------------
        _str_col = 'imposto_a_calcular'
        icms_dfs = main_df.loc[main_df[_str_col] == 'ICMS', :]
        iss_dfs = main_df.loc[main_df[_str_col] == 'ISS', :]
        others = main_df[~main_df[_str_col].isin(
            icms_dfs[_str_col]) & ~main_df[_str_col].isin(iss_dfs[_str_col])]

        merged_df = pd.concat([icms_dfs, iss_dfs, others])

        required_df = merged_df.loc[:, attributes_required]
        # order setup
        # TODO: shall this be a function????

        # for client_row in self._yield_rows(required_df):
        allowed_column_names = ['nf_saidas', 'nf_entradas']

        for row in merged_df.to_dict(orient='records'):
            client_row = [row[var] for var in required_df.columns.to_list()]
            print(client_row)

            # pois o argumento é uma lista... Próxima implementação, criar tabela específica?
            # se sim, vai ter que ..mergir.. os dataframes corretamente...
            # por enquanto só tem umvalor na lista
            if row['nf_saidas'] != 'não há' and row['nf_entradas'] != 'não há':
                G5(*client_row,
                   compt=self.compt)
                row['declarado'] = True

                COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt__dict(
                    row['cnpj'], row, allowed=allowed_column_names)

    def main_generate_dados(self) -> pd.DataFrame:
        df_compt = self.DADOS_COMPT
        df_padrao = self.EMPRESAS_DADOS

        merged_df = pd.merge(df_padrao, df_compt,
                             left_on='id', right_on='main_empresa_id')
        return merged_df

    # def _yield_rows_getattr(self, df: pd.DataFrame):
    #     variables = df.columns.to_list()
    #     for row in df.itertuples(False):
    #         yield [getattr(row, var) for var in variables]

    def generate_compts_to_gui(self):
        InitialSetting.ate_atual_compt()
        pass

        # TODO: Get Data to pass to selenium apps methods
        # backend.py, setting new gui.py

        # clients_list = EMPRESAS.iloc[:, 0].to_list()

        # EMPRESAS_ORM_OPERATIONS.

    def transform_dict_to_object(self, dictonary: dict) -> object:
        class MyObject:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
        return MyObject(**dictonary)
