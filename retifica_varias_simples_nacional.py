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


# from pgdas_fiscal_oesk.relacao_nfs import iss_plan_exists, NfCanceled

from default.sets import get_all_valores

# from win10toast import ToastNotifier
import os

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
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

    def pgdas(compt=COMPT):
        print(razao_social)

        if declarado.upper() != 'OK' and imposto_a_calcular != 'LP' and (sem_ret != "nan" or com_ret != "nan"):
            # ret!='nan' remove o erro de declarar sem o "zerou na planilha"
            # NÃO PRECISA MAIS NECESSARIAMENTE FICAR MARCANDO COM OK...
            print(declarado, valor_tot, imposto_a_calcular)
            # if float(valor_tot) == 0 or str(valor_tot) in ['zerou', 'nan']:
            if str(valor_tot) == "0":
                # if imposto_a_calcular == 'SEM_MOV':
                PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
                                compt=compt)
            elif imposto_a_calcular.strip() in IMPOSTOS_POSSIVEIS:
                all_valores = get_all_valores(
                    sem_ret, com_ret, anexo, valor_tot)
                print(all_valores)
                if all_valores:
                    PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
                                    compt=compt,
                                    all_valores=all_valores)
                elif all_valores is False:
                    PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
                                    compt=compt,)
                else:  # None
                    raise ValueError(
                        f'{razao_social.upper()} possui problemas na planilha')
        else:
            print(
                f"Não irei declarar {razao_social}, pois não 'zerou' ou não declarou valor")

    if cnpj == '20367544000101':  # CNPJ requerido
        _calc_a_partir = 14 + (12 * 5)
        for compt in InitialSetting.ate_atual_compt(get_compt(-3), get_compt(_calc_a_partir)):
            # pgdas()
            print(compt)
        # path_final = [*str(__path).split('/')[:-1], __new_folder, razao_social]
        # Dirs.pathit(*path_final)
