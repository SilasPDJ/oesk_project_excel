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

    def __lsdv(self, dta):
        # list of dict values = lsdv meaning
        return list(dta.values())

    def consultar_geral(self):
        DADOS_PADRAO = self.__lsdv(self.__DADOS_PADRAO.to_dict())
        cont = 0
        while True:
            try:
                razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = [
                    list(d.values())[cont] for d in DADOS_PADRAO]

                if str(razao_social) == 'nan':
                    break
                yield razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac
                cont += 1
            except IndexError:
                break

    def get_fieldnames(self):
        CAMPOS_COMPT_ATUAL = list(self.DADOS_compt_atual.to_dict().keys())
        returned = list(self.__DADOS_PADRAO.to_dict().keys()) + \
            CAMPOS_COMPT_ATUAL
        return sorted(set(returned))  # list

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
