from default.sets import Initial
from default.sets import get_compt
import pandas as pd


class Consultar(Initial):
    def __init__(self, compt=None) -> None:
        super().__init__()

        self.MAIN_FOLDER = self.getset_folderspath()
        self.MAIN_FILE = self.getset_folderspath(False)
        self.ATUAL_COMPT = get_compt(m_cont=-1) if compt is None else compt

        self.DADOS_PADRAO = pd.read_excel(
            self.MAIN_FILE, sheet_name='DADOS_PADRÃO').to_dict()
# .to_html
        self.DADOS = self.__lsdv(self.DADOS_PADRAO)

    def __lsdv(self, dta):
        # list of dict values = lsdv meaning
        return list(dta.values())

    def consultar_geral(self):
        cont = 0
        while True:
            razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas = [
                list(d.values())[cont] for d in self.DADOS]

            if str(razao_social) == 'nan':
                break
            yield razao_social, self.treat_documents_values(cnpj), cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas
            cont += 1

    def consultar_compt(self):

        compt_atual = pd.read_excel(
            self.MAIN_FILE, sheet_name=self.ATUAL_COMPT)
        df = self.__lsdv(compt_atual.to_dict())

        cont = 0
        while True:
            once = razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = [
                list(d.values())[cont] for d in df]
            yield once
            if str(razao_social) == 'nan':
                break

            cont += 1

    @staticmethod
    def treat_documents_values(arg):
        return str(int(arg))
