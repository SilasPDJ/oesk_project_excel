from backend.database import MySqlInitConnection
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
