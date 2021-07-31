# import pgdas_fiscal_oesk
# from pgdas_fiscal_oesk import rotina_pgdas

from default.webdriver_utilities.pre_drivers import pgdas_driver, ginfess_driver
from default.sets import get_compt
from pgdas_fiscal_oesk import Consultar


from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao

COMPT = get_compt(-1)

CONS = Consultar()
consultar_geral = CONS.consultar_geral
consultar_compt = CONS.consultar_compt

main_folder = CONS.MAIN_FOLDER
main_file = CONS.MAIN_FILE

TOTAL_CLIENTES = len(list(consultar_compt()))

for part in consultar_compt():
    dal = razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, envio, div_envios = part
    print(part)



input('a')
PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples,
                compt=COMPT, driver=pgdas_driver)
