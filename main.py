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
from pgdas_fiscal_oesk.silas_jr import JR
from pgdas_fiscal_oesk.export2same_folder import Export2SameFolder
import os


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

        # JUNIOR
        if nf_out.lower() == 'ok':
            if declarado not in ['S', 'OK']:

                JR(razao_social, cnpj, cpf, codigo_simples,
                   valor_tot, imposto_a_calcular, nf_out, compt=COMPT)
        else:
            if imposto_a_calcular == 'ISS':
                Export2SameFolder(razao_social, cnpj,
                                  compt=COMPT).iss()
            # export.unzip_folder()
            # g5 loop

            # G5(razao_social, cnpj, cpf, codigo_simples, valor_tot, imposto_a_calcular)
            # teste
            # Set-ExecutionPolicy AllSigned
Export2SameFolder('', '', compt=COMPT).icms()
