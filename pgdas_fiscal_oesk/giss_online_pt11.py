# dale
from default.sets import InitialSetting
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

    def __init__(self, dados, driver, compt, first_compt=None):
        from functools import partial
        with open('pgdas_fiscal_oesk/data_clients_files/giss_passwords.txt') as f:
            __senhas = f.read().split(',')
        # [print(s) for s in __senhas]
        __r_social, _giss_cnpj, _logar = dados[:3]
        self.compt_atual = compt
        print(self.compt_atual)
        self.client_path = self.files_pathit(
            __r_social.strip(), compt)

        if not self.certifs_exist():
            self.driver = driver(self.client_path)
            driver = self.driver
            super().__init__(self.driver)
            [print(a)
                for a in self.ate_atual_compt(first_compt)]

            # self.driver = ginfess_driver()

            # holy
            cont_senha = 0
            while True:
                # TxtIdent
                self.driver.get(weblink)
                driver.find_element_by_xpath(
                    '//input[@name="TxtIdent"]').send_keys(_logar)
                driver.find_element_by_xpath(
                    '//input[@name="TxtSenha"]').send_keys(__senhas[cont_senha])
                print(f'Senha: {__senhas[cont_senha]}', end=' ')
                cont_senha += 1
                driver.find_element_by_link_text("Acessar").click()
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
                    iframe = driver.find_element_by_xpath(
                        "//iframe[@name='header']")
                    driver.switch_to.frame(iframe)
                except NoSuchElementException:
                    driver.execute_script(
                        "window.location.href=('/tomador/tomador.asp');")
                # principal MENU frame...
                # a = driver.find_elements_by_tag_name("iframe")[0]
                # driver.switch_to.frame(a)
                # driver.execute_script(
                #     "javascript: clickTomador(); FunImg('6');")

                constr = False
                try:
                    driver.find_element_by_xpath(
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

    def certifs_exist(self, at_least=2):
        arqs_search = self.files_get_anexos_v4(self.client_path, 'png')
        arqs_search = [
            self.path_leaf(f, True) for f in arqs_search]
        arqs_search = [f for f in arqs_search if f.startswith('giss')]

        if len(arqs_search) >= at_least:
            return True
        return False

    def gerar_cert(self, arq):
        import os
        arq = 'gissoline.png' if arq is None else arq
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
        try:
            driver.find_element_by_xpath(
                '/html/body/form/table[2]/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[4]/a').click()
            # driver.find_elements_by_xpath("//*[contains(text(), 'Encerrar Escrituração ')]")[0].click()
            try:
                sleep(2)
                driver.find_elements_by_xpath(
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
                    driver.switch_to.alert.accept()
                    pass
                else:
                    raise e

                # .................
        except NoSuchElementException:
            print('Exception line 140, sem PRESTADOR')
            # print("BACKEI. Aqui vai ser a parte 2")
        driver.switch_to.default_content()
        iframe = driver.find_element_by_xpath("//iframe[@name='header']")
        sleep(2.5)
        driver.switch_to.frame(iframe)
        driver.find_element_by_xpath(
            '//img[contains(@src,"bt_menu__06_off.jpg")]').click()
        driver.switch_to.default_content()
        iframe = driver.find_element_by_xpath("//iframe[@name='principal']")
        driver.switch_to.frame(iframe)

        """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TOMADOR """
        cont = 0
        for i in range(2):
            sleep(3)
            a = driver.find_elements_by_tag_name('a')
            print(len(a))

            a[4].click()
            sleep(1.5)
            try:
                driver.find_elements_by_xpath(
                    "//*[contains(text(), 'CLIQUE AQUI')]")[0].click()
                break
            except IndexError:
                try:
                    driver.find_element_by_link_text('Menu Principal').click()
                except NoSuchElementException:
                    driver.find_element_by_link_text('OK').click()

        # pressione "ESC" para continuar

    def constr_civil(self):
        # parei nessa belezinha aqui, tomador e prestador tão ok
        XPATH = "//*[contains(text(), '- Serviço da Construção Civil')]", "//*[contains(text(), '- Demais Serviços')]"

        driver = self.driver
        driver.find_element_by_xpath(
            '//img[contains(@src,"bt_menu__06_off.jpg")]').click()
        sleep(2)
        driver.switch_to.default_content()
        self.calls_write_date()
        for contX in range(len(XPATH)):
            driver.switch_to.default_content()
            sleep(2)

            iframe = driver.find_element_by_xpath("//iframe[@name='header']")
            driver.switch_to.frame(iframe)
            driver.find_element_by_xpath(
                '//img[contains(@src,"bt_menu__07_off.jpg")]').click()

            driver.switch_to.default_content()
            sleep(2)
            iframe = driver.find_element_by_xpath(
                "//iframe[@name='principal']")
            driver.switch_to.frame(iframe)

            driver.find_element_by_xpath(XPATH[contX]).click()
            # XPATH
            # input("faça os processos daqui pra baixo")

            if contX == 0:
                ttt = 5.0
                for i in range(2):
                    sleep(ttt)
                    ttt -= 2.5
                    driver.find_element_by_xpath(
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
                driver.find_element_by_xpath(
                    "//*[contains(text(), 'Encerrar Escrituração')]").click()
                driver.find_elements_by_xpath(
                    "//*[contains(text(), 'CLIQUE AQUI')]")[0].click()
                # ENCERRADO
                sleep(5)

    def write_date_variascompt(self, mes, ano):
        driver = self.driver

        # mes, ano = self.set_get_compt_file(m_cont, y_cont, file_type=False).split('-')
        # print(f'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa {mes}---{ano}')

        sleep(5)
        iframe = driver.find_element_by_xpath("//iframe[@name='principal']")
        driver.switch_to.frame(iframe)
        self.tags_wait('input')
        m = driver.find_element_by_xpath('//input[@name="mes"]')
        a = driver.find_element_by_xpath('//input[@name="ano"]')
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
