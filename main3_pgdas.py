# import pgdas_fiscal_oesk
# from pgdas_fiscal_oesk import rotina_pgdas

from pgdas_fiscal_oesk.gias import GIA
from default.webdriver_utilities.pre_drivers import pgdas_driver, ginfess_driver
from default.sets import get_compt
from pgdas_fiscal_oesk import Consultar


from default.sets import get_all_valores

from pgdas_fiscal_oesk.rotina_pgdas_v2 import PgdasDeclaracao
from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui
from pgdas_fiscal_oesk.silas_abre_g5_loop_v8 import G5

COMPT = get_compt(-1)

CONS = Consultar(COMPT)
consultar_geral = CONS.consultar_geral
consultar_compt = CONS.consultar_compt

main_folder = CONS.MAIN_FOLDER
main_file = CONS.MAIN_FILE

TOTAL_CLIENTES = len(list(consultar_compt()))
IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']


def any_to_str(*args):
    for v in args:
        yield "".join(str(v))


def pgdas():
    LIST_ECAC = []
    LIST_NORMAL = []

    for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
        razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = list(
            any_to_str(*compt_vals))
        __razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
            any_to_str(*geral))
        envio = envio.upper()
        email = email.strip()
        dividas_ativas = dividas_ativas.strip().lower()

        print(razao_social)

        def append_me(obj_list):
            if float(valor_tot) == 0 or str(valor_tot) in ['zerou', 'nan']:
                # if imposto_a_calcular == 'SEM_MOV':
                obj_list.append((razao_social, cnpj, cpf,
                                 codigo_simples, valor_tot, proc_ecac, None))
            elif imposto_a_calcular.strip() in IMPOSTOS_POSSIVEIS:
                all_valores = get_all_valores(
                    sem_ret, com_ret, anexo, valor_tot)

                if all_valores:
                    obj_list.append(
                        (razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac, all_valores))
                elif all_valores is False:
                    obj_list.append((razao_social, cnpj, cpf,
                                     codigo_simples, valor_tot, proc_ecac, None))
                else:  # None
                    raise ValueError(
                        f'{razao_social.upper()} possui problemas na planilha')

        if declarado.upper() != 'S' and declarado != 'OK':
            print(declarado, valor_tot, imposto_a_calcular)

            if proc_ecac.lower() == "sim":
                append_me(LIST_ECAC)
            else:
                append_me(LIST_NORMAL)

        # PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
        #             compt=COMPT, driver=pgdas_driver)
        # Não tem mais arg all_valores (está embutido)

    return LIST_ECAC, LIST_NORMAL


list_ecac, list_normal = pgdas()

PgdasDeclaracao(*list_ecac, compt=COMPT, driver=pgdas_driver)

input(list_ecac)
input(list_normal)
