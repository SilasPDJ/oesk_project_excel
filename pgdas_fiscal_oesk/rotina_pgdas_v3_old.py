# dale
from random import randint
# from default.sets import InitialSetting
# from default.webdriver_utilities.wbs import WDShorcuts
from default.interact import press_keys_b4, press_key_b4
from default.webdriver_utilities.pre_drivers import pgdas_driver, pgdas_driver_ua
from .rotina_pgdas_simplesnacional_utils import SimplesNacionalUtilities

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException

from time import sleep
from default.sets.pathmanager import HasJson
# from . import *
# qualquer coisa me devolve


# to fazendo um teste

# class SimplesNacionalUtilities(WDShorcuts, NewSetPaths, ExcelToData):
from .rotina_pgdas import PgdasDeclaracao as DeclaracaoMethods


class PgdasDeclaracao(DeclaracaoMethods):
    def __init__(self, *args, compt):
        self.compt = compt
        for __cli__ in args:
            __r_social, __cnpj, __cpf, __cod_simples, __valor_competencia, proc_ecac, all_valores = __cli__

            self.client_path = self.files_pathit(
                __r_social.strip(), self.compt)

            # drivers declarados
            [print('\033[1;33m', __cod_simples, '\033[m')for i in range(1)]

            if __cod_simples is None or __cod_simples == '-' or proc_ecac.lower().strip() == 'sim':
                if __cli__ == args[0]:
                    self.driver = driver = pgdas_driver_ua()
                    super().__init__(self.driver, self.compt, self.client_path)
                    self.loga_cert()
                self.enable_download_in_headless_chrome(self.client_path)
                self.change_ecac_client(__cnpj)
            else:
                self.driver = driver = pgdas_driver_ua(self.client_path)
                super().__init__(self.driver, self.compt, self.client_path)
                self.loga_simples(__cnpj, __cpf, __cod_simples, __r_social)

            if self.driver.current_url == "https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/AvisoMensagens.aspx":
                print("pressione f9 para continuar")
                press_keys_b4("f9")
                try:
                    self.driver.find_element(By.NAME,
                                             "ctl00$ContentPlaceHolder$btnContinuarSistema").click()
                except NoSuchElementException:
                    self.driver.refresh()
            self.current_url = self.driver.current_url
            self.link_gera_das, self.download_protocolos_das = 'Das/PorPa', '/Consulta'
            try:
                self.tag_with_text('span', 'DEVEDOR')
                self.criar_json_das_atrasados()
                self.gerar_das_atrasados_sem_parc()
            except NoSuchElementException:
                pass
            self.opta_script() if self.m() == 12 else None

            # loga e digita competencia de acordo com o BD
            self.compt_typist(self.compt)
            try:
                self.webdriverwait_el_by(By.ID, "msgBox", 3)
                self.opta_script(False)
            except (NoSuchElementException, TimeoutException):
                print("No msgBox")
            else:
                self.compt_typist(self.compt)
            # declara compt de acordo com o valor
            if not self.compt_already_declared(self.compt):
                __valor_competencia = 0 if float(
                    __valor_competencia) == 0 else __valor_competencia

                if float(__valor_competencia) == 0:
                    self.declaracao_sem_movimento(__valor_competencia)

                else:

                    self.declaracao_anexos(
                        all_valores, __valor_competencia, __cnpj)

            else:
                print('is already declared')

        self.sair_com_seguranca()
