# import pgdas_fiscal_oesk
# from pgdas_fiscal_oesk import rotina_pgdas

# from default.sets.pathmanager import Dirs
from datetime import datetime
import pandas as pd
from pgdas_fiscal_oesk.gias import GIA
from default.webdriver_utilities.pre_drivers import pgdas_driver, ginfess_driver
from default.sets import InitialSetting, get_compt
from pgdas_fiscal_oesk import Consultar

from time import sleep
import pyautogui as pygui
from default.interact import *


# from pgdas_fiscal_oesk.relacao_nfs import iss_plan_exists, NfCanceled

from default.sets import get_all_valores

# from win10toast import ToastNotifier
import os

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracaoRetificaVarias
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
    razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, imposto_a_calcular = list(
        any_to_str(*compt_vals))
    _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, proc_ecac = list(
        any_to_str(*geral))
    envio = envio.upper()
    email = email.strip()

    proc_ecac = proc_ecac.lower()
    imposto_a_calcular = imposto_a_calcular.upper()

    if cnpj == '20367544000101':  # CNPJ requerido
        _calc_a_partir = 14 + (12 * 5)
        df = pd.read_excel(
            r"O:\OneDrive\_FISCAL-2021\2023\faturamento revisão danilo ano 2022 era do mei_.xlsx")
        print(df)
        # compts_loop = list(InitialSetting.ate_atual_compt(
        #     get_compt(-3), get_compt(_calc_a_partir)))

        # for e, compt in enumerate(compts_loop):
        for e in range(len(df)):
            # compt = df_compt = datetime.date(df.iloc[0, e]).strftime("%m-%Y")

            cell_value = df.iloc[e, 0]
            compt_init = pd.to_datetime(cell_value)
            compt = compt_init.strftime("%m-%Y")
            if e > 11:
                valor_nao_retido = df.iloc[e, 1]
                anexo = df.iloc[e, -1]
                valor_tot = valor_nao_retido + 0
                all_valores = [{'valor_n_retido': valor_nao_retido,
                               'valor_retido': 0, 'anexo': 'III'}]
                PgdasDeclaracaoRetificaVarias(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
                                              compt=compt, main_compt=COMPT,
                                              all_valores=all_valores)

        # path_final = [*str(__path).split('/')[:-1], __new_folder, razao_social]
        # Dirs.pathit(*path_final)
