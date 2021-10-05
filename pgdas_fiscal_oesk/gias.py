# dale
from default.sets import InitialSetting
from default.webdriver_utilities.wbs import WDShorcuts
from default.interact import *

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException,  NoSuchElementException, ElementClickInterceptedException
from time import sleep

import pyautogui as pygui
import os

link = "ChromeDriver/chromedriver.exe"
possible = ['GIA']


class GIA(InitialSetting, WDShorcuts):

    def __init__(self, *args, compt, driver):

        __r_social, __cnpj, login, senha = args

        # __anexo,  __valor_n_ret, __valor_ret, already_declared

        # competencia declarada
        self.compt_used = compt

        self.client_path = self.files_pathit(
            __r_social.strip(), self.compt_used)
        # self.client_path = self.pathit(self.compt, main_path, __r_social)

        # drivers declarados
        self.driver = driver(self.client_path)
        menuX, menuY = 20, 27

        def fecha_janela_contribuintes_gia():
            sleep(1)
            pygui.click(1322, 333, duration=.5)
            pygui.hotkey('left', 'enter')
        # self.GIA()

        #
        # mudei do for pra ca
        self.abre_programa(self.get_env_for_path(
            '\\Desktop\\GIA.exe'), path=True)

        IE = __cnpj
        my_print = login
        print(my_print)
        # pygui.hotkey('alt', 'tab')
        print(IE)
        #

        try:
            fecha_janela_contribuintes_gia()
        except IndexError:
            print('Não precisei fechar')
        self.pt1_gia_software(IE, self.compt_used)

        pygui.doubleClick(menuX+35, menuY)
        # consistir
        sleep(3)
        pygui.click(menuX, menuY)
        sleep(.5)
        foritab(2, 'up')
        pygui.hotkey('enter')
        pygui.click(x=836, y=394)
        foritab(7, 'tab')
        pygui.hotkey('enter', 'enter', interval=.25)
        pygui.hotkey('enter')
        self.save_novagia_pdf()

        # if certificado...
        if not self.certifs_exist('GiaScreenShoot', 1):

            self.driver = driver(self.client_path)
            driver = self.driver
            super().__init__(self.driver)
            driver.get(
                'https://www3.fazenda.sp.gov.br/CAWEB/Account/Login.aspx')
            llg = driver.find_element_by_id(
                'ConteudoPagina_txtUsuario')
            llg.clear()
            llg.send_keys(login)

            ssn = driver.find_element_by_xpath(
                "//input[@type='password']")
            ssn.clear()
            ssn.send_keys(senha)

            self.send_keys_anywhere(Keys.TAB)
            self.send_keys_anywhere(Keys.ENTER)
            print('pressione f7 p/ continuar após captcha')
            press_key_b4('f8')
            # self.find_submit_form()
            # enter entrar
            sleep(5)
            driver.find_element_by_link_text('Nova GIA').click()
            sleep(3)
            driver.find_element_by_partial_link_text(
                'Documentos Fiscais (Normal, Substit. e Coligida)').click()
            sleep(2)
            driver_clicks = driver.find_elements_by_xpath(
                "//input[@type='file']")

            driver_clicks[0].send_keys(self.clieninput_filepath())
            driver.find_elements_by_xpath(
                "//input[@type='button']")[0].click()
            try:
                driver.switch_to.alert.accept()
            except NoAlertPresentException:
                print('Sem alerta')
            sleep(5)
            """
            bt_imprime = driver.find_element_by_css_selector('[alt="Imprimir"]')
            self.exec_list(click=bt_imprime, enter=pygui)
            print('Glória a Deus f7 p continuar')
            press_key_b4('f7')
            """
            self.save_save_img2pdf()
            driver.close()
            sleep(5)
            # pygui.hotkey('enter')
            # ############################################ parei daqui

    def save_save_img2pdf(self):
        from PIL import Image
        path1 = f'{self.client_path}/GiaScreenShoot.png'
        path2 = f'{self.client_path}/Recibo_{self.compt_used}.pdf'
        self.driver.save_screenshot(path1)
        image1 = Image.open(path1)
        try:
            im1 = image1.convert('RGB')
        except ValueError:
            im1 = image1
        im1.save(path2)

    def save_novagia_pdf(self):
        from shutil import copy
        pathinit = r'C:\Users\user\Documents\SEFAZ\GIA\TNormal'
        pathinit += f'\\{os.listdir(pathinit)[0]}'
        # copy(r"C:\Users\User\Documents\SEFAZ\GIA\TNormal\{}".format(os.listdir(r"C:\Users\User\Documents\SEFAZ\GIA\TNormal")[0]), r"C:\Users\user\OneDrive\_FISCAL-2021\2021\01-2021\GIA_Tharles Marli")
        copy(pathinit, self.client_path)

    def pt1_gia_software(self, ie, cpt_write):
        cpt_write = "".join(cpt_write.split('-'))
        print(cpt_write
              )
        menuX, menuY = 20, 27
        [pygui.click(menuX, menuY, duration=2.5) for i in range(1)]
        sleep(2)
        pygui.hotkey('tab', 'enter', interval=.25)
        pygui.hotkey('tab', 'tab')
        pygui.write(ie, interval=.1)
        foritab(2, 'tab', 'enter')
        pygui.hotkey('tab', 'tab', 'enter')
        sleep(.2)
        pygui.write(cpt_write)
        sleep(.5)
        pygui.hotkey('tab', 'enter')
        sleep(.2)
        pygui.hotkey('left', 'enter', 'enter', 'tab', 'enter', interval=.25)

    def clieninput_filepath(self, filetype='sfz'):

        dir_searched_now = self.client_path
        file = [os.path.join(dir_searched_now, fname) for fname in os.listdir(
            dir_searched_now) if fname.lower().endswith(filetype)]

        return file[0] if len(file) == 1 else False

    def exec_list(self, **args):
        """
        :param args: somente dicionarios
        :return:
        """
        from time import sleep
        import pyautogui as pygui
        from concurrent.futures import ThreadPoolExecutor
        executors_list = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            for key, vs in args.items():
                if key == 'click':
                    executors_list.append(executor.submit(vs.click))
                else:
                    executors_list.append(
                        executor.submit(pygui.hotkey, str(key)))
                    print('else')
                sleep(2)
                print('sleeping')

    def abre_programa(self, name, path=False):
        """
        :param name: path/to/nameProgram
        :param path: False => contmatic, True => any path
        :return: winleft+r open
        """
        if path is False:
            programa = contmatic_select_by_name(name)
        else:
            programa = name

        senha = '240588140217'
        sleep(1)
        pygui.hotkey('winleft', 'r')
        # pesquisador
        sleep(1)
        pygui.write(programa)
        sleep(1)
        pygui.hotkey('enter')

        sleep(10)

        # p.write(senha)
        # p.hotkey('tab', 'enter', interval=.5)

        pygui.sleep(5)
        # pygui.click(x=1508, y=195) # fecha a janela inicial no G5

    def get_env_for_path(self, path='\\Desktop\\GIA.exe'):

        p1path = os.getenv('APPDATA')
        p1path = os.path.abspath(os.path.join(os.path.dirname(p1path), '..'))
        p1path += path
        return p1path

        # CONTMATIC_PATH = p1path + r'\Microsoft\Windows\Start Menu\Programs\Contmatic Phoenix'

    # def gerar_cert(self, arq):
    #     import os
    #     save = os.path.join(self.client_path, arq)
    #     self.driver.save_screenshot(save)

    def certifs_exist(self, startswith, at_least=2):
        arqs_search = self.files_get_anexos_v4(self.client_path, 'png')
        arqs_search = [
            self.path_leaf(f, True) for f in arqs_search]
        arqs_search = [f for f in arqs_search if f.startswith(startswith)]

        if len(arqs_search) >= at_least:
            return True
        return False
