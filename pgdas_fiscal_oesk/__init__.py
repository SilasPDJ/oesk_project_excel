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
                once = razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = [
                    list(d.values())[cont] for d in DADOS_PADRAO]

                if str(razao_social) == 'nan':
                    break
                yield once
                cont += 1
            except IndexError:
                break

    def get_fieldnames(self):
        tutti = list(self.DADOS_compt_atual.to_dict().keys())
        tutti += [f for f in list(self.__DADOS_PADRAO.to_dict().keys())
                  if f not in tutti]
        return tutti

    def consultar_compt(self):

        df = self.__lsdv(self.DADOS_compt_atual.to_dict())

        cont = 0
        while True:
            try:
                once = razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = [
                    list(d.values())[cont] for d in df]
                yield once
                if str(razao_social) == 'nan':
                    break
            except IndexError:
                break
            cont += 1

    def __lsdv(self, dta):
        # list of dict values = lsdv meaning
        return list(dta.values())

    def __read_pandas(self, shname):
        import pandas as pd
        filename = self.MAIN_FILE

        main_pandas = pd.read_excel(
            filename, sheet_name=shname or shname.lower())
        return main_pandas
