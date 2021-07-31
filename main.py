# import pgdas_fiscal_oesk
# from pgdas_fiscal_oesk import rotina_pgdas
from pgdas_fiscal_oesk import *
from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao

from default.webdriver_utilities.pre_drivers import pgdas_driver, ginfess_driver
PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples,
                compt=ATUAL_COMPT, driver=pgdas_driver, main_path=MAIN_FOLDER)
