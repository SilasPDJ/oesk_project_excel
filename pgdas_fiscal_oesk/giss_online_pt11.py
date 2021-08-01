# dale
from default.sets import InitialSetting
from default.webdriver_utilities.wbs import WDShorcuts
from default.interact import press_keys_b4, press_key_b4

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep
from . import *


weblink = 'https://portal.gissonline.com.br/login/index.html'

link = "ChromeDriver/chromedriver.exe"
# ...

sh_name = 'GISS'


# self.pyautogui
class GissGui(InitialSetting, WDShorcuts):

    def __init__(self, firstcompt=None):
        from functools import partial
        sh_names = ['GISS']
        # input(len(after_read['CNPJ']))

        self.compt_atual = super().get_compt_only()
        excel_file_name = super().excel_file_path()

        for sh_name in sh_names:
            # agora eu posso fazer downloalds sem me preocupar tendo a variável path
            mshExcelFile = pd.ExcelFile(excel_file_name)

            msh = mshExcelFile.parse(sheet_name=str(sh_name))
            col_str_dic = {column: str for column in list(msh)}
            msh = mshExcelFile.parse(
                sheet_name=str(sh_name), dtype=col_str_dic)
            READ = self.le_excel_each_one(msh)
            self.after_read = self.readnew_lista(READ, False)
            after_read = self.after_read
            with open('pgdas_fiscal_oesk/data_clients_files/giss_passwords.txt') as f:
                __senhas = f.read().split(',')

            [print(s) for s in __senhas]
            used_after_read = list(after_read.values())[:5]
            __giss_cnpj, __feito, __logar, self.__construcao, _anotacoes = used_after_read
            for i in range(len(__feito)):

                _giss_cliente, _feito, _logar, self._construcao, anotacoes = (__giss_cnpj[i], __feito[i], __logar[i], self.__construcao[i],
                                                                           _anotacoes[i])

                if _logar.strip() == "GISS LOGIN" or _feito.strip() != "":
                    continue
                    # ################################ essa lógica acima ...................................... continue
                for loop_compt in self.ate_atual_compt(first_compt=firstcompt):
                    [print(a) for a in self.ate_atual_compt(first_compt=firstcompt)]

                    # self.driver = ginfess_driver()
                    self.driver = pgdas_driver()
                    super().__init__(self.driver)
                    driver = self.driver
                    driver.get(weblink)
                    chrome = driver
                    cont_senha = 0
                    while True:
                        # TxtIdent
                        driver.find_element_by_xpath('//input[@name="TxtIdent"]').send_keys(_logar)
                        driver.find_element_by_xpath('//input[@name="TxtSenha"]').send_keys(__senhas[cont_senha])
                        print(f'Senha: {__senhas[cont_senha]}', end=' ')
                        cont_senha += 1
                        driver.find_element_by_link_text("Acessar").click()
                        try:
                            WebDriverWait(chrome, 5).until(expected_conditions.alert_is_present(),
                                                           'Timed out waiting for PA creation ' +
                                                           'confirmation popup to appear.')
                            alert = chrome.switch_to.alert
                            alert.accept()
                            print("estou no try")
                            driver.execute_script("window.history.go(-1)")
                        except TimeoutException:
                            print("no alert, sem alerta, exceptado")
                            break
                            # holy
                    """
                    for m in range(m_cont):
                        # print(self.write_date(m_cont, y_cont))
                        mes, ano = self.set_get_compt_file(m_cont, y_cont, file_type=False).split('-')
        
                        print(mes, ano)
                    input()
                    """

                    month, year = loop_compt.split('-')

                    self.calls_write_date = partial(self.write_date_variascompt, month, year)
                    try:
                        iframe = driver.find_element_by_xpath("//iframe[@name='header']")
                        driver.switch_to.frame(iframe)
                    except NoSuchElementException:
                        driver.execute_script("window.location.href=('/tomador/tomador.asp');")

                    if self._construcao.lower().strip() != 'sim':
                        driver.find_element_by_xpath("//img[contains(@src,'images/bt_menu__05_off.jpg')]").click()

                    else:
                        print('Construção Civil?')
                        self.constr_civil()
                    driver.switch_to.default_content()
                    sleep(1)
                    if self._construcao.lower() == 'sim':
                        self.fazendo_principal(True)
                    else:
                        self.fazendo_principal()
                    driver.implicitly_wait(10)
                self.driver.close()
        print('GISS encerrado!')

    def readnew_lista(self, READ, print_values=False):
        """ TRANSFORMO EM DICIONÁRIO, CONTINUAR"""
        get_all = {}
        new_lista = []
        for k, lista in READ.items():
            for v in lista:
                v = str(v)
                v = v.replace(u'\xa0', u' ')
                v = v.strip()
                if str(v) == 'nan':
                    v = ''
                new_lista.append(v)
            get_all[k] = new_lista[:]
            new_lista.clear()
        if print_values:
            for k, v in get_all.items():
                print(f'\033[1;32m{k}')
                for vv in v:
                    print(f'\033[m{vv}')
        return get_all

    def fazendo_principal(self, constr=False):
        """
        o click do prestador está no init
        :return:
        """

        driver = self.driver
        if not constr:
            self.calls_write_date()
        try:
            driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[4]/a').click()
            # driver.find_elements_by_xpath("//*[contains(text(), 'Encerrar Escrituração ')]")[0].click()
            try:
                sleep(2)
                driver.find_elements_by_xpath("//*[contains(text(), 'CLIQUE AQUI')]")[0].click()
                # PrintScreenFinal(clien)

            except (NoSuchElementException, IndexError):
                print('Provavelmente já foi declarada... Ou tem que encerrar sem movimento')
                # .................
        except NoSuchElementException:
            print('Exception line 140, sem PRESTADOR')
            # print("BACKEI. Aqui vai ser a parte 2")
        driver.switch_to.default_content()
        iframe = driver.find_element_by_xpath("//iframe[@name='header']")
        sleep(2.5)
        driver.switch_to.frame(iframe)
        driver.find_element_by_xpath('//img[contains(@src,"bt_menu__06_off.jpg")]').click()
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
                driver.find_elements_by_xpath("//*[contains(text(), 'CLIQUE AQUI')]")[0].click()
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
        driver.find_element_by_xpath('//img[contains(@src,"bt_menu__06_off.jpg")]').click()
        sleep(2)
        driver.switch_to.default_content()
        self.calls_write_date()
        for contX in range(len(XPATH)):
            driver.switch_to.default_content()
            sleep(2)

            iframe = driver.find_element_by_xpath("//iframe[@name='header']")
            driver.switch_to.frame(iframe)
            construcao = self._construcao
            driver.find_element_by_xpath('//img[contains(@src,"bt_menu__07_off.jpg")]').click()

            driver.switch_to.default_content()
            sleep(2)
            iframe = driver.find_element_by_xpath("//iframe[@name='principal']")
            driver.switch_to.frame(iframe)

            driver.find_element_by_xpath(XPATH[contX]).click()
            # XPATH
            # input("faça os processos daqui pra baixo")

            if contX == 0:
                ttt = 5.0
                for i in range(2):
                    sleep(ttt)
                    ttt -= 2.5
                    driver.find_element_by_xpath("//*[contains(text(), 'Encerrar Competência')]").click()
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
                driver.find_element_by_xpath("//*[contains(text(), 'Encerrar Escrituração')]").click()
                driver.find_elements_by_xpath("//*[contains(text(), 'CLIQUE AQUI')]")[0].click()
                # ENCERRADO
                sleep(5)

    def write_date_variascompt(self, mes, ano):
        driver = self.driver

        # mes, ano = self.set_get_compt_file(m_cont, y_cont, file_type=False).split('-')
        # print(f'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa {mes}---{ano}')

        sleep(5)
        iframe = driver.find_element_by_xpath("//iframe[@name='principal']")
        driver.switch_to.frame(iframe)
        self.tag_wait(driver, 'input')
        driver.find_element_by_xpath('//input[@name="mes"]').send_keys(mes)
        driver.find_element_by_xpath('//input[@name="ano"]').send_keys(ano)

    def tag_wait(self, driver, tag):
        delay = 10
        try:
            my_elem = WebDriverWait(driver, delay).until(expected_conditions.presence_of_element_located((By.TAG_NAME, tag)))
            print(f"\033[1;31m{tag.upper()}\033[m is ready!")
        except TimeoutException:
            input("Loading took too much time!")

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
                compt = first_compt = first_compt + relativedelta.relativedelta(months=1)

                compt_appended = f'{compt.month:02d}-{compt.year}'
                # list_compts.append(compt_appended)
                yield compt_appended

        #TODO: depois faço aprtindo do first_compt
        # O objetivo dessa função é retornar yildar um range de compt, partindo do first_compt

        # yield list_compts


GissGui()
