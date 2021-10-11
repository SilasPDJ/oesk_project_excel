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
from random import randint, uniform


class RotinaDividas(InitialSetting, WDShorcuts):
    def __init__(self, *args, compt, driver):
        for __cli__ in args:
            input(__cli__)
            __r_social, __cnpj, simples_or_ativa = __cli__

            simples_or_ativa = simples_or_ativa.lower().strip()

            self.client_path = self.files_pathit(
                'Dívidas_Simples_' + __r_social, compt)
            __client_path = self.client_path

            if __cli__ == args[0]:
                self.driver = driver()
                super().__init__(self.driver, self.compt)
                self.loga_cert()
            if not hasattr(self, 'driver'):
                raise AttributeError('Sem driver')

            self.enable_download_in_headless_chrome(self.client_path)
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
                sleep(10)
                driver.get(
                    "https://sisparnet.pgfn.fazenda.gov.br/sisparInternet/autenticacao.jsf")
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

    # Loga certificado do ecac, padrão
    def loga_cert(self):
        """
        :return: mixes the two functions above (show_actual_tk_window, mensagem)
        """
        from win10toast import ToastNotifier
        driver = self.driver
        driver.get("https://cav.receita.fazenda.gov.br/ecac/")

        toaster = ToastNotifier()
        toaster.show_toast(
            "PGDAS ECAC", "Faça login uma vez e o resto deixa comigo! Pressione F9 para continuar", duration=10)
        print('PRESSIONE F9 para continuar')

        press_key_b4('f9')

        from random import randint, uniform
        from functools import partial
        # import pyautogui as pygui
        from time import sleep
        # from threading import Thread

        __ = partial(uniform, 1.01, 1.99)
        randsleep = partial(uniform, 1.01, 2.99)
        def randsleep2(n1, n2): return uniform(n1, n2)
        # from selenium.webdriver import Chrome

        # # driver.set_window_position(1912, -8)
        # pos = (1912, -8), (0, 0), (0, 0)
        # driver.set_window_position(*pos[randint(0, 1)])
        # driver.set_window_size(randint(900, 1350), randint(550, 1000))

        # driver.get("https://sso.acesso.gov.br/authorize?response_type=code&client_id=cav.receita.fazenda.gov.br&scope=openid+govbr_recupera_certificadox509+govbr_confiabilidades&redirect_uri=https://cav.receita.fazenda.gov.br/autenticacao/login/govbrsso&state=aESzUCvrPCL56W7S")
        # # 17bd6f43454
        # initial = WebDriverWait(driver, 30).until(
        #     expected_conditions.presence_of_element_located((By.LINK_TEXT, 'Certificado digital')))
        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'T')
        # sleep(2)
        # make_login = initial.get_attribute("href")
        # driver.maximize_window()
        # driver.execute_script("window.open()")
        # driver.switch_to.window(driver.window_handles[1])
        # a = Thread(target=lambda: driver.get(make_login))
        # a.start()
        # sleep(randsleep2(0.71, 2.49))
        # [pygui.hotkey('enter', interval=randsleep2(0.21, 0.78))
        #  for i in range(3)]
        # pygui.hotkey('ctrl', 'w')
        # # driver.close()
        # driver.switch_to.window(driver.window_handles[0])
        # initial.click()
        print('ativando janela acima, logando certificado abaixo, linhas 270')
        sleep(randsleep2(3, 7))
        driver.get("https://cav.receita.fazenda.gov.br/ecac/")
        sleep(randsleep2(3, 7))
        # self.click_elements_by_tt("Acesso Gov BR", tortil='alt')

    def change_ecac_client(self, CNPJ):
        """:return: vai até ao site de declaração do ECAC."""
        driver = self.driver
        # Merge me after with others like me...
        for i in range(randint(1, 2)):
            driver.get("https://cav.receita.fazenda.gov.br/ecac/")
            driver.implicitly_wait(10)
            sleep(randint(3, 5))

        def elem_with_text(elem, searched):
            _tag = driver.find_element_by_xpath(
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
                # don't need anymore
                # break
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
        # chegou em todo mundo...

        driver.get(
            'https://sinac.cav.receita.fazenda.gov.br/simplesnacional/aplicacoes/atspo/pgdasd2018.app/')
        driver.implicitly_wait(5)
