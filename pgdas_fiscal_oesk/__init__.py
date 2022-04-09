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
            self.MAIN_FILE, sheet_name='DADOS_PADRÃO', dtype=str)
        self.DADOS_compt_atual = pd.read_excel(
            self.MAIN_FILE, sheet_name=self.ATUAL_COMPT)

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
                yield once
                if str(once[0]) == 'nan':
                    break
            except IndexError:
                break
            cont += 1

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
