# dale
from bs4 import BeautifulSoup
from default.sets import InitialSetting
from default.webdriver_utilities.pre_drivers import ginfess_driver, pgdas_driver
from default.webdriver_utilities.wbs import WDShorcuts
from default.interact import press_keys_b4, press_key_b4

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
# from . import *
# qualquer coisa me devolve


weblink = 'https://portal.gissonline.com.br/login/index.html'

link = "ChromeDriver/chromedriver.exe"
# ...


# self.pyautogui
class GissGui(InitialSetting, WDShorcuts):

    def __init__(self, dados, compt, first_compt=None):
        from functools import partial
        with open('pgdas_fiscal_oesk/data_clients_files/giss_passwords.txt') as f:
            __senhas = f.read().split(',')
        # [print(s) for s in __senhas]
        __r_social, _giss_cnpj, _logar = dados[:3]
        self.compt_atual = compt
        print(self.compt_atual)
        self.client_path = self.files_pathit(
            __r_social.strip(), compt)

        if not self.certifs_exist('giss'):
            self.driver = driver = ginfess_driver(self.client_path)
            # self.driver = driver = pgdas_driver(self.client_path)
            super().__init__(self.driver)
            [print(a)
                for a in self.ate_atual_compt(first_compt)]

            # self.driver = ginfess_driver()

            # holy
            cont_senha = 0
            while True:
                # TxtIdent
                self.driver.get(weblink)
                driver.find_element(By.XPATH,
                                    '//input[@name="TxtIdent"]').send_keys(_logar)
                driver.find_element(By.XPATH,
                                    '//input[@name="TxtSenha"]').send_keys(__senhas[cont_senha])
                print(f'Senha: {__senhas[cont_senha]}', end=' ')
                cont_senha += 1
                driver.find_element(By.LINK_TEXT, "Acessar").click()
                try:
                    WebDriverWait(driver, 5).until(expected_conditions.alert_is_present(),
                                                   'Timed out waiting for PA creation ' +
                                                   'confirmation popup to appear.')
                    alert = driver.switch_to.alert
                    alert.accept()
                    print("estou no try")
                    driver.execute_script("window.history.go(-1)")
                except TimeoutException:
                    print("no alert, sem alerta, exceptado")
                    break
            for loop_compt in self.ate_atual_compt(first_compt):
                # driver.get(
                #     'https://www10.gissonline.com.br/interna/default.cfm')
                driver.refresh()
                month, year = loop_compt.split('-')

                self.calls_write_date = partial(
                    self.write_date_variascompt, month, year)
                try:
                    iframe = driver.find_element(By.XPATH,
                                                 "//iframe[@name='header']")
                    driver.switch_to.frame(iframe)
                except NoSuchElementException:
                    driver.execute_script(
                        "window.location.href=('/tomador/tomador.asp');")
                # principal MENU frame...
                # a = driver.find_elements(By.TAG_NAME, "iframe")[0]
                # driver.switch_to.frame(a)
                # driver.execute_script(
                #     "javascript: clickTomador(); FunImg('6');")

                constr = False
                try:
                    driver.find_element(By.XPATH,
                                        "//img[contains(@src,'images/bt_menu__05_off.jpg')]").click()
                    # Try prestador, else = Construção civil
                except (NoSuchElementException, ElementNotInteractableException):
                    self.constr_civil()
                    self.gerar_cert('giss-construcao.png')
                    constr = True
                finally:
                    driver.switch_to.default_content()
                    sleep(1)
                    self.fazendo_principal(constr)
                    self.gerar_cert('giss-tomador.png')

                driver.implicitly_wait(10)
            driver.close()
        print('GISS encerrado!')

    def certifs_exist(self, startswith, at_least=2):
        arqs_search = self.files_get_anexos_v4(self.client_path, 'png')
        arqs_search = [
            self.path_leaf(f, True) for f in arqs_search]
        arqs_search = [f for f in arqs_search if f.startswith(startswith)]

        if len(arqs_search) >= at_least:
            return True
        return False

    def gerar_cert(self, arq):
        import os
        save = os.path.join(self.client_path, arq)
        self.driver.save_screenshot(save)

    def fazendo_principal(self, constr=False):
        """
        o click do prestador está no init
        :return:
        """

        driver = self.driver
        if not constr:
            self.calls_write_date()

        self.__check_prestador_guias()
        input('teste volto pra onde')
        try:
            driver.find_element(By.XPATH,
                                '/html/body/form/table[2]/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[4]/a').click()
            # driver.find_elements(By.XPATH, "//*[contains(text(), 'Encerrar Escrituração ')]")[0].click()
            try:
                sleep(2)
                driver.find_elements(By.XPATH,
                                     "//*[contains(text(), 'CLIQUE AQUI')]")[0].click()
                self.gerar_cert('giss-prestador.png')
                # PrintScreenFinal(clien)

            except (NoSuchElementException, IndexError):
                print(
                    'Provavelmente já foi declarada... Ou tem que encerrar sem movimento')
            except UnexpectedAlertPresentException as e:
                # Não é possível encerrar pelo motivo in abaixo...
                texto = e.alert_text
                if "Empresa Não Incide I.S.S.Q.N" in texto:
                    # driver.switch_to.alert.accept()
                    # não posso aceitar pq não é encontrado
                    pass
                else:
                    raise e

                # .................
        except NoSuchElementException:
            print('Exception line 140, sem PRESTADOR')
            # print("BACKEI. Aqui vai ser a parte 2")
        driver.switch_to.default_content()
        iframe = driver.find_element(By.XPATH, "//iframe[@name='header']")
        sleep(2.5)
        driver.switch_to.frame(iframe)
        driver.find_element(By.XPATH,
                            '//img[contains(@src,"bt_menu__06_off.jpg")]').click()
        driver.switch_to.default_content()
        iframe = driver.find_element(By.XPATH, "//iframe[@name='principal']")
        driver.switch_to.frame(iframe)

        """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TOMADOR """
        cont = 0
        for i in range(2):
            sleep(3)
            a = driver.find_elements(By.TAG_NAME, 'a')
            print(len(a))

            a[4].click()
            sleep(1.5)
            try:
                driver.find_elements(By.XPATH,
                                     "//*[contains(text(), 'CLIQUE AQUI')]")[0].click()
                break
            except IndexError:
                try:
                    driver.find_element(By.LINK_TEXT, 'Menu Principal').click()
                except NoSuchElementException:
                    driver.find_element(By.LINK_TEXT, 'OK').click()

        # pressione "ESC" para continuar
    def __check_prestador_guias(self):
        def __download_prestador_guias():
            tb = self.driver.find_element(By.TAG_NAME, 'table')
            __meses_guias = tb.find_elements(By.TAG_NAME, 'a')
            MESES, GUIAS = (
                [mes for mes in __meses_guias if mes.text != ''],
                [guia for guia in __meses_guias if guia.text == '']
            )
            # [print(mes.text) for mes in meses]
            # [print(guia) for guia in guias]

            # SOUP to compare values part
            soup = BeautifulSoup(tb.get_attribute('innerHTML'), 'html.parser')
            rows = soup.find_all('tr')
            vals_pagos, vals_abertos = [], []
            for row in rows[1:]:
                def trata_val(v):
                    try:
                        return float(v.replace(',', '.'))
                    except ValueError:
                        print('value error')
                        return v
                _vcobs, _vrecs = [r for r in row.find_all('td')[5:7]]
                vals_pagos.append(trata_val(_vcobs.text))
                vals_abertos.append(trata_val(_vrecs.text))

            # get indexes for GUIAS
            vals_pendentes = []
            for cont, (val_pago, val_em_aberto) in enumerate(zip(vals_pagos, vals_abertos)):
                if val_em_aberto != 0:
                    # print(val_em_aberto)
                    vals_pendentes.append(cont)
            # gera guias a pagar
            __meses = []  # for naming certificate of existing guias file
            for indx in vals_pendentes:
                guia, mes = GUIAS[indx], MESES[indx].text
                __meses.append(mes)
                # generate guia
                # guia.click()
            __meses = "_".join(__meses)
            self.driver.save_screenshot(
                f'{self.client_path}/{__meses}-GUIASpendentes-giss.png')
            GUIAS[-1].click()  # the last one
            self.webdriverwait_el_by(By.TAG_NAME, 'a').click()  # download...
            print('Downlaod da ultima guia funcional')
            print('~'*10, f'meses abertos: {__meses}')

        driver = self.driver

        # driver.find_element(By.XPATH,
        #     '//img[contains(@src,"bt_menu__05_off.jpg")]').click()
        driver.switch_to.default_content()
        iframe = driver.find_element(By.XPATH, "//iframe[@name='principal']")
        driver.switch_to.frame(iframe)
        el = self.tag_with_text('a', 'Conta Corrente')

        el.click()
        # year_selected = self.tag_with_text('font', self.compt_atual.split('-')[-1])
        # self.click_ac_elementors(year_selected)
        self.click_elements_by_tt(self.compt_atual.split('-')[-1])

        # tabela com as guias
        # table = self.driver.find_elements(By.TAG_NAME, 'table')[1]
        table = self.driver.find_elements(By.TAG_NAME, 'table')[1]
        iframe = table.find_element(By.XPATH, "//iframe[@name='conteudo']")
        self.driver.switch_to.frame(iframe)

        __download_prestador_guias()

        # driver.find_element(By.ID, )
        driver.switch_to.default_content()
        driver.switch_to.default_content()
        iframe = driver.find_element(By.XPATH, "//iframe[@name='header']")
        driver.switch_to.frame(iframe)
        driver.execute_script('javascript: clickPrestador(); ')
        driver.switch_to.default_content()
        input('deu certo?')

    def constr_civil(self):
        # parei nessa belezinha aqui, tomador e prestador tão ok
        XPATH = "//*[contains(text(), '- Serviço da Construção Civil')]", "//*[contains(text(), '- Demais Serviços')]"

        driver = self.driver
        driver.find_element(By.XPATH,
                            '//img[contains(@src,"bt_menu__06_off.jpg")]').click()
        sleep(2)
        driver.switch_to.default_content()
        self.calls_write_date()
        for contX in range(len(XPATH)):
            driver.switch_to.default_content()
            sleep(2)

            iframe = driver.find_element(By.XPATH, "//iframe[@name='header']")
            driver.switch_to.frame(iframe)
            driver.find_element(By.XPATH,
                                '//img[contains(@src,"bt_menu__07_off.jpg")]').click()

            driver.switch_to.default_content()
            sleep(2)
            iframe = driver.find_element(By.XPATH,
                                         "//iframe[@name='principal']")
            driver.switch_to.frame(iframe)

            driver.find_element(By.XPATH, XPATH[contX]).click()
            # XPATH
            # input("faça os processos daqui pra baixo")

            if contX == 0:
                ttt = 5.0
                for i in range(2):
                    sleep(ttt)
                    ttt -= 2.5
                    driver.find_element(By.XPATH,
                                        "//*[contains(text(), 'Encerrar Competência')]").click()
                try:
                    WebDriverWait(driver, 3).until(expected_conditions.alert_is_present(),
                                                   'Timed out waiting for PA creation ' +
                                                   'confirmation popup to appear.')
                    # ENCERRADO
                    driver.switch_to.alert.accept()
                    sleep(5)
                except (NoAlertPresentException, TimeoutException):
                    print('no alert')

                driver.refresh()
                # input('drive refresh')
            elif contX == 1:
                driver.find_element(By.XPATH,
                                    "//*[contains(text(), 'Encerrar Escrituração')]").click()
                driver.find_elements(By.XPATH,
                                     "//*[contains(text(), 'CLIQUE AQUI')]")[0].click()
                # ENCERRADO
                sleep(5)

    def write_date_variascompt(self, mes, ano):
        driver = self.driver

        # mes, ano = self.set_get_compt_file(m_cont, y_cont, file_type=False).split('-')
        # print(f'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa {mes}---{ano}')

        sleep(5)
        iframe = driver.find_element(By.XPATH, "//iframe[@name='principal']")
        driver.switch_to.frame(iframe)
        self.tags_wait('input')
        m = driver.find_element(By.XPATH, '//input[@name="mes"]')
        a = driver.find_element(By.XPATH, '//input[@name="ano"]')
        m.clear()
        a.clear()
        m.send_keys(mes)
        a.send_keys(ano)

    def ate_atual_compt(self, first_compt=None):

        from datetime import date
        from dateutil import relativedelta
        if first_compt is None:
            yield self.compt_atual
        else:
            first_compt = first_compt.split('-')
            if len(first_compt) == 1:
                first_compt = first_compt.split('/')
            first_compt = [int(val) for val in first_compt]
            first_compt = date(first_compt[1], first_compt[0], 1)

            # next_date = first_compt + relativedelta.relativedelta(months=1)

            last_compt = self.compt_atual.split('-')
            # compt = [int(c) for c in compt]
            last_compt = [int(v) for v in last_compt]
            last_compt = date(last_compt[1], last_compt[0], 1)

            list_compts = []
            while first_compt != last_compt:
                compt = first_compt = first_compt + \
                    relativedelta.relativedelta(months=1)

                compt_appended = f'{compt.month:02d}-{compt.year}'
                # list_compts.append(compt_appended)
                yield compt_appended

        # TODO: depois faço aprtindo do first_compt
        # O objetivo dessa função é retornar yildar um range de compt, partindo do first_compt

        # yield list_compts
