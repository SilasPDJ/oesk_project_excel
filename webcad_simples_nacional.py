import pandas as pd
##
#
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from wbs import WDShorcuts as Util
from webdriver_manager.chrome import ChromeDriverManager

from __backend import (COMPT, CONS, IMPOSTOS_POSSIVEIS, TOTAL_CLIENTES,
                       Backend, PgdasDeclaracaoFull, consultar_compt,
                       consultar_geral, get_compt, getfieldnames, main_file,
                       main_folder)

# pip install -i https://test.pypi.org/simple/ wds-utilities


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


ddriver = Util(driver)


class Main(Backend):

    def __init__(self):
        self.cadastro_rotina_servicos()
        # self.cadastro_geral()

    def any_to_str(self, *args):
        for v in args:
            yield "".join(str(v)) if str(v) != 'nan' else ""

    def cadastro_rotina_servicos(self):
        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios, imposto_a_calcular = list(
                self.any_to_str(*compt_vals))
            _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
                self.any_to_str(*geral))
            values = [cnpj, ginfess_link, gissonline, ginfess_cod, giss_login]

            if imposto_a_calcular.upper() == "ISS" or giss_login != '' or ginfess_cod != '':
                driver.get("http://localhost:8501/Empresas_de_Servicos")
                ddriver.webdriverwait_el_by(By.TAG_NAME, 'input')

                for cont, input in enumerate(driver.find_elements(By.TAG_NAME, "input")):
                    input.send_keys(values[cont])
                    # if input.get_attribute('aria-autocomplete') == "list":
                driver.find_elements(
                    By.CSS_SELECTOR, '[kind="secondaryFormSubmit"]')[-1].click()
            print(f'{razao_social} cadastrado')

    def cadastro_geral(self):
        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios, imposto_a_calcular = list(
                self.any_to_str(*compt_vals))
            _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
                self.any_to_str(*geral))
            driver.get("http://localhost:8501/cadastrar_empresa")
            # el = driver.find_element()

            tipo_empresa = "Simples Nacional"
            select_based = ddriver.webdriverwait_el_by(
                By.CSS_SELECTOR, '[data-baseweb="select"]')
            # select_based = select_based.find_element(By.TAG_NAME, 'input')
            # select_based.send_keys(tipo_empresa)

            _withcol_1 = driver.find_elements(By.TAG_NAME, "input")
            PREENCHER_01 = [razao_social, cnpj, cpf, email]
            for _indx, el in enumerate(_withcol_1):
                if el.get_attribute('aria-autocomplete') == "list":
                    el.send_keys(tipo_empresa)
                    el.send_keys(Keys.ENTER)
                else:
                    el.send_keys(PREENCHER_01[_indx])
            driver.find_elements(
                By.CSS_SELECTOR, '[kind="secondaryFormSubmit"]')[-1].click()
            from time import sleep
            sleep(2)

            # -- PRÓXIMA PÁGINA

            if codigo_simples == "-":
                proc_ecac = "SIM"
            PREENCHER_02 = [anexo, codigo_simples, proc_ecac, dividas_ativas]
            _withcol_2 = driver.find_elements(By.TAG_NAME, "input")[
                len(_withcol_1):]
            for _indx, el in enumerate(_withcol_2[1:]):
                el.send_keys(PREENCHER_02[_indx])
                # print(_withcol_1[0].get_attribute("aria-label"))
            el.send_keys(Keys.ENTER)
            # driver.find_elements(
            #     By.CSS_SELECTOR, '[kind="secondaryFormSubmit"]')[-1].click()
            ddriver.tag_with_text('button', 'ENVIAR').click()
            sleep(2)


Main()
