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


class RotinaDividas(InitialSetting, WDShorcuts):
    def __init__(self, *args, compt, driver):
        __r_social, __cnpj, simples_or_ativa = args

        simples_or_ativa = simples_or_ativa.lower().strip()

        self.client_path = self.files_pathit(
            'Dívidas_Simples_' + __r_social, compt)
        __client_path = self.client_path

        self.driver = driver(__client_path)
        super().__init__(self.driver)
        driver = self.driver

        self.loga_cert()
        self.change_ecac_client(__cnpj)

        driver.find_element_by_id('linkHome').click()

        if simples_or_ativa == 'simples nacional':
            driver.find_element_by_link_text(
                'Simples Nacional').click()
            driver.find_element_by_link_text(
                'Solicitar, acompanhar e emitir DAS de parcelamento').click()

            driver.implicitly_wait(10)

            driver.switch_to.frame(
                driver.find_element_by_id('frmApp'))

            empel = driver.find_element_by_id(
                'ctl00_contentPlaceH_linkButtonEmitirDAS')
            empel.click()
            WebDriverWait(self.driver, 20).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, '//input[@value="Continuar"]'))
            ).click()

            imprimires = WebDriverWait(self.driver, 20).until(
                expected_conditions.presence_of_all_elements_located((By.LINK_TEXT, 'Imprimir')))
            for imprimir in imprimires:
                imprimir.click()
            # Imprimir
            driver.switch_to.default_content()
        elif simples_or_ativa == 'dívida ativa':

            driver.find_element_by_link_text(
                'Dívida Ativa da União').click()
            driver.find_element_by_link_text(
                'Débitos Inscritos em Dívida Ativa da União').click()

            driver.switch_to.window(driver.window_handles[1])
            driver.implicitly_wait(10)

            sispar_url = f"{'/'.join(driver.current_url.split('/')[:-1])}/sispar"
            driver.get(sispar_url)
            try:
                WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located((By.TAG_NAME, 'button')))
                self.tag_with_text(
                    'button', 'Acessar o SISPAR').click()
            except NoSuchElementException:
                WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located((By.TAG_NAME, 'button')))
                self.tag_with_text(
                    'button', 'Acessar').click()
                # provavelmente uma mudança no sistema mas vou validar
            # WebDriverWait(self.driver, 10).until(expected_conditions.new_window_is_opened(driver.window_handles))
            WebDriverWait(self.driver, 10).until(
                expected_conditions.number_of_windows_to_be(3))
            driver.switch_to.window(driver.window_handles[2])

            driver.execute_script(
                "PrimeFaces.addSubmitParam('cabecalho',{'cabecalho:j_idt45':'cabecalho:j_idt45'}).submit('cabecalho');")
            self.click_elements_by_tt('DEFERIDO E CONSOLIDADO')
            sleep(1)
            WebDriverWait(self.driver, 20).until(
                expected_conditions.presence_of_element_located((By.ID, 'formListaDarf:idbtnDarf'))).click()

            WebDriverWait(self.driver, 20).until(
                expected_conditions.presence_of_element_located((By.TAG_NAME, 'table')))
            compt_dividas_ativas = f'{self.m():02d}/{self.y()}'
            print(compt_dividas_ativas)

            sleep(7)

            dris = driver.find_elements_by_css_selector(
                ".colunaAlinhaCentro")

            elemitidos = driver.find_elements_by_css_selector(
                f"[title*='Já emitido']")
            for el in elemitidos:
                el.click()
                sleep(.5)
                self.send_keys_anywhere(Keys.ENTER)
            print('breakou, baixou JÁ EMITIDOS')
            self.contains_title('Não emitido').click()
            sleep(.5)
            self.send_keys_anywhere(Keys.ENTER)
            self.click_ac_elementors(WebDriverWait(self.driver, 20).until(
                expected_conditions.presence_of_element_located((
                    By.ID, 'formResumoParcelamentoDarf:dlgInformacoesEmissaoDarf'))))
            self.send_keys_anywhere(Keys.TAB)
            self.send_keys_anywhere(Keys.TAB)
            self.send_keys_anywhere(Keys.ENTER)

            self.click_ac_elementors(WebDriverWait(self.driver, 20). until(
                expected_conditions.presence_of_element_located((By.ID, 'formResumoParcelamentoDarf:emitirDarf'))))

            WebDriverWait(self.driver, 5)

    def loga_cert(self):
        """
        :return: mixes the two functions above (show_actual_tk_window, mensagem)
        """
        import pyautogui as pygui
        from time import sleep
        driver = self.driver

        driver.get("https://sso.acesso.gov.br/authorize?response_type=code&client_id=cav.receita.fazenda.gov.br&scope=openid+govbr_recupera_certificadox509+govbr_confiabilidades&redirect_uri=https://cav.receita.fazenda.gov.br/autenticacao/login/govbrsso&state=aESzUCvrPCL56W7S")

        initial = WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, 'Certificado digital')))

        print('ativando janela acima, logando certificado abaixo, linhas 270')
        sleep(5)

        a = pygui.getWindowsWithTitle('gov.br - Acesse sua conta')[0]
        pygui.click(a.center, clicks=0)
        pygui.move(100, 140)
        pygui.click()
        pygui.move(0, -300)
        print('sleep')
        sleep(2.5)
        pygui.click(duration=.5)

        driver.back()
        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, 'Certificado digital'))).click()

        driver.get("https://cav.receita.fazenda.gov.br/ecac/")
        driver.implicitly_wait(10)
        driver.find_elements_by_tag_name("img")[1].click()

    def change_ecac_client(self, CNPJ):
        """:return: vai até ao site de declaração do ECAC."""
        driver = self.driver

        def elem_with_text(elem, searched):
            _tag = driver.find_element_by_xpath(
                f"//{elem}[contains(text(),'{searched.rstrip()}')]")
            return _tag

        self.tags_wait('html', 'span')
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
        # driver.find_element_by_class_name('access-button').click()
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
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        sleep(2)
        while True:
            try:
                driver.find_element_by_xpath(
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
        # c
