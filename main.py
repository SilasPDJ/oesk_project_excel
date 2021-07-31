# import pgdas_fiscal_oesk
# from pgdas_fiscal_oesk import rotina_pgdas

from default.webdriver_utilities.pre_drivers import pgdas_driver, ginfess_driver
from default.sets import Consultar

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao

consultar = Consultar().consultar

razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas = list(*consultar(
    2))
input(razao_social)

PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples,
                compt=ATUAL_COMPT, driver=pgdas_driver, main_path=MAIN_FOLDER)
