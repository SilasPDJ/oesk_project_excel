# dale
from default.sets import InitialSetting
from default.webdriver_utilities.pre_drivers import pgdas_driver
from default.webdriver_utilities.wbs import WDShorcuts
from default.interact import *
from default.interact import _contmatic_select_by_name

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

    def __init__(self, *args, compt, first_compt=None):

        __r_social, __ecac, login, senha = args

        # __anexo,  __valor_n_ret, __valor_ret, already_declared

        # competencia declarada
        # loop_compt = compt

        self.client_path = self.files_pathit(
            __r_social.strip(), compt)
        # self.client_path = self.pathit(self.compt, main_path, __r_social)

        # drivers declarados
        # menuX, menuY = 20, 27
        self.menuX, self.menuY = 26, 31

        def fecha_janela_contribuintes_gia():
            sleep(1)
            pygui.click(1322, 333, duration=.5)
            pygui.hotkey('left', 'enter')
        # self.GIA()

        # if certificado...
        if len(self.files_get_anexos_v4(self.client_path, 'sfz')) < 1:
            for loop_compt in self.ate_atual_compt(first_compt, compt):
                janelas_gias = pygui.getWindowsWithTitle('GIA')
                for win in janelas_gias:
                    if win.title == 'GIA':
                        win.maximize()
                        win.activate()
                        break
                else:
                    # there is no break...
                    self.abre_programa(self.get_env_for_path(
                        '\\Desktop\\GIA.exe'), path=True)

                IE = __ecac
                my_print = login
                print(my_print)
                # pygui.hotkey('alt', 'tab')
                print(IE)
                #

                try:
                    fecha_janela_contribuintes_gia()
                except IndexError:
                    print('Não precisei fechar')
                self.pt1_gia_software(IE, loop_compt)

                pygui.doubleClick(self.menuX+35, self.menuY)
                # consistir
                sleep(3)
                pygui.click(self.menuX, self.menuY)
                sleep(.5)
                foritab(2, 'up')
                pygui.hotkey('enter')
                pygui.click(x=836, y=394)
                foritab(7, 'tab')
                pygui.hotkey('enter', 'enter', interval=.25)
                pygui.hotkey('enter')
                self.save_novagia()

        if not self.certifs_exist('ReciboGIA', 1):
            for loop_compt in self.ate_atual_compt(first_compt, compt):
                self.driver = driver = pgdas_driver(self.client_path)
                super().__init__(self.driver)
                driver.get(
                    'https://www3.fazenda.sp.gov.br/CAWEB/Account/Login.aspx')
                llg = driver.find_element(By.ID,
                                          'ConteudoPagina_txtUsuario')
                llg.clear()
                llg.send_keys(login)

                ssn = driver.find_element(By.XPATH,
                                          "//input[@type='password']")
                ssn.clear()
                ssn.send_keys(senha)

                self.send_keys_anywhere(Keys.TAB)
                self.send_keys_anywhere(Keys.ENTER)
                print('pressione f7 p/ continuar após captcha')
                press_key_b4('f8')
                # self.find_submit_form()
                # enter entrar
                sleep(3)
                self.webdriverwait_el_by(
                    By.LINK_TEXT, 'Guia de Informação (Arts. 253-254 RICMS/00)').click()
                self.webdriverwait_el_by(By.LINK_TEXT, 'Envio de GIA').click()
                # self.webdriverwait_el_by(By.PARTIAL_LINK_TEXT,
                #                          'Documentos Fiscais (Normal, Substit.e Coligida)').click()
                sleep(3)
                driver_clicks = driver.find_elements(By.XPATH,
                                                     "//input[@type='file']")

                driver_clicks[0].send_keys(self.clieninput_filepath())
                driver.find_elements(By.XPATH,
                                     "//input[@type='button']")[0].click()
                try:
                    driver.switch_to.alert.accept()
                except NoAlertPresentException:
                    print('Sem alerta')
                sleep(5)
                """
                    bt_imprime = driver.find_element(By.CSS_SELECTOR, '[alt="Imprimir"]')
                    self.exec_list(click=bt_imprime, enter=pygui)
                    print('Glória a Deus f7 p continuar')
                    press_key_b4('f7')
                    """
                png_name = 'GiaScreenShoot.png'
                self.driver.save_screenshot(
                    os.path.join(self.client_path, png_name))
                # convert_img2pdf is only joining both or NOT joining both...
                self.convert_img2pdf(
                    png_name,
                    f'ReciboGIA_{loop_compt}.pdf', self.client_path)
                driver.close()
                sleep(5)
                # pygui.hotkey('enter')
                # ############################################ parei daqui

    def save_novagia(self):
        from shutil import copy
        pathinit = os.path.join(
            self.get_documents_folder_location(), 'SEFAZ/GIA/TNORMAL')
        pathinit = self.sort_files_by_most_recent(pathinit)[0]
        # copy(r"C:\Users\User\Documents\SEFAZ\GIA\TNormal\{}".format(os.listdir(r"C:\Users\User\Documents\SEFAZ\GIA\TNormal")[0]), r"C:\Users\user\OneDrive\_FISCAL-2021\2021\01-2021\GIA_Tharles Marli")
        copy(pathinit, self.client_path)

    def pt1_gia_software(self, ie, cpt_write):
        cpt_write = "".join(cpt_write.split('-'))
        print(cpt_write
              )
        [pygui.click(self.menuX, self.menuY, duration=2.5) for i in range(1)]
        sleep(2)
        pygui.hotkey('tab', 'enter', interval=.25)
        sleep(.5)
        foritab(2, 'tab')
        pygui.write(ie, interval=.1)
        foritab(2, 'tab', 'enter')
        # pygui.hotkey('tab', 'tab', 'enter')
        foritab(2, 'tab')
        pygui.hotkey('enter')
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
            programa = _contmatic_select_by_name(name)
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
