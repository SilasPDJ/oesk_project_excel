from random import randint
from default.sets import InitialSetting
from default.webdriver_utilities.wbs import WDShorcuts
from default.interact import press_keys_b4, press_key_b4
# from default.webdriver_utilities.pre_drivers import pgdas_driver, pgdas_driver_ua

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver import Remote

from time import sleep
# from default.sets.pathmanager import HasJson

# from . import *
# qualquer coisa me devolve


class SimplesNacionalUtilities(InitialSetting, WDShorcuts):

    def __init__(self, driver: Remote, compt, client_path):
        # super().__init__(driver)

        WDShorcuts.__init__(self, driver)
        self.driver = driver
        self.__set_driver()
        self._uclient_path = client_path

    def simples_and_ecac_utilities(self, option, compt):
        """
        :param int option: somente de 1 a 2, sendo
        :param str compt: competência
        1 -> Gerar Das somente se for consolidar para outra DATA
        2 -> Gerar Protocolos
        :return:
        """
        # estou na "declaração", aqui faço o que quiser
        from datetime import datetime
        now_year = str(datetime.now().year)
        compt = ''.join(v for v in compt if v.isdigit())
        # month_compt = compt[:2]
        year_compt = compt[2:]

        driver = self.driver
        current_url = self.current_url
        link_gera_das, download_protocolos_das = self.link_gera_das, self.download_protocolos_das

        if option == 2:

            self.get_sub_site(download_protocolos_das, current_url)
            driver.implicitly_wait(5)

            if now_year != year_compt:
                self.send_keys_anywhere(year_compt)
                self.find_submit_form()
                sleep(3.5)
            try:
                comp_clic = driver.find_elements(By.CLASS_NAME, 'pa')
                lenc = len(comp_clic) - 1
                comp_clic[lenc].click()
            except IndexError:
                pass
            for i in range(3):
                sleep(2)
                self.send_keys_anywhere(Keys.TAB)
                self.send_keys_anywhere(Keys.ENTER)

        elif option == 1:
            # gera das
            data_vencimento = datetime.now()
            venc_month_compt = data_vencimento.month
            venc = self.get_last_business_day_of_month(
                venc_month_compt, data_vencimento.year)
            retifica_p_dia = f'{venc.day:02d}{venc.month:02d}{venc.year}'
            self.get_sub_site(link_gera_das, current_url)
            self.tags_wait('input')
            driver.implicitly_wait(10)
            periodo = driver.find_element(By.ID, 'pa')
            periodo.send_keys(compt)
            self.find_submit_form()
            sleep(2.5)
            # if  len(driver.find_elements(By.ID, 'msgBox')) == 0 # CASO NÃO EXISTA O DAS
            consolida = driver.find_element(By.ID, 'btnConsolidarOutraData')
            consolida.click()
            sleep(2.5)

            validade_id = 'txtDataValidade'
            driver.execute_script(
                f"document.getElementById('{validade_id}').focus();")
            validade_change = driver.find_element(By.ID, validade_id)
            validade_change.send_keys(retifica_p_dia)
            sleep(1)
            driver.find_element(By.ID, 'btnDataValidade').click()
            # coloquei a validade
            # gerei das

            driver.implicitly_wait(5)
            self.find_submit_form()
            sleep(5)
            # GERAR DAS
        else:
            return False

    def opta_script(self, ultrarior=True):
        driver = self.driver
        try:
            # #################################################### opta
            self.get_sub_site('/RegimeApuracao/Optar', self.current_url)
            # driver.execute_script("""window.location.href += '/RegimeApuracao/Optar'""")

            from selenium.webdriver.support.ui import Select
            anocalendario = Select(driver.find_element(By.ID, 'anocalendario'))

            if ultrarior:
                anocalendario.select_by_value(f'{self.y()+1}')
            else:
                anocalendario.select_by_value(f'{self.y()}')
            self.find_submit_form()

            # competencia
            competencia, caixa = '0', '1'

            driver.find_element(By.CSS_SELECTOR,
                                f"input[type='radio'][value='{competencia}']").click()
            self.find_submit_form()
            sleep(2.5)
            # driver.find_element(By.ID, 'btnSimConfirm').click()

            try:
                driver.implicitly_wait(10)
                self.click_ac_elementors(
                    driver.find_element(By.CLASS_NAME, 'glyphicon-save'))
            except NoSuchElementException:
                input('input Não consegui')
            else:
                print('Não fui exceptado')
            # ########################################################
        except NoSuchElementException:
            pass
        finally:
            driver.get(self.current_url)
            driver.execute_script(
                """window.location.href += '/declaracao?clear=1'""")
            sleep(2.5)

    def loga_simples(self, CNPJ, CPF, CodSim, CLIENTE):
        driver = self.driver
        driver.get(
            'https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')

        driver.get(
            'https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')
        while str(driver.current_url.strip()).endswith('id=60'):
            CAPT = self.__loga_simples_capt()
            self.tags_wait('body')
            self.tags_wait('html')
            self.tags_wait('input')

            # driver.find_elements(By.XPATH, "//*[contains(text(), 'CNPJ:')]")[0].click()
            # pygui.hotkey('tab', interval=0.5)
            cpcp = driver.find_element(By.NAME,
                                       'ctl00$ContentPlaceHolder$txtCNPJ')
            cpcp.clear()
            cpcp.send_keys(CNPJ)

            cpfcpf = driver.find_element(By.NAME,
                                         'ctl00$ContentPlaceHolder$txtCPFResponsavel')
            cpfcpf.clear()
            cpfcpf.send_keys(CPF)

            cod = driver.find_element(By.NAME,
                                      'ctl00$ContentPlaceHolder$txtCodigoAcesso')
            cod.clear()
            cod.send_keys(CodSim)

            cod_caract = driver.find_element(By.ID,
                                             'txtTexto_captcha_serpro_gov_br')
            btn_som = driver.find_element(By.ID,
                                          'btnTocarSom_captcha_serpro_gov_br')
            # sleep(2.5)
            # btn_som.click()
            # sleep(.5)
            # cod_caract.click()
            cod_caract.send_keys(CAPT)
            # print(f'PRESSIONE ENTER P/ PROSSEGUIR, {CLIENTE}')
            # press_keys_b4('enter')
            while True:
                try:
                    submit = driver.find_element(By.XPATH,
                                                 "//input[@type='submit']").click()
                    break
                except (NoSuchElementException, ElementClickInterceptedException):
                    print('sleepin'
                          'g, line 167. Cadê o submit?')
                    driver.refresh()
                    sleep(5)
            sleep(5)

    def __loga_simples_capt(self) -> str:
        import subprocess
        import os
        capt = "capt.png"

        img_req = "captcha-img"

        self.webdriverwait_el_by(By.ID, img_req)

        self.driver.execute_script(f"""
        let cap = document.querySelector("#{img_req}");
        let a = document.createElement("a");
        let capSrc = cap.getAttribute("src")
        a.setAttribute("href", capSrc);
        a.setAttribute("download", "{capt}");
        a.click()
        """)  # download image

        uclient_path = self._uclient_path
        capt_image = os.path.join(uclient_path, capt)
        capt_ready = os.path.join(uclient_path, "capt_omega.txt")
        simplificar = r"Rscript"
        scriptpath = os.path.join(os.path.dirname(os.path.abspath(
            __file__)), "rscripts\\scrap_simple.R")
        subprocess.run(
            f"{simplificar} {scriptpath} {capt_image.replace(' ', '&_&')} {capt_ready.replace(' ', '&_&')}"
        )
        os.remove(capt_image)
        scret = open(capt_ready, "r").read()
        return str(scret)

    # Loga certificado do ecac, padrão
    def loga_cert(self):
        """
        :return: mixes the two functions above (show_actual_tk_window, mensagem)
        """
        from random import randint, uniform
        import pyautogui as pygui
        from time import sleep
        from functools import partial
        from threading import Thread

        randsleep = partial(uniform, 1.01, 2.99)
        def randsleep2(n1, n2): return uniform(n1, n2)
        from selenium.webdriver import Chrome

        driver = self.driver
        # driver.set_window_position(1912, -8)
        pos = (1912, -8), (0, 0), (0, 0)
        driver.set_window_position(*pos[randint(0, 1)])
        # driver.set_window_size(randint(900, 1350), randint(550, 1000))

        driver.get("https://sso.acesso.gov.br/authorize?response_type=code&client_id=cav.receita.fazenda.gov.br&scope=openid+govbr_recupera_certificadox509+govbr_confiabilidades&redirect_uri=https://cav.receita.fazenda.gov.br/autenticacao/login/govbrsso&state=aESzUCvrPCL56W7S")
        # 17bd6f43454
        initial = WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, 'Seu certificado digital')))
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 'T')
        sleep(2)
        make_login = initial.get_attribute("href")

        driver.execute_script("window.open()")

        driver.switch_to.window(driver.window_handles[1])
        a = Thread(target=lambda: driver.get(make_login))
        a.start()
        sleep(randsleep2(0.71, 2.49))
        [pygui.hotkey('enter', interval=randsleep2(0.21, 0.78))  # down, enter
         for i in range(3)]
        pygui.hotkey('ctrl', 'w')
        # driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # driver.execute_script("closeModal('modal-tips')")
        initial.click()
        print('ativando janela acima, logando certificado abaixo, linhas 270')
        sleep(randsleep2(3, 7))
        driver.get("https://cav.receita.fazenda.gov.br/autenticacao/login")
        sleep(10)
        # driver.execute_script("validarRecaptcha('frmLoginCert')")
        sleep(10)

        self.click_elements_by_tt("Acesso Gov BR", tortil='alt')
        while self.driver.current_url == "https://cav.receita.fazenda.gov.br/autenticacao/login":
            try:
                self.click_elements_by_tt("Acesso Gov BR", tortil='alt')
            except NoSuchElementException as e:
                pass
                sleep(1)
                print("sleeping...")
        # TODO descobrir pq zerar ICMS por certificado não funciona direito

    def change_ecac_client(self, CNPJ):
        """:return: vai até ao site de declaração do ECAC."""
        driver = self.driver
        # Merge me after with others like me...
        for i in range(randint(1, 2)):
            driver.get("https://cav.receita.fazenda.gov.br/ecac/")
            driver.implicitly_wait(10)
            sleep(randint(3, 5))

        def elem_with_text(elem, searched):
            _tag = driver.find_element(By.XPATH,
                                       f"//{elem}[contains(text(),'{searched.rstrip()}')]")
            return _tag

        self.tags_wait('html', 'span')
        sleep(5)
        # nextcl = elem_with_text("span", "Alterar perfil de acesso")
        # nextcl.click()
        btn_perfil = WebDriverWait(self.driver, 20).until(
            expected_conditions.presence_of_element_located((By.ID, 'btnPerfil')))
        self.click_ac_elementors(btn_perfil)
        # altera perfil e manda o cnpj
        self.tags_wait('label')

        cnpj = elem_with_text("label", "Procurador de pessoa jurídica - CNPJ")
        cnpj.click()
        sleep(.5)
        self.send_keys_anywhere(CNPJ)
        sleep(1)
        self.send_keys_anywhere(Keys.TAB)
        self.send_keys_anywhere(Keys.ENTER)
        sleep(1)
        # driver.find_element(By.CLASS_NAME, 'access-button').click()
        # sleep(10)
        antigo = driver.current_url

        """I GOT IT"""
        # switch_to.frame...

        sleep(5)
        driver.get(
            'https://sinac.cav.receita.fazenda.gov.br/simplesnacional/aplicacoes/atspo/pgdasd2018.app/')
        sleep(2.5)
        driver.get(antigo)
        driver.get(
            'https://cav.receita.fazenda.gov.br/ecac/Aplicacao.aspx?id=10009&origem=menu')
        driver.switch_to.frame(self.webdriverwait_el_by(By.TAG_NAME, "iframe"))
        sleep(2)
        while True:
            try:
                # don't need anymore
                # break
                driver.find_element(By.XPATH,
                                    '//span[@class="glyphicon glyphicon-off"]').click()
                driver.refresh()
                break
            except ElementClickInterceptedException:
                print('---> PRESSIONE ESC PARA CONTINUAR <--- glyphicon-off intercepted')
                press_key_b4('esc')
            except NoSuchElementException:
                print('---> PRESSIONE ESC PARA CONTINUAR NoSuchElement glyphicon-off')
                press_key_b4('esc')
                driver.get(
                    'https://sinac.cav.receita.fazenda.gov.br/simplesnacional/aplicacoes/atspo/pgdasd2018.app/')
                driver.implicitly_wait(5)
                break
        sleep(3)
        driver.switch_to.default_content()
        """I GOT IT"""
        # chegou em todo mundo...

        driver.get(
            'https://sinac.cav.receita.fazenda.gov.br/simplesnacional/aplicacoes/atspo/pgdasd2018.app/')
        driver.implicitly_wait(5)

    def compt_typist(self, compt):
        driver = self.driver
        self.tags_wait('body', 'input')
        # self.webdriverwait_el_by(By.TAG_NAME, )
        onlif = 'declaracao'
        if onlif not in driver.current_url:
            driver.execute_script(
                f"""window.location.href += '{onlif}?clear=1'""")

        driver.implicitly_wait(10)
        periodo = self.webdriverwait_el_by(By.ID, 'pa', 20)
        periodo.send_keys(compt)
        self.find_submit_form()

    def compt_typist_valtotal(self, valor_total=None):
        driver = self.driver
        compt = self.compt
        VALOR_ZERADO = 0
        valor_total = 0 if valor_total is None else valor_total

        self.webdriverwait_el_by(By.TAG_NAME, "input")
        self.send_keys_anywhere(valor_total)
        self.send_keys_anywhere(Keys.TAB)
        self.send_keys_anywhere(VALOR_ZERADO)
        try:
            self.find_submit_form()
        except NoSuchElementException:
            driver.find_elements(By.CLASS_NAME,
                                 'btn-success')[1].click()

    def compt_already_declared(self, compt):
        driver = self.driver
        try:
            js_confirm = driver.find_element(By.ID, 'jsMsgBoxConfirm')
            """
            tk_msg('F2 para somente gerar os últimos 3 arquivos de declarações.\n F4 para RETIFICAR'
                   '\nF10 p/ consolidar para ultima data do mês\n\n'
                   '\nF11 Para passar para o próximo cliente \n\n'
                   'Espere ou clique OK', 10)
            """
            print('F2 para somente gerar os últimos 3 arquivos de declarações.\n F4 para RETIFICAR'
                  '\nF10 p/ consolidar para ultima data do mês\n\n'
                  '\nF11 Para passar para o próximo cliente \n\n'
                  'Espere ou clique OK')
            # não consegui callback em mensagem
            which_one = press_keys_b4('f2', 'f4', 'f10', 'f11')
            print(type(which_one))
            print(which_one)

            if which_one == 'f2':
                # consultar declarações, baixar arquivos
                self.simples_and_ecac_utilities(2, compt)

            elif which_one == 'f4':
                print('RETIFICA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                driver.execute_script("""
                window.location.href = '/SimplesNacional/Aplicacoes/ATSPO/pgdasd2018.app/Pa/Retificar'""")
                # raise vai fazer a ratificação
                raise NoSuchElementException
            elif which_one == 'f10':
                self.simples_and_ecac_utilities(1, compt)
                # F10 p/ consolidar para ultima data do mês
            elif which_one == 'f11':
                pass
        except NoSuchElementException:
            # already_declared is False...
            # próxima etapa
            return False
        else:
            return True

    def sair_com_seguranca(self):
        self.driver.get('https://cav.receita.fazenda.gov.br/ecac/')
        self.webdriverwait_el_by(By.ID, 'sairSeguranca').click()
        self.driver.close()
        self.driver.quit()

    def __set_driver(self):
        self.driver.set_window_position(2000, 0)
        self.driver.maximize_window()
