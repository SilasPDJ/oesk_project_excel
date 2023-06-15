# from default.interact import press_key_b4
# from pgdas_fiscal_oesk.ginfess_excel_values import ExcelValuesPreensh
# from pgdas_fiscal_oesk.rotina_dividas_v3 import dividas_ativas_complete as rotina_dividas
# from pgdas_fiscal_oesk.send_dividas import SendDividas
# from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
import functools
import os
from typing import List
from default.interact.autocomplete_entry import AutocompleteEntry
from pgdas_fiscal_oesk.contimatic import Contimatic
from pgdas_fiscal_oesk.gias import GIA
from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
from pgdas_fiscal_oesk.silas_abre_g5_loop_v10 import G5
# # from pgdas_fiscal_oesk.silas_abre_g5_loop_v9_iss import G5
# from pgdas_fiscal_oesk.gias import GIA

from backend.database import MySqlInitConnection
from backend.models import SqlAchemyOrms
from default.sets import InitialSetting
import pandas as pd
import sys
from backend.database.db_create import TablesCreationInDBFromPandas
from backend.database.db_interface import DBInterface, InitNewCompt
from default.sets import calc_date_compt_offset, get_compt, compt_to_date_obj
# from default.sets import get_all_valores

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
# from pgdas_fiscal_oesk.rotina_pgdas_v3 import PgdasDeclaracao as PgdasDeclaracaoFull
# from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui
# from selenium.common.exceptions import UnexpectedAlertPresentException
# from pgdas_fiscal_oesk.silas_jr import JR
from default.webdriver_utilities.pre_drivers import pgdas_driver, pgdas_driver_ua, default_qrcode_driver


GIAS_GISS_COMPT = get_compt(int(sys.argv[2])) if len(
    sys.argv) > 2 else get_compt(-2)
IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']
VENC_DAS = '20-06-2023'
# TODO: GUI para impostos possiveis

# TODO: transformar self.compt das rotinas para objeto date com strformatado


class Rotinas:
    def _create_all_datas_using_sheets(self, compt_inicial='07-2021'):
        tables_creation_obj = TablesCreationInDBFromPandas(
            get_compt(-1), compt_inicial)
        tables_creation_obj.init_db_with_excel_data()

    def consultar_para_main_application():
        pass


# Rotinas()._create_all_datas_using_sheets()


class ComptGuiManager(DBInterface):
    # ---- class attributes
    # Consulta junta... DBInterface
    # Session = conn_obj.Session
    def __setup__(self):
        conn_obj = MySqlInitConnection()
        db_interface = DBInterface(conn_obj)
        self.EMPRESAS_ORM_OPERATIONS = db_interface.EmpresasOrmOperations(
            db_interface.conn_obj)
        self.COMPT_ORM_OPERATIONS = db_interface.ComptOrmOperations(
            db_interface.conn_obj)
        __full_query_compts = self.COMPT_ORM_OPERATIONS.filter_all_by_compt(
            compt_to_date_obj(self.compt))
        self.DADOS_COMPT = self.COMPT_ORM_OPERATIONS.generate_df_query_results_all(
            __full_query_compts)
        # self.engine = conn_obj.engine
        # self.session = conn_obj.Session

    def setup_required(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.__setup__()
            print(func, 'Is being called')
            return func(self, *args, **kwargs)
        return wrapper

    def __init__(self, compt: str):
        # ---- instance attributes...
        self.compt = compt
        InitNewCompt(compt)

        self.__setup__()

        self.EMPRESAS_DADOS = self.EMPRESAS_ORM_OPERATIONS.generate_df_v2(None, None)
        self.EMPRESAS_DADOS = self.EMPRESAS_DADOS[self.EMPRESAS_DADOS['status_ativo']]
         # somente ativos NA GUI
        # EMPRESA_DADOS is an actual constant

        self._specifics = None

    def create_month_if_not_exists(self):
        self.compt

    def call_simples_nacional(self, specifics_list: List[AutocompleteEntry] = None):
        # separar simples nacional de certificado???

        merged_df = self.main_generate_dados(allow_only_authorized=True)
        merged_df = self._get_specifics(specifics_list, merged_df)
        # merged_df = _merged_df.sort_values(
        #     'ha_procuracao_ecac', key=lambda x: x.map({'não': 0, 'sim': 1}))

        merged_df_cod_acesso = merged_df.loc[merged_df['ha_procuracao_ecac'] == 'não', :]
        merged_df_proc_ecac = merged_df.loc[merged_df['ha_procuracao_ecac'] == 'sim', :]
        # TODO: agora só falta conseguir alterar cliente direto no código
        # talvez seja legal debugar
        _iniciando_driver_ = default_qrcode_driver('C:\\Temp')

        for merged_df in [merged_df_cod_acesso, merged_df_proc_ecac]:

            attributes_required = ['razao_social', 'cnpj', 'cpf',
                                   'codigo_simples', 'valor_total', 'ha_procuracao_ecac']
            anexo_valores_keys = ['sem_retencao', 'com_retencao',  'anexo']

            required_df = merged_df.loc[:,
                                        attributes_required+anexo_valores_keys]

            SEP_INDX = len(attributes_required)
            # for client_row in self._yield_rows(required_df):
            allowed_column_names = ['declarado']

            # fazer_tudo_em_uma única sessão

            for row in merged_df.to_dict(orient='records'):
                client_row = [row[var]
                              for var in required_df.columns.to_list()]
                print(client_row)

                # this will be updated to add many anexos
                valores = {key: row[key] for key in anexo_valores_keys}
                # valores.update({key: float(row[key])
                #                for key in anexo_valores_keys[:-1]})
                all_valores = [
                    valores
                ]
                # ---
                prossegue = False if row['declarado'] else True

                if prossegue or self._specifics:
                    if row['ha_procuracao_ecac'] == 'sim':
                        PgdasDeclaracao(*client_row[:SEP_INDX],
                                        compt=self.compt, all_valores=all_valores, driver=_iniciando_driver_)
                    else:
                        PgdasDeclaracao(*client_row[:SEP_INDX],
                                        compt=self.compt, all_valores=all_valores)

                    row['declarado'] = True

                    self.COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt__dict(
                        row['cnpj'], row, allowed=allowed_column_names)

    def call_ginfess(self, specifics_list: List[AutocompleteEntry] = None):
        merged_df = self.main_generate_dados()
        merged_df = self._get_specifics(specifics_list, merged_df)

        attributes_required = ['razao_social',
                               'cnpj', 'ginfess_cod', 'ginfess_link']
        required_df = merged_df.loc[:, attributes_required]

        for row in merged_df.to_dict(orient='records'):
            allowed_column_names = ['sem_retencao',
                                    'com_retencao', 'valor_total']
            row_required = [row[var] for var in required_df.columns.to_list()]
            # all_valores = [float(v) for v in client_row[SEP_INDX:]]
            if row['ginfess_link'] != '':
                try:
                    dgg = DownloadGinfessGui(*row_required[:],
                                             compt=self.compt, show_driver=True)
                except Exception as e:
                    pass
                    print(f'\033[1;31mErro com {row["razao_social"]}\033[m')
                else:
                    if dgg.ginfess_valores is not None:
                        for e, k in enumerate(allowed_column_names):
                            row[k] = dgg.ginfess_valores[e]

                        allowed_column_names.append('pode_declarar')
                        allowed_column_names.append('nf_saidas')
                        row['nf_saidas'] = ''
                        row['pode_declarar'] = True

                        self.COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt__dict(
                            row['cnpj'], row, allowed=allowed_column_names)
                    else:
                        row['pode_declarar'] = True
                        self.COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt__dict(
                            row['cnpj'], row, allowed=['pode_declarar'])

                print(row)
                # row['declarado'] = True

    def call_giss(self, specifics_list: List[AutocompleteEntry] = None):
        merged_df = self.main_generate_dados()
        merged_df = self._get_specifics(specifics_list, merged_df)
        merged_df = merged_df = merged_df.loc[merged_df['giss_login'].str.lower().isin(
            ['', 'ginfess cód', 'não há']) == False]

        attributes_required = ['razao_social',
                               'cnpj', 'giss_login']

        required_df = merged_df.loc[:, attributes_required]

        allowed_column_names = []

        for row in merged_df.to_dict(orient='records'):
            row_required = [row[var] for var in required_df.columns.to_list()]
            # all_valores = [float(v) for v in client_row[SEP_INDX:]]
            try:
                GissGui(row_required,
                        compt=self.compt, first_compt=get_compt(-2))
            except Exception:
                print('\033[1;31m] GISS ONLINE - Não foi possível:\033[m')
                print(row)
                print('-----------')

            # COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt__dict(
            #     row['cnpj'], row, allowed=allowed_column_names)
            print(row)
            # row['declarado'] = True

    def call_g5(self, specifics_list: List[AutocompleteEntry] = None):
        main_df = self.main_generate_dados()
        elses = main_df.loc[main_df['imposto_a_calcular'] == 'ICMS']
        print('\033[1;31m', elses, '\033[;m')
        # main_df = main_df.loc[main_df['imposto_a_calcular'] != 'ICMS']

        main_df = self._get_specifics(specifics_list, main_df)

        attributes_required = ['razao_social', 'cnpj', 'cpf',
                               'codigo_simples', 'valor_total', 'imposto_a_calcular', 'nf_saidas', 'nf_entradas']
        # anexo_valores = ['sem_retencao', 'com_retencao',  'anexo']
        # SEP_INDX = len(attributes_required)
        # -------------------
        merged_df = main_df
        required_df = merged_df.loc[:, attributes_required]
        # order setup
        # for client_row in self._yield_rows(required_df):
        allowed_column_names = ['nf_saidas', 'nf_entradas']

        for row in merged_df.to_dict(orient='records'):
            client_row = [row[var] for var in required_df.columns.to_list()]
            row['nf_saidas'] = row['nf_saidas'].upper()
            if row['nf_entradas'] == 'NÃO HÁ' == row['nf_saidas']:
                continue

            if specifics_list[0].get() != '':
                G5(*client_row,
                   compt=self.compt)
            checker_continues = 'OK' not in row['nf_saidas'].upper().strip()
            # TODO: row['nf_entradas']?
            if checker_continues:
                G5(*client_row,
                   compt=self.compt)
                row['nf_saidas'] = "OK"
                # r

                self.COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt__dict(
                    row['cnpj'], row, allowed=allowed_column_names)

    def call_send_pgdas_email(self, specifics_list: List[AutocompleteEntry] = None):
        # simples_nacional procuradeclaracao_version
        # só vai chamar compts já criadas...
        # Como todas foram criadas 09-03-2023, tomar cuidado......

        merged_df = self.main_generate_dados(allow_only_authorized=True)
        merged_df = self._get_specifics(specifics_list, merged_df)

        _emailsenviados_df = merged_df.loc[merged_df['envio'] == True, :]
        _emailsenviados_df.to_excel(os.path.join(InitialSetting.getset_folderspath(
        ), "_EMAILS_ENVIADOS", f"{self.compt}_envio.xlsx"))

        # Envia e-mails baseado na condição do envio ser False
        allowed_df = merged_df.loc[(
            merged_df['envio'] == False) & merged_df['declarado'] == True, :]

        attributes_required = ['razao_social', 'cnpj', 'cpf',
                               'declarado', 'valor_total', 'imposto_a_calcular', 'envio']
        # anexo_valores_keys = ['sem_retencao', 'com_retencao',  'anexo']

        required_df = allowed_df.loc[:, attributes_required]

        # for client_row in self._yield_rows(required_df):
        allowed_column_names = ['envio']

        for row in allowed_df.to_dict(orient='records'):
            client_row = [row[var] for var in required_df.columns.to_list()]
            print(client_row)
            if row['envio'] != True:
                row['envio'] = True
                PgDasmailSender(
                    *client_row, email=row['email'], compt=self.compt, venc_das=VENC_DAS)
                self.COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt__dict(
                    row['cnpj'], row, allowed=allowed_column_names)

    def call_gias(self, specifics_list: List[AutocompleteEntry] = None):
        merged_df = self.main_generate_dados(allow_lucro_presumido=True)
        merged_df = self._get_specifics(specifics_list, merged_df)

        # Envia e-mails baseado na condição do envio ser False
        allowed_column_names = ['declarado']
        allowed_df = merged_df.loc[merged_df['ha_procuracao_ecac'].str.contains(
            ".", regex=False)]
        # No caso das gias é irrelevante
        # allowed_df = allowed_df.loc[allowed_df['declarado'] != True]
        attributes_required = ['razao_social',
                               'ha_procuracao_ecac', "ginfess_cod"]

        required_df = allowed_df.loc[:, attributes_required]
        allowed_df[['login', 'senha']] = required_df[['login', 'senha']] = required_df['ginfess_cod'].str.split(
            "//", expand=True)
        required_df = required_df.drop('ginfess_cod', axis=1)
        # ie
        for row in allowed_df.to_dict(orient='records'):
            if row['declarado']:
                print('PASSANDO GIA: ', row['razao_social'])
                continue

            client_row = [row[var] for var in required_df.columns.to_list()]
            client_row[1] = client_row[1].replace(".", "")
            row['declarado'] = True
            GIA(*client_row, compt=self.compt, first_compt=self.compt)
            self.COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt__dict(
                row['cnpj'], row, allowed=allowed_column_names)

    @setup_required
    def main_generate_dados(self, df_as_it_is: bool = False, allow_only_authorized=False, allow_lucro_presumido=False) -> pd.DataFrame:
        df_compt = self.DADOS_COMPT
        df_padrao = self.EMPRESAS_DADOS

        main_df = pd.merge(df_padrao, df_compt,
                           left_on='id', right_on='main_empresa_id')
        # ----- TODO: esta parte abaixo em função
        _str_col = 'imposto_a_calcular'
        if allow_only_authorized:
            main_df = main_df.loc[main_df['pode_declarar'] == True, :]
        icms_dfs = main_df.loc[main_df[_str_col] == 'ICMS', :]
        iss_dfs = main_df.loc[main_df[_str_col] == 'ISS', :]
        sem_mov_dfs = main_df.loc[main_df[_str_col] == 'SEM_MOV', :]

        lp_dfs = main_df.loc[main_df[_str_col] == 'LP', :]

        others = main_df[~main_df[_str_col].isin(icms_dfs[_str_col])
                         & ~main_df[_str_col].isin(iss_dfs[_str_col])
                         & ~main_df[_str_col].isin(sem_mov_dfs[_str_col])
                         & ~main_df[_str_col].isin(lp_dfs[_str_col])]

        list_with_all_dfs = [others, iss_dfs, icms_dfs, sem_mov_dfs, lp_dfs]
        if allow_lucro_presumido:
            list_with_all_dfs.append(sem_mov_dfs)
        if not df_as_it_is:
            merged_df = pd.concat(list_with_all_dfs)
            return merged_df
        else:
            return main_df

    def _get_specifics(self, specifics_list: List[AutocompleteEntry], merged_df: pd.DataFrame) -> pd.DataFrame:
        self._specifics = None
        print(specifics_list[0].get())
        if specifics_list[0].get() != "":
            # because gui.py will always have one field in ENTRIS_CLI...
            self._specifics = [cli.get() for cli in specifics_list]
            return merged_df[merged_df['razao_social'].isin(self._specifics)]
        return merged_df

    # def _yield_rows_getattr(self, df: pd.DataFrame):
    #     variables = df.columns.to_list()
    #     for row in df.itertuples(False):
    #         yield [getattr(row, var) for var in variables]

    @setup_required
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
