# import pandas as pd
from default.sets import Initial, InitialSetting, compt_to_date_obj
from backend.models import SqlAchemyOrms
from backend.database import MySqlInitConnection
import pandas as pd


class TablesCreationInDBFromPandas(MySqlInitConnection):
    """Executes the creation of a Database from Excel File

    Args:
        Consulta_DB (_type_): Brings methods for getting data
    """
    MAIN_FILE = InitialSetting.getset_folderspath(False)
    # MAIN_FILE = open(
    #     r"O:\HACKING\MY_PROJECTS\oesk_project_excel\default\sets\with_titlePATH.txt").read()

    def __init__(self, main_compt, compt_initial) -> None:
        from default.sets import InitialSetting
        """

        Args:
            main_compt (str): based COMPT
            compt_initial (str): first COMPT created automatically from the loop
        """
        self.compts = InitialSetting.ate_atual_compt(main_compt, compt_initial)
        self.str_compt = None

    def init_db_with_excel_data(self):
        """Make the tables creation routine from 2023-03
        """
        for compt in self.compts:
            self._generate_db_based_on_excel()
            self.str_compt = compt
            self._insert_dfs_into_db_init()

    def _insert_dfs_into_db_init(self):

        super().__init__()
        session = self.Session()
        compt_as_date = compt_to_date_obj(self.str_compt)
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

            esta_declarado = row['Declarado'].upper(
            ) == 'OK' or row['Declarado'].upper() == 'S'
            row['Declarado'] = True if esta_declarado else False

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
                .filter_by(compt=compt_to_date_obj(self.str_compt))\
                .filter(SqlAchemyOrms.ClientsCompts.main_empresa_id == main_empresa_id)\
                .first()
            if not existing_row:
                session.add(padrao)
        # Commit the changes to the database
        session.commit()

    def consuldream(self):
        # não preciso ficar ordenando no excel que nem maluco

        df_padrao, df_compt = self._consuldream__read_pandas()

        df_compt = df_compt.sort_values(
            by=["Imposto a calcular", 'Razão Social'])
        df_compt = df_compt.set_index('Razão Social')
        df_padrao = df_padrao.set_index('Razão Social')
        df_padrao = df_padrao.reindex(df_compt.index)

        _df_compt_with_cnpj = pd.merge(df_compt, df_padrao[['CNPJ']],
                                       left_index=True, right_index=True)

        merged_df = pd.merge(_df_compt_with_cnpj, df_padrao, on='CNPJ')

        df_padrao = df_padrao.reset_index()
        df_compt = _df_compt_with_cnpj.reset_index()
        df_compt = df_compt.drop('Razão Social', axis=1)
        # df_compt = df_compt.drop('CNPJ', axis=1)

        # dpadrao

        # pd.set_option('display.max_rows', None)
        return df_padrao, df_compt

    def _consuldream__read_pandas(self):
        DADOS_PADRAO = pd.read_excel(
            self.MAIN_FILE, sheet_name='DADOS_PADRÃO')
        DADOS_COMPT_ATUAL = pd.read_excel(
            self.MAIN_FILE, sheet_name=self.str_compt, dtype=str)

        return DADOS_PADRAO, DADOS_COMPT_ATUAL
        # df_padrao, df_compt_atual = self.consuldream()
        # self.pd_insert_df_to_mysql(df_padrao, 'main')
        # self.pd_insert_df_to_mysql(df_compt_atual, self.ATUAL_COMPT)
        # old methods are commented

    def _generate_db_based_on_excel(self) -> None:
        alc = SqlAchemyOrms()
        alc.Base.metadata.create_all(alc.engine)

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
