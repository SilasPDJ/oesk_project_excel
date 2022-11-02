import _import
import pyautogui as pygui
from default.interact import *
from pgdas_fiscal_oesk import Consultar
from default.sets import InitialSetting, get_compt
import clipboard

p = pygui
COMPT = get_compt(-1)
CONS = Consultar(COMPT)
consultar_geral = CONS.consultar_geral
consultar_compt = CONS.consultar_compt
getfieldnames = CONS.get_fieldnames

main_folder = CONS.MAIN_FOLDER
main_file = CONS.MAIN_FILE

TOTAL_CLIENTES = len(list(consultar_compt()))
IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']


class Main:

    def any_to_str(self, *args):
        for v in args:
            yield "".join(str(v))

    def consultar_mixed(self): return zip(consultar_geral(), consultar_compt())

    def get_dataclipboard(self, campo: str):
        # input(campo)
        if campo == '':
            campo = "CNPJ"
        indcampo = CONS.get_fieldnames().index(campo)
        selected_list_values = list(
            self.any_to_str(*CONS.clients_list(indcampo)))
        # whoindex = self.__get_clienid(self.selected_client.get())
        whoindex = 0
        returned = str(selected_list_values[whoindex])
        clipboard.copy(returned)
        return returned

    def get_clients_with_dividas(self):
        """
        #  Organiza o G5 para fazer primeiro ISS, depois ICMS
        """
        # LIST_ISS = []
        # LIST_ICMS = []
        LIST_DIVIDAS = []

        def get_order():

            for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
                razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios, imposto_a_calcular = list(
                    self.any_to_str(*compt_vals))
                _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
                    self.any_to_str(*geral))
                envio = envio.upper()
                email = email.strip()
                dividas_ativas = dividas_ativas.strip().lower()
                proc_ecac = proc_ecac.lower()
                TUPLA_DATA = (razao_social, cnpj, cpf,
                              codigo_simples, valor_tot, imposto_a_calcular, proc_ecac)

                def append_me(obj_list):
                    if imposto_a_calcular.strip() in IMPOSTOS_POSSIVEIS:
                        obj_list.append(TUPLA_DATA)

                if dividas_ativas != "não há":
                    append_me(LIST_DIVIDAS)
                    # print(razao_social, _razao_social)
                # return [TUPLA_DATA]  # important for loop
            # full = LIST_ISS + LIST_ICMS
            full = LIST_DIVIDAS
            # return LIST_ECAC, LIST_NORMAL
            return full
        for v in get_order():
            pass


M1 = Main()
print(*M1.get_clients_with_dividas())

GFN = getfieldnames
gdc = M1.get_dataclipboard(GFN()[0])

print(gdc)
