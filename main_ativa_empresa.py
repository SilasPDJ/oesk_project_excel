# import pgdas_fiscal_oesk
# from pgdas_fiscal_oesk import rotina_pgdas

from pgdas_fiscal_oesk.contimatic import Contimatic
from pgdas_fiscal_oesk.gias import GIA
from default.webdriver_utilities.pre_drivers import pgdas_driver, ginfess_driver
from default.sets import InitialSetting, get_compt
from pgdas_fiscal_oesk import Consultar

from time import sleep
import pyautogui as pygui
from default.interact import *


from pgdas_fiscal_oesk.relacao_nfs import iss_plan_exists, NfCanceled

from default.sets import get_all_valores

from pgdas_fiscal_oesk.rotina_pgdas_v2 import PgdasDeclaracao
from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui
from pgdas_fiscal_oesk.silas_abre_g5_loop_v8 import G5
# from win10toast import ToastNotifier
import os
os.system('d:/PROGRAMAS/oesk_project_excel-master/venv/Scripts/activate.bat')
COMPT = get_compt(-1)

CONS = Consultar(COMPT)
consultar_geral = CONS.consultar_geral
consultar_compt = CONS.consultar_compt

main_folder = CONS.MAIN_FOLDER
main_file = CONS.MAIN_FILE

TOTAL_CLIENTES = len(list(consultar_compt()))
IMPOSTOS_POSSIVEIS = ['ICMS, ISS']


def any_to_str(*args):
    for v in args:
        yield "".join(str(v))


class JROnly(Contimatic):

    def __init__(self, *args, compt):
        __r_social, self.__cnpj, __cpf, __cod_simples, __valor_competencia, imposto_a_calcular, nf_out = args
        __client = __r_social

        self.compt_used = compt
        self.client_path = self.files_pathit(__client)

        # Se tem 3valores[excel], tem XML. Se não tem, não tem
        # (pois o xml e excel vem do ginfess_download)....

        registronta = self.registronta()

    def make_it(self):
        all_xls_inside = self.files_get_anexos_v4(
            self.client_path, file_type='xlsx')
        relacao_notas = all_xls_inside[0] if len(
            all_xls_inside) == 1 else IndexError()
        self.activating_client(self.formatar_cnpj(self.__cnpj))
        # pygui.getActiveWindow().maximize()
        # # Agora vai ser por cnpj...
        # self.start_walk_menu()
        # foritab(2, 'right')
        # foritab(7, 'down')
        # pygui.hotkey('right')
        # foritab(7, 'down')
        # pygui.hotkey('enter')


# for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
#     razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = list(
#         any_to_str(*compt_vals))
#     __razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
#         any_to_str(*geral))
#     envio = envio.upper()
#     email = email.strip()
#     dividas_ativas = dividas_ativas.strip().lower()

#     jonly = JROnly(razao_social, cnpj, cpf, codigo_simples,
#                    valor_tot, imposto_a_calcular, nf_out, compt=COMPT)
#     if e == 0:
#         jonly.abre_ativa_programa('Jr')

#     jonly.make_it()
#     print('PRESSIONE F1 PARA ATIVAR O PROXIMO CLIENTE')
#     # ToastNotifier().show_toast("Pressione F9 para ativar o próximo cliente", duration=10)
#     press_key_b4('f1')
