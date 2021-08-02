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
from default.webdriver_utilities.pre_drivers import ginfess_driver
from openpyxl import Workbook


class DownloadGinfessGui(InitialSetting, WDShorcuts):

    # only static methods from JsonDateWithDataImprove

    def __init__(self, fname, compt_file=None,):
        from time import sleep
        if compt_file is None:
            # compt, excel_file_name = self.set_get_compt_file(1)
            compt_file = self.set_get_compt_file(1)
        print('teste ginfess')
        json_file = self.load_json(fname)
        # input(len(after_READ['CNPJ']))
        print('-='*30)
        print(f'{"Ginfess Download":^30}')
        # print(json_file)
        print('-='*30)
        for eid in json_file.keys():
            print('~'*30)
            print(eid)
            print('~' * 30)
            # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'*10)
            # print(list_with_dict)
            list_with_dic = json_file[eid]

            values = [v.values() for v in list_with_dic[:]]
            # padrão
            __r_social, __cnpj, __cpf, __cod_simples, __ja_declared = 1,2,3,4,5,6
            
            _ginfess_cod = ''.join(values[-6])
            
            _city = ''.join(values[-4])
            print(_ginfess_cod, _city)
            # mesma coisa de self.any_to_str, só que ele aceita args desempacotados
            self.client_path = self.files_pathit(__r_social.strip(), self.compt)

            # Checa se já existe certificado
            if _ginfess_cod.lower() == 'não há':
                # removi o ja_imported
                print(f'\033[1;31m o cliente {__r_social} não possui notas\n...(muito bom) O certificado anula o _ja_imported...\033[m')
            elif self.check_done(self.client_path, '.png', startswith='GINFESS'):
                # Checka o certificado ginfess, somente

                # if city in 'ABC':
                self.driver = ginfess_driver(self.client_path)
                super().__init__(self.driver)
                driver = self.driver
                driver.maximize_window()

                cities = "Trem", "A", "B", "C", "SP"
                urls = \
               'https://santoandre.ginfes.com.br/', 'https://nfse.isssbc.com.br/', 'https://saocaetano.ginfes.com.br/', \
               'https://nfe.prefeitura.sp.gov.br/login.aspx'
                try:
                    self.driver.get(id_url)
                except InvalidArgumentException:
                    if int(eid)-1 == len(json_file.keys()):
                        print('FIM')
                        break
                #for
                if _city in ['A', 'B', 'C']:
                    # links das cidades

                    # driver.maximize_window()
                    # #######################################################
                    self.ABC_ginfess(__cnpj, _ginfess_cod, _city)

                    # #######################################################

                    try:
                        # Find existent tags
                        driver.implicitly_wait(5)
                        self.tags_wait('table', 'tbody', 'tr', 'td')

                        print('printscreen aqui')

                        self.download(_city)
                        driver.implicitly_wait(5)
                        self.cexcel_from_html_above_v1(__r_social, self.ginfess_table_valores_html_code())

                    except IndexError:
                        print('~' * 30)
                        print('não emitiu nenhuma nota'.upper())
                        print('~' * 30)

                    driver.save_screenshot(self.certif_feito(self.client_path, add='GINFESS'))
                    # coloquei tudo no dele

                elif _city.upper() == 'TREM':
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
                    compt = self.compt_and_filename()[0]
                    mes, ano = compt.split('-')

                    driver.find_element_by_name('ano').clear()
                    driver.find_element_by_name('ano').send_keys(ano)
                    mes = self.nome_mes(int(mes))

                    driver.find_element_by_xpath(f"//select[@name='mes']/option[text()='{mes}']").click()
                    # driver.find_element_by_name('ano').send_keys(ano)

                    driver.implicitly_wait(5)
                    driver.find_element_by_id('btnOk').click()

                    driver.implicitly_wait(10)

                    # iframe = driver.find_element_by_id('iframe')
                    # driver.switch_to_frame(iframe)

                    self.tag_with_text('td', 'Encerramento').click()
                    # driver.switch_to_alert().accept()

                    # driver.get('../fechamento/prestado.php')
                    driver.find_element_by_xpath('//a[contains(@href,"../fechamento/prestado.php")]').click()
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
                        driver.execute_script("abre_arquivo('dmm/_menuPeriodo.php');")
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
                    self.download(_city)

                    path_zip = client_path
                    print(f'path_zip-> {path_zip}')
                    self.unzipe_file(path_zip)

                    driver.switch_to_default_content()
                    driver.save_screenshot(self.certif_feito(self.client_path, add='GINFESS'))

                [(print(f'Sleeping before close {i}'), sleep(1)) for i in range(5, -1, -1)]

                driver.close()

    def wait_main_tags(self):
        self.tags_wait('body', 'div', 'table')

    def ABC_ginfess(self, __cnpj, __senha, city):

        driver = self.driver

        def label_with_text(searched):
            label = driver.find_element_by_xpath(f"//label[contains(text(),'{searched.rstrip()}')]")
            return label

        def button_with_text(searched):
            bt = driver.find_element_by_xpath(f"//button[contains(text(),'{searched.rstrip()}')]")
            return bt

        def a_with_text(searched):
            link_tag = driver.find_element_by_xpath(f"//a[contains(text(),'{searched.rstrip()}')]")
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

    def download(self, city):
        """
        :city:
        :return:
        """
        driver = self.driver

        if city.strip().lower() not in ('trem', 'sp'):
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
                    downloada_xml = driver.find_element_by_xpath('//img[@src="imgs/download.png"]')
                    try:
                        downloada_xml.click()
                    except ElementClickInterceptedException:
                        self.click_ac_elementors(downloada_xml)
                    # self.click_ac_elementors(downloada_xml)

            except NoSuchElementException:
                print('NÃO CONSEGUI FAZER DOWNLOAD...')
        else:
            if driver.current_url.lower() in 'sigiss':
                pass

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

        xml_pages = driver.find_element_by_xpath('//input[@class="x-tbar-page-number"]')
        driver.implicitly_wait(5)
        number_in_pages = xml_pages.get_attribute('value')

        html_cod = """           
                    <style>/*.detalheNota:after{background: red; content: 'cancelada';}*/
                    .notaCancelada{
                    background: red
                    }
                    </style>
                   """.strip()
        pasta_a_salvar = 'G5'

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

            wanted_wanted = driver.find_elements_by_xpath("//div[contains(@class, 'x-grid3-row')]")
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

    def cexcel_from_html_above_v1(self, cliente, html_codigo):
        # # DEPOIS JUNTAR ELA COM GINFESS_SCRAP
        import os
        import pyautogui as pygui
        from pyperclip import paste, copy
        from time import sleep
        from .retornot import RetidosNorRetidos, RnrSo1
        from .ginfess_scrap import cria_site_v1

        """
         :param cliente: nome do cliente vindo do loop
         :param competencia: vindo do GINFESS_download na linha 37
         :param site_cria: (lugar_salvar)
         :return: return_full_path for with_titlePATH.txt
         """
        client_path = self.client_path
        # impossível ser None
        driver = self.driver

        qtd_nf = driver.find_element_by_class_name('x-paging-info')
        qtd_text = qtd_nf.text
        proc = qtd_text.index('of')
        pal = qtd_text[proc:].split()
        qtd_text = pal[1]
        prossigo = cria_site_v1(html_codigo, qtd_text)
        _prossigo = prossigo[0]
        len_tables = prossigo[1]
        # input(f'{prossigo}, {len_tables}, {_prossigo}')
        sleep(5)
        if _prossigo:
            arq = f'rnc-{cliente}.xlsx'
            if len(arq) > 32:
                arq = f'rnc-{cliente.split()[0]}.xlsx'
            x, y = pygui.position()
            arq = f'{client_path}/{arq}' if '/' in client_path else f'{client_path}\\{arq}'
            # not really necessary, but i want to
            try:
                wb = Workbook()
                sh_name = client_path.split('/')[-1] if '\\' not in client_path else client_path.split('\\')[-1]
                sh_name = sh_name[:10]
                # limitando
                wb.create_sheet(sh_name)
                wb.active = 1
                wb.remove(wb['Sheet'])
                wb.save(arq)
            except FileExistsError:
                pass

            finally:
                # ########## ABRINDO EXCEL ####### #
                program = arq.split('_')[-1]
                """~~~~"""
                os.startfile(arq)
                """~~~~"""
                sleep(12)

                allin = pygui.getAllWindows()
                for e, l in enumerate(allin):
                    if program in l.title.lower():
                        l.restore()
                        l.activate()
                        l.maximize()

                # ########## ABRINDO #########
                sleep(6)
                if len_tables > 1:
                    RetidosNorRetidos()
                # input('RETIDOS N RETIDOS')
                    pygui.hotkey('alt', 'f4')
                    sleep(5)
                    pygui.hotkey('enter')
                # from RETIDOS_N_RETIDOS import save_after_changes
                else:
                    RnrSo1()
                    print(f'Testado, len tables = {len_tables}')

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
