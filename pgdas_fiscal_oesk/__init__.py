from scripts.init_database import MySqlInitConnection
from default.sets import Initial
from default.sets import get_compt
import pandas as pd


class Consultar(Initial):
    def __init__(self, compt=None) -> None:
        super().__init__()

        self.MAIN_FOLDER = self.getset_folderspath()
        self.MAIN_FILE = self.getset_folderspath(False)
        self.ATUAL_COMPT = get_compt(m_cont=-1) if compt is None else compt

        self.__DADOS_PADRAO = pd.read_excel(
            self.MAIN_FILE, sheet_name='DADOS_PADRÃO')
        self.DADOS_compt_atual = pd.read_excel(
            self.MAIN_FILE, sheet_name=self.ATUAL_COMPT, dtype=str)
        self.__DADOS_PADRAO, self.DADOS_compt_atual = self.__consuldream()

    def __consuldream(self):
        # não preciso ficar ordenando no excel que nem maluco

        df = self.DADOS_compt_atual
        dpadrao = self.__DADOS_PADRAO

        df = df.sort_values(by=["Imposto a calcular"])
        df = df.set_index('Razão Social')
        dpadrao = dpadrao.set_index('Razão Social')
        dpadrao = dpadrao.reindex(df.index)

        dpadrao = dpadrao.reset_index()
        df = df.reset_index()
        # pd.set_option('display.max_rows', None)
        return dpadrao, df

    def consultar_geral(self):
        DADOS_PADRAO = self.__lsdv(self.__DADOS_PADRAO.to_dict())
        cont = 0
        while True:
            try:
                once = [
                    list(d.values())[cont] for d in DADOS_PADRAO]

                if str(once[0]) == 'nan':
                    break
                yield once
                cont += 1
            except IndexError:
                break

    def consultar_compt(self):
        df = self.__lsdv(self.DADOS_compt_atual.to_dict())
        cont = 0
        while True:
            try:
                once = [
                    list(d.values())[cont] for d in df]
                if str(once[0]) == 'nan':
                    break
                yield once
                cont += 1
            except IndexError:
                break

    def consultar_dividas(self):
        # forma de substituir o while true com for
        import os
        divdf = pd.read_excel(
            os.path.join(self.MAIN_FOLDER, 'parcelamentos.xlsx'), sheet_name=self.ATUAL_COMPT, dtype=str)
        divdf = self.__lsdv(divdf.to_dict())
        for cont in range(len(divdf)):
            yield [list(d.values())[cont] for d in divdf]

    def get_fieldnames(self):
        # tutti = list(self.DADOS_compt_atual.to_dict().keys())
        # tutti += [f for f in list(self.__DADOS_PADRAO.to_dict().keys())]
        df = pd.merge(self.DADOS_compt_atual, self.__DADOS_PADRAO)
        tutti = list(df.to_dict().keys())
        return tutti

    def clients_list(self, get_campo=0) -> list:
        def __lsdv(dta): return list(dta.values())
        df = pd.merge(self.DADOS_compt_atual, self.__DADOS_PADRAO)
        dados = list(__lsdv(df.to_dict())[get_campo].values())
        return dados

    def __lsdv(self, dta):
        # list of dict values = lsdv meaning
        return list(dta.values())


class Consulta_DB(Initial, MySqlInitConnection):
    # mysql_conn = init_connection()

    def __init__(self, compt=None) -> None:
        super().__init__()
        """
        Calls SqlInitConnection...
        """
        self.compt = compt
        self.MAIN_FOLDER = self.getset_folderspath()
        self.MAIN_FILE = self.getset_folderspath(False)
        self.MAIN_COMPT = get_compt(m_cont=-1) if compt is None else compt
        # TODO: get_compt as date() value type

        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='main'"
        # Create SQLAlchemy engine using the connection string

        # self.consuldream()

        # df = self.pd_read_sql(query)

        # s_settings_df = pd.DataFrame(self.engine.connect().execute(text(query)))
        # pd.read_sql(query, self.mysql_conn)
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
            self.MAIN_FILE, sheet_name=self.MAIN_COMPT, dtype=str)

        return DADOS_PADRAO, DADOS_COMPT_ATUAL
        # df_padrao, df_compt_atual = self.consuldream()
        # self.pd_insert_df_to_mysql(df_padrao, 'main')
        # self.pd_insert_df_to_mysql(df_compt_atual, self.ATUAL_COMPT)
        # old methods are commented
