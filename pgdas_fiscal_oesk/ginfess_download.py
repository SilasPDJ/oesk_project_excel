# dale
import openpyxl
from default.sets import InitialSetting
from default.webdriver_utilities.wbs import WDShorcuts
from default.interact import press_keys_b4, press_key_b4
from selenium.webdriver import Chrome

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
from default.webdriver_utilities.pre_drivers import ginfess_driver
from openpyxl import Workbook
from openpyxl.utils.cell import coordinate_from_string
from openpyxl.utils import get_column_letter as gcl
import pandas as pd
import os


class DownloadGinfessGui(InitialSetting, WDShorcuts):

    # only static methods from JsonDateWithDataImprove

    def __init__(self, *dados, driver, compt):
        __r_social, __cnpj, _ginfess_cod, link = dados
        _ginfess_cod = str(_ginfess_cod)

        self.compt = compt
        # mesma coisa de self.any_to_str, só que ele aceita args desempacotados
        self.client_path = self.files_pathit(__r_social.strip(), self.compt)

        # Checa se já existe certificado
        if _ginfess_cod.lower() == 'não há':
            # removi o ja_imported
            print(
                f'\033[1;31m o cliente {__r_social} não possui notas\n...(muito bom) O certificado anula o _ja_imported...\033[m')
        elif self.check_done(self.client_path, '.png', startswith='GINFESS'):
            # Checka o certificado ginfess, somente

            # if city in 'ABC':
            self.driver = driver(self.client_path)
            super().__init__(self.driver)
            driver = self.driver
            driver.maximize_window()

            self.driver.get(link)
            # for
            if self.driver.title == 'NFS-e':
                # links das cidades

                # driver.maximize_window()
                # #######################################################
                self.ABC_ginfess(__cnpj, _ginfess_cod)
                # #######################################################

                try:
                    # Find existent tags
                    driver.implicitly_wait(5)
                    self.tags_wait('table', 'tbody', 'tr', 'td')

                    print('printscreen aqui')

                    self.download()

                    driver.implicitly_wait(5)

                    # Creation initial
                    excel_file = os.path.join(
                        self.client_path, f'{__cnpj}.xlsx')
                    # Aqui
                    self.excel_from_html_above(
                        excel_file, html=self.ginfess_table_valores_html_code())

                except IndexError:
                    print('~' * 30)
                    print('não emitiu nenhuma nota'.upper())
                    print('~' * 30)

                driver.save_screenshot(self.certif_feito(
                    self.client_path, add='GINFESS'))
                # coloquei tudo no dele

            elif self.driver.current_url == 'https://tremembe.sigiss.com.br/tremembe/contribuinte/login.php':
                driver.implicitly_wait(5)

                zero_um = _ginfess_cod.split('//')
                # ginfess login//senha
                self.tags_wait('html')
                self.tags_wait('body')
                while True:
                    driver.implicitly_wait(5)

                    ccm = driver.find_element_by_id('ccm')
                    senha = driver.find_element_by_id('senha')
                    confirma = driver.find_element_by_id('confirma')
                    ccm.send_keys(zero_um[0])

                    for el in ccm, senha, confirma:
                        el.clear()
                    ccm.send_keys(zero_um[0])
                    senha.send_keys(zero_um[1])
                    trem_cod = self.captcha_hacking()
                    confirma.send_keys(trem_cod)
                    # driver.find_element_by_id('btnOk').click()
                    if 'login.php' in driver.current_url:
                        driver.refresh()
                        driver.implicitly_wait(6)
                    else:
                        break

                print('break')
                driver.implicitly_wait(10)
                driver.execute_script("""function abre_arquivo(onde){
                var iframe = document.getElementById("main");
                iframe.src = onde;
                }
                """)

                driver.execute_script("abre_arquivo('dmm/_menuPeriodo.php');")

                driver.implicitly_wait(5)

                # self.tag_with_text('td', 'Movimento ').click()

                sleep(5)

                iframe = driver.find_element_by_id('main')
                driver.switch_to_frame(iframe)
                driver.find_element_by_name('btnAlterar').click()
                driver.implicitly_wait(5)

                # handelling select
                compt = self.compt
                mes, ano = compt.split('-')

                driver.find_element_by_name('ano').clear()
                driver.find_element_by_name('ano').send_keys(ano)
                mes = self.nome_mes(int(mes))

                driver.find_element_by_xpath(
                    f"//select[@name='mes']/option[text()='{mes}']").click()
                # driver.find_element_by_name('ano').send_keys(ano)

                driver.implicitly_wait(5)
                driver.find_element_by_id('btnOk').click()

                driver.implicitly_wait(10)

                # iframe = driver.find_element_by_id('iframe')
                # driver.switch_to_frame(iframe)

                self.tag_with_text('td', 'Encerramento').click()
                # driver.switch_to_alert().accept()

                # driver.get('../fechamento/prestado.php')
                driver.find_element_by_xpath(
                    '//a[contains(@href,"../fechamento/prestado.php")]').click()
                driver.implicitly_wait(10)
                try:
                    driver.find_element_by_id('btnSalvar').click()
                    driver.implicitly_wait(5)
                    driver.switch_to_alert().accept()
                    driver.implicitly_wait(5)
                    # driver.back()
                except (NoSuchElementException, NoAlertPresentException):
                    print('Já encerrado')
                finally:
                    driver.implicitly_wait(5)
                    driver.back()
                    driver.back()
                    driver.execute_script("""function abre_arquivo(onde){
                    var iframe = document.getElementById("main");
                    iframe.src = onde;
                    }
                    """)
                    driver.execute_script(
                        "abre_arquivo('dmm/_menuPeriodo.php');")
                    iframe = driver.find_element_by_id('main')
                    driver.switch_to_frame(iframe)
                    driver.find_element_by_name('btnAlterar').click()
                    driver.find_element_by_name('btnOk').click()

                    # ############### validar driver.back()

                url = '/'.join(driver.current_url.split('/')[:-1])
                driver.get(f'{url}/nfe/nfe_historico_exportacao.php')
                driver.implicitly_wait(3)
                self.tags_wait('html')
                self.tags_wait('body')

                driver.implicitly_wait(2)
                driver.find_element_by_id('todos').click()
                driver.find_element_by_id('btnExportar').click()
                driver.switch_to.alert.accept()

                path_zip = self.client_path
                print(f'path_zip-> {path_zip}')
                self.unzip_folder(path_zip)

                driver.switch_to_default_content()
                driver.save_screenshot(self.certif_feito(
                    self.client_path, add='GINFESS'))

            elif self.driver.current_url == 'https://app.siappa.com.br/issqn_itupeva/servlet/com.issqnwebev3v2.login':
                self.driver.find_element_by_id('vUSR_COD').send_keys(__cnpj)
                self.driver.find_element_by_css_selector(
                    '[type="password"]').send_keys(_ginfess_cod)
                # d = Chrome().
                press_keys_b4('f9')
                driver.save_screenshot(self.certif_feito(
                    self.client_path, add='GINFESS'))
            elif self.driver.current_url == 'https://bragancapaulista.giap.com.br/apex/pmbp/f?p=994:101':
                a = __login, __senha = _ginfess_cod.split('//')
                self.driver.find_element_by_id(
                    'P101_USERNAME').send_keys(__login)
                self.driver.find_element_by_css_selector(
                    '[type="password"]').send_keys(str(__senha))
                self.click_ac_elementors(self.tag_with_text('span', 'ENTRAR'))

                # CONSULTAR
                self.driver.implicitly_wait(30)
                self.driver.execute_script(
                    "javascript:apex.submit('EMISSAO NOTA');")
                mes, ano = self.compt.split('-')
                mes = self.nome_mes(int(mes))
                self.driver.find_element_by_xpath(
                    f"//select[@name='P26_MES']/option[text()='{mes}']").click()
                self.driver.find_element_by_xpath(
                    f"//select[@name='P26_ANO']/option[text()='{ano}']").click()
                # CONSULTAR
                self.driver.execute_script(
                    "apex.submit({request:'P26_BTN_CONSULTAR'});")

                self.driver.save_screenshot(self.certif_feito(
                    self.client_path, add='GINFESS'))
            else:

                self.send_keys_anywhere(__cnpj)
                self.send_keys_anywhere(Keys.TAB)
                self.send_keys_anywhere(_ginfess_cod)
                self.send_keys_anywhere(Keys.TAB)

                press_keys_b4('f9')
                driver.save_screenshot(self.certif_feito(
                    self.client_path, add='GINFESS'))
            [(print(f'Sleeping before close {i}'), sleep(1))
             for i in range(5, -1, -1)]

            driver.close()

    def wait_main_tags(self):
        self.tags_wait('body', 'div', 'table')

    def ABC_ginfess(self, __cnpj, __senha):

        driver = self.driver

        def label_with_text(searched):
            label = driver.find_element_by_xpath(
                f"//label[contains(text(),'{searched.rstrip()}')]")
            return label

        def button_with_text(searched):
            bt = driver.find_element_by_xpath(
                f"//button[contains(text(),'{searched.rstrip()}')]")
            return bt

        def a_with_text(searched):
            link_tag = driver.find_element_by_xpath(
                f"//a[contains(text(),'{searched.rstrip()}')]")
            return link_tag

        self.wait_main_tags()
        """ ~~~~~~~~~~~~~~~~~~~~~~ GLÓRIA A DEUS ~~~~~~~~~~~~~~~~~~"""
        name_c = 'gwt-DialogBox'

        self.del_dialog_box(name_c)

        self.wait_main_tags()
        self.tags_wait('img')
        driver.implicitly_wait(10)

        try:
            try:
                button_with_text('OK').click()
            except (NoSuchElementException, ElementClickInterceptedException):
                pass
            driver.find_element_by_xpath('//img[@src="imgs/001.gif"]').click()
        except (NoSuchElementException, ElementClickInterceptedException):
            pass
        name_c = 'x-window-dlg', 'ext-el-mask', 'x-shadow'

        try:
            for name in name_c:
                try:
                    self.del_dialog_box(name)
                except NoSuchElementException:
                    print('Except dentro do except e no for, [linha 310]')
                    ...
                driver.implicitly_wait(5)
            button_with_text('OK').click()
        except (NoSuchElementException, ElementClickInterceptedException):
            print('Sem janela possivel, linha 246')
            # driver.execute_script('window.alert("Não foi possível prosseguir")')

        driver.implicitly_wait(5)
        """ ~~~~~~~~~~~~~~~~~~~~~~ GLÓRIA A DEUS ~~~~~~~~~~~~~~~~~~"""

        # print('mandando teclas...')
        label_with_text("CNPJ:").click()
        self.send_keys_anywhere(__cnpj)
        passwd = driver.find_element_by_xpath("//input[@type='password']")

        self.tags_wait('body', 'img')
        passwd.clear()
        passwd.send_keys(__senha)
        button_with_text("Entrar").click()

        # tratando atualiza dados
        driver.implicitly_wait(15)
        try:
            self.wait_main_tags()
            button_with_text('X').click()
            button_with_text('X').click()
            print('CLICADO, X. Linha 263')
        except (NoSuchElementException, ElementClickInterceptedException):
            print('Tentando atualizar os dados')

        a_with_text("Consultar").click()

        print('Waiting main_excel_manager tags')
        self.wait_main_tags()

        period = label_with_text('Período')
        period.click()
        driver.implicitly_wait(5)
        de = label_with_text('De:')
        de.click()
        self.send_keys_anywhere(Keys.BACKSPACE, 10)
        write = '01/09'
        first, last = self.first_and_last_day_compt()
        self.send_keys_anywhere(first)
        driver.implicitly_wait(2.5)
        self.send_keys_anywhere(Keys.TAB)

        self.send_keys_anywhere(last)
        driver.implicitly_wait(5)
        button_with_text("Consultar").click()
        self.wait_main_tags()
        driver.implicitly_wait(10)

    def download(self):
        """
        :city: A, B, C only
        :return:
        """
        driver = self.driver
        try:
            try:
                # self.del_dialog_box('x-shadow')
                xsh = driver.find_element_by_class_name('x-shadow')
                if 'block' in xsh.get_attribute('style'):
                    self.del_dialog_box('x-shadow')
                    driver.implicitly_wait(10)
                    print('W-SHADOW-DELETADO')
                else:
                    raise NoSuchElementException

            except NoSuchElementException:
                print('Tem notas')
                driver.implicitly_wait(10)
                downloada_xml = driver.find_element_by_xpath(
                    '//img[@src="imgs/download.png"]')
                try:
                    downloada_xml.click()
                except ElementClickInterceptedException:
                    self.click_ac_elementors(downloada_xml)

                except ElementNotInteractableException:
                    pass
                # self.click_ac_elementors(downloada_xml)

        except NoSuchElementException:
            print('NÃO CONSEGUI FAZER DOWNLOAD...')

    def ginfess_table_valores_html_code(self):
        """
        :return: (html_cod): código dele se existe a class ytb-text, scrap_it
        """
        driver = self.driver

        max_value_needed = driver.find_elements_by_class_name('ytb-text')
        max_value_needed = max_value_needed[1].text[-1]
        print(max_value_needed)
        self.tags_wait('input', 'body')

        cont_export = 1

        xml_pages = driver.find_element_by_xpath(
            '//input[@class="x-tbar-page-number"]')
        driver.implicitly_wait(5)
        number_in_pages = xml_pages.get_attribute('value')

        html_cod = """           
                    <style>/*.detalheNota:after{background: red; content: 'cancelada';}*/
                    .notaCancelada{
                    background: red
                    }
                    </style>
                   """.strip()

        for i in range(10):
            print(number_in_pages)
            xml_pages.send_keys(Keys.BACKSPACE)
            xml_pages.send_keys(cont_export)

            xml_pages.send_keys(Keys.ENTER)
            driver.implicitly_wait(5)
            print('CALMA...')
            cont_export += 1
            number_in_pages = xml_pages.get_attribute('value')

            # // div[ @ id = 'a'] // a[ @class ='click']

            wanted_wanted = driver.find_elements_by_xpath(
                "//div[contains(@class, 'x-grid3-row')]")
            print(wanted_wanted[0].text)
            # table = wanted_wanted

            for w in wanted_wanted:
                # w.click()
                print(w.text)
                html_cod += w.get_attribute('innerHTML')
                # sleep(2)
            # XML_to_excel.ginfess_scrap()
            if int(cont_export) == int(max_value_needed) + 1:
                break
            print('breakou')

            print('~~~~~~~~')
        return html_cod
        # de.send_keys(Keys.TAB)

    def excel_from_html_above(self, excel_file, html):
        from bs4 import BeautifulSoup
        from openpyxl.styles import PatternFill

        mylist = pd.read_html(html)

        soup = BeautifulSoup(html, 'html.parser')
        with_class = tables = [str(table) for table in soup.select('table')]
        df = pd.concat([l for l in mylist])
        header = ['Nº NF', 'Data', 'Valor', 'Imposto',
                  'CPF/CNPJ tomador']

        def to_number(ind):
            df[ind] = [d.replace('R$ ', '') for d in df[ind]]
            df[ind] = [d.replace('.', '') for d in df[ind]]
            df[ind] = [d.replace(',', '.') for d in df[ind]]
            df[ind] = pd.to_numeric(df[ind])
            return df[ind]
        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            df[2] = to_number(2)
            df[3] = to_number(3)
            # df.style =
            # create new formats
            book = writer.book
            contabil_format = book.add_format({'num_format': 44})

            add_soma = f'C{len(df[2])+1}'
            add_soma = df[2].sum()
            # df.loc[2] = add_soma

            # input(add_soma)

            while True:
                try:
                    wb = df.to_excel(writer, sheet_name='Sheet1',
                                     header=header, index=False)
                    break
                except ValueError:
                    header.append('-')

            worksheet = writer.sheets['Sheet1']

            worksheet.set_column('C:C', None, contabil_format)
            worksheet.set_column('D:D', None, contabil_format)

        wb = openpyxl.load_workbook(excel_file)
        wks = wb.worksheets
        ws = wb.active

        # next line = nxln
        # last value line = llv
        line = nxln = llv = len(df[2]) + 3
        llv -= 2

        # filt
        ws.auto_filter.ref = f'A1:F{llv}'

        ln_ret = line + 1
        ln_nao = line + 2

        # Total independente E DESCARTÁVEL
        ws[f'E{line}'] = f'= SUM(C2:C{llv})'

        ws[f'C{line}'] = f'= SUM(C{ln_ret}:C{ln_nao})'
        ws[f'A{line}'] = f'Valor total'

        formul_ret = f'= SUMPRODUCT(SUBTOTAL(9,OFFSET(C2,ROW(C2:C{llv})-ROW(C2),0)),(D2:D{llv}>0)+0)'
        n_retforml = f'= SUMPRODUCT(SUBTOTAL(9,OFFSET(C2,ROW(C2:C{llv})-ROW(C2),0)),(D2:D{llv}=0)+0)'

        # valores
        ws[f'C{ln_ret}'] = formul_ret
        ws[f'A{ln_ret}'] = 'RETIDO'
        ws[f'C{ln_nao}'] = n_retforml
        ws[f'A{ln_nao}'] = 'NÃO RETIDO'
        # formatacoes
        ws[f'C{ln_ret}'].number_format = ws['C2'].number_format
        ws[f'C{ln_nao}'].number_format = ws['C2'].number_format
        ws[f'C{line}'].number_format = ws['C2'].number_format
        # muda
        redFill = PatternFill(start_color='FFFF0000',
                              end_color='FFFF0000',
                              fill_type='solid')
        for table, row in zip(with_class, ws['A']):
            if 'notaCancelada' in table:
                row.fill = redFill
        # ws['A2'].fill = redFill
        wb.save(excel_file)

    def check_done(self, save_path, file_type, startswith=None):
        """
        :param save_path: lugar que checka tipo de arquivo
        :param file_type: extension
        :param startswith: same...
        :return:
        """
        from os import listdir

        for file in listdir(save_path):
            print(file)
            if file.endswith(file_type):
                if startswith is None:
                    print('CERTIFICADO EXISTENTE, NÃO PROSSEGUE')
                    return False
                elif file.startswith(startswith):
                    print('CERTIFICADO EXISTENTE, NÃO PROSSEGUE')
                    return False

        print('\033[1;35mPROSSEGUE\033[m')
        return True

    def captcha_hacking(self):
        """
        :param driver:
        :return:
        SbFConverter() -> class called

        Tremembé... rs
        """
        driver = self.driver

        class SbFConverter:
            """
            MUITO OBRIGADO, SENHOR

            # retorna copiada a imagem através do nome dela
            """

            def __init__(self, img_name, path=''):
                from pyperclip import copy
                self.convert_gray_scale(img_name)

                read = self.read(img_name)
                copy(read)

            def read(self, img_name):
                self.convert_gray_scale(img_name)

                import pytesseract
                from PIL import Image
                pytesseract.pytesseract.tesseract_cmd = r"J:\NEVER\tesseract.exe"
                r = img_name
                text = pytesseract.image_to_string(r)
                print(text)
                return text

            def convert_gray_scale(self, img_name):
                img2 = img_name
                from PIL import Image
                img = Image.open(img2).convert('LA')
                img.save(img_name)

        from pyautogui import hotkey
        from pyperclip import paste
        img = driver.find_element_by_id('div-img-captcha')
        img_name = 'hacking.png'
        img.screenshot(img_name)
        SbFConverter(img_name)

        continua = paste()
        return continua

    def first_and_last_day_compt(self, sep='/'):
        """
        ELE JÁ PEGA O ANTERIOR MAIS PROX
        :param str compt:(competencia or whatever). Defaults then call cls.get_compt_only() as default
        :param sep: separates month/year
        # É necessario o will_be pois antes dele é botado ao contrário
        # tipo: 20200430
        # ano 2020, mes 04, dia 30... (exemplo)
        :return: ÚLTIMO DIA DO MES
        """
        from datetime import date, timedelta
        from dateutil.relativedelta import relativedelta

        compt = self.compt
        ill_split = ''.join([v for v in compt if v not in '0123456789'])
        mes, ano = compt.split(ill_split)
        mes, ano = int(mes), int(ano)
        #  - timedelta(days=1)
        # + relativedelta(months=1)

        last_now = date(ano, mes, 1) + relativedelta(months=1)
        last_now -= timedelta(days=1)
        first_now = date(ano, mes, 1)

        z, a = last_now, first_now
        br1st = f'{a.day:02d}{sep}{a.month:02d}{sep}{a.year}'
        brlast = f'{z.day:02d}{sep}{z.month:02d}{sep}{z.year}'
        print(br1st, brlast)
        return br1st, brlast
