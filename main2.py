from default.sets import InitialSetting
# import pgdas_fiscal_oesk
# from pgdas_fiscal_oesk import rotina_pgdas

from pgdas_fiscal_oesk.gias import GIA
from default.webdriver_utilities.pre_drivers import pgdas_driver, ginfess_driver
from default.sets import get_compt
from pgdas_fiscal_oesk import Consultar


from default.sets import get_all_valores

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui
from pgdas_fiscal_oesk.silas_abre_g5_loop_v8 import G5

COMPT = get_compt(-2)

CONS = Consultar(COMPT)
consultar_geral = CONS.consultar_geral
consultar_compt = CONS.consultar_compt

main_folder = CONS.MAIN_FOLDER
main_file = CONS.MAIN_FILE

TOTAL_CLIENTES = len(list(consultar_compt()))
IMPOSTOS_POSSIVEIS = ['ICMS, ISS']


for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
    razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = compt_vals
    __razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = geral

    if razao_social == __razao_social:

        path = InitialSetting.files_pathit(razao_social, COMPT)
        import os
        lspath = os.listdir(path)
        try:
            # print(path)
            f = open(os.path.join(path, 'NF_canceladas.txt')).read()
            print(razao_social)
            input(f) if f != '' else None
        except FileNotFoundError:
            pass

        # print(lspath) if 'REGISTRO_ISS' in str(lspath).upper() else None


# teste
# Set-ExecutionPolicy AllSigned
