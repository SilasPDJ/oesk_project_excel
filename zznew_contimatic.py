# import pgdas_fiscal_oesk
# from pgdas_fiscal_oesk import rotina_pgdas

# from default.sets.pathmanager import Dirs
from pgdas_fiscal_oesk.gias import GIA
from default.webdriver_utilities.pre_drivers import pgdas_driver, ginfess_driver
from default.sets import InitialSetting, get_compt
from pgdas_fiscal_oesk import Consultar

from time import sleep
import pyautogui as pygui
from default.interact import *


from pgdas_fiscal_oesk.relacao_nfs import iss_plan_exists, NfCanceled

from default.sets import get_all_valores

# from win10toast import ToastNotifier
import os
# os.system('d:/PROGRAMAS/oesk_project_excel-master/venv/Scripts/activate.bat')
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


for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
    razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = list(
        any_to_str(*compt_vals))
    __razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
        any_to_str(*geral))
    envio = envio.upper()
    email = email.strip()
    dividas_ativas = dividas_ativas.strip().lower()

    if imposto_a_calcular == 'ICMS':
        __new_folder = 'NOVA_CONTIMATIC'

        if str(nf_in).strip() != "não há":
            __path = InitialSetting.files_pathit(
                razao_social, 'ENTRADAS', __new_folder)
            input(__path)
        if str(nf_out).strip() != "não há":
            __path = InitialSetting.files_pathit(
                razao_social, 'SAÍDAS', __new_folder)

            input(__path)
        # path_final = [*str(__path).split('/')[:-1], __new_folder, razao_social]
        # Dirs.pathit(*path_final)
