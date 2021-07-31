# import pgdas_fiscal_oesk
# from pgdas_fiscal_oesk import rotina_pgdas

from default.webdriver_utilities.pre_drivers import pgdas_driver, ginfess_driver
from default.sets import Consultar
from default.sets import get_compt

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao

COMPT = get_compt(-1)

CONS = Consultar()
consultar = CONS.consultar
main_folder = CONS.MAIN_FOLDER
main_file = CONS.MAIN_FILE

geral = razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas = list(*consultar(
    2))
print(geral)


PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples,
                compt=COMPT, driver=pgdas_driver)
