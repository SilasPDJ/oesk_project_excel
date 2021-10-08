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

    if razao_social == __razao_social:

        # print(razao_social)
        def pgdas():
            print(razao_social)

            if declarado.upper() != 'S' and declarado != 'OK':
                print(declarado, valor_tot, imposto_a_calcular)
                if float(valor_tot) == 0 or str(valor_tot) in ['zerou', 'nan']:
                    # if imposto_a_calcular == 'SEM_MOV':
                    PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
                                    compt=COMPT, driver=pgdas_driver)
                elif imposto_a_calcular.strip() in IMPOSTOS_POSSIVEIS:
                    all_valores = get_all_valores(
                        sem_ret, com_ret, anexo, valor_tot)
                    print(all_valores)
                    if all_valores:
                        PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
                                        compt=COMPT, driver=pgdas_driver,
                                        all_valores=all_valores)
                    elif all_valores is False:
                        PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
                                        compt=COMPT, driver=pgdas_driver)
                    else:  # None
                        raise ValueError(
                            f'{razao_social.upper()} possui problemas na planilha')

        # Giss Online
        # Auto Giss Online

        def giss_online():
            if str(giss_login).lower().strip() not in ['ginfess cód', 'não há'] and str(giss_login) != 'nan':

                print(str(giss_login))
                GissGui([razao_social, cnpj, giss_login],
                        pgdas_driver, COMPT)
                # GissGui([razao_social, cnpj, giss_login],
                #         driver=pgdas_driver, compt=COMPT, first_compt='04-2019')
        # pgdas()

        # JUNIOR
        if nf_out.lower() == 'ok' and declarado not in ['S', 'OK']:
            from pgdas_fiscal_oesk.silas_jr import JR
            JR(razao_social, cnpj, cpf, codigo_simples,
               valor_tot, imposto_a_calcular, nf_out, compt=COMPT)

        # giss_online()
        # pgdas()
        # Ginfess

        # print(razao_social)
        # if str(ginfess_link) != 'nan':
        #     DownloadGinfessGui(razao_social, cnpj, str(ginfess_cod),
        #                        ginfess_link, driver=ginfess_driver, compt=COMPT)

        # g5 loop

        # G5(razao_social, cnpj, cpf, codigo_simples, valor_tot, imposto_a_calcular)
# teste
# Set-ExecutionPolicy AllSigned
