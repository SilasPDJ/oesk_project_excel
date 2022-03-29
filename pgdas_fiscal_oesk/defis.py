
# from pgdas_fiscal_oesk.silas_abre_g5_loop_v9_iss import G5
from default.webdriver_utilities.pre_drivers import pgdas_driver, pgdas_driver_ua, ginfess_driver
from default.sets import get_compt
from pgdas_fiscal_oesk import Consultar

from default.webdriver_utilities import WDShorcuts
from default.sets import InitialSetting

from default.sets import get_all_valores
import os
import tkinter as tk

COMPT = get_compt(-1)
CONS = Consultar(COMPT)


class Defis(WDShorcuts, InitialSetting):
    def __init__(self, compt=None):
        """
        :param compt: from GUI
        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        from default.webdriver_utilities.pre_drivers import pgdas_driver
        # O vencimento DAS(seja pra qual for a compt) está certo, haja vista que se trata do mes atual

        sh_names = ['DEFIS']
        sh_name = sh_names[0]

        if compt is None:
            compt = COMPT

        excel_file_name = CONS.MAIN_FILE

        COMPT = compt = f"DEFIS_{self.y()}"
        # transcrevendo compt para que não seja 02/2021

        # excel_file_name = '/'.join(excel_file_name.split('/')[:-1])
        excel_file_name = os.path.dirname(excel_file_name)
        excel_file_name += f'/DEFIS-anual.xlsx'
        pdExcelFile = pd.ExcelFile(excel_file_name)
        #######
        msh = pdExcelFile.parse(sheet_name=str(sh_name))
        col_str_dic = {column: str for column in list(msh)}

        msh = pdExcelFile.parse(sheet_name=str(sh_name), dtype=col_str_dic)
        READ = self.le_excel_each_one(msh)
        self.after_READ = self.readnew_lista(READ, False)

        msh_socio = pdExcelFile.parse(sheet_name='Socios')
        col_str_dic = {column: str for column in list(msh_socio)}
        msh_socio = pdExcelFile.parse(sheet_name='Socios', dtype=col_str_dic)
        self.after_socio = self.readnew_lista(
            self.le_excel_each_one(msh_socio))

        SK = list(self.after_socio.keys())
        #  ACHEI FINALMENTE O JEITO RESPONSIVO DE DECLARAR PRA NÃO FICAR TENDO QUE ESCREVER POR EXTENSO

        cont_soc = 0
        for i, CNPJ in enumerate(self.after_READ['CNPJ']):
            _cliente = self.empresa_now = self.after_READ['Razão Social'][i]
            _ja_declared = self.after_READ['Declarado'][i].upper().strip()
            _cod_sim = self.after_READ['Código Simples'][i]
            _cpf = self.after_READ['CPF'][i]
            _cert_or_login = self.after_READ['CERTORLOGIN'][i]

            # Defis exclusivos
            _dirf = self.after_READ['DIRF'][i]
            # +2 Pois começa da linha 2, logo o excel está reconhendo isso como index
            while int(self.after_socio[SK[-4]][cont_soc])-2 != i:
                cont_soc += 1
            __ate_soc = self.after_socio[SK[-3]][cont_soc]
            __ate_soc = int(__ate_soc) + cont_soc

            self.socios_now__cnpj = self.after_socio[SK[0]][cont_soc:__ate_soc]
            self.socios_now__cpf = self.after_socio[SK[1]][cont_soc:__ate_soc]
            self.socios_now__nome = self.after_socio[SK[2]][cont_soc:__ate_soc]
            self.socios_now__cota = self.after_socio[SK[3]][cont_soc:__ate_soc]
            self.socios_now__tipo = self.after_socio[SK[5]][cont_soc:__ate_soc]

            self.client_path = self.files_pathit(_cliente, COMPT, )
            if _ja_declared not in ['S', 'OK', 'FORA']:
                print('-' * 60)
                # print(f'CNPJ: {CNPJ}, {CNPJ.strip()==self.socios_now__cnpj[0]}')
                self.the_print()

                __client_path = self.client_path
                self.driver = pgdas_driver(__client_path)
                now_process = subprocess.Popen(f'explorer {__client_path}')
                driver = self.driver
                super().__init__(driver)

                if _cert_or_login == 'certificado':
                    self.loga_cert()
                    # loga ECAC, Insere CNPJ
                    self.change_ecac_client(CNPJ)

                    self.current_url = driver.current_url
                    self.opta_script() if self.m() == 12 else None

                else:
                    self.loga_simples(CNPJ, _cpf, _cod_sim, _cliente)
                    self.current_url = driver.current_url
                    self.opta_script() if self.m() == 12 else None

                driver.get(
                    'https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/defis.app/entrada.aspx')
                while True:
                    try:
                        WebDriverWait(self.driver, 10).until(
                            expected_conditions.presence_of_element_located((By.TAG_NAME, 'input')))
                        my_radios_bt = driver.find_elements_by_name(
                            'ctl00$conteudo$AnoC')
                        my_radios_bt[-2].click()
                        driver.find_element_by_id(
                            'ctl00_conteudo_lnkContinuar').click()
                        break
                    except TimeoutException:
                        driver.get(
                            'https://sinac.cav.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/defis.app/entrada.aspx')
                (print('sleeping'), sleep(5))
                self.send_keys_anywhere(Keys.TAB, 2)
                self.send_keys_anywhere(Keys.ENTER, 1)
                self.contains_text(str(self.y()-1)).click()
                self.contains_text('Continuar').click()
                driver.implicitly_wait(10)
                self.send_keys_anywhere(Keys.TAB, 9)
                self.send_keys_anywhere(Keys.ENTER, 1)
                self.send_keys_anywhere(Keys.TAB, 2)
                self.send_keys_anywhere(Keys.ENTER, 1)
                WebDriverWait(self.driver, 5)
                try:
                    self.send_keys_anywhere(Keys.TAB, 1)
                    self.send_keys_anywhere(Keys.ENTER, 1)
                except UnexpectedAlertPresentException:
                    pass
                else:
                    # se 3 => De toda MP
                    self.send_keys_anywhere(Keys.TAB, 2)
                    self.send_keys_anywhere(Keys.ENTER)

                    self.send_keys_anywhere(Keys.TAB, 1)
                    # Informações econômicas e fiscais do estabelecimento

                    ac = ActionChains(self.driver)
                    for sdc in range(13):
                        ac.send_keys('0')
                        ac.send_keys(Keys.TAB)
                    ac.perform()
                    self.send_keys_anywhere(Keys.TAB, 11, pause=.1)

                    self.send_keys_anywhere(Keys.RIGHT)
                    self.send_keys_anywhere(Keys.TAB)
                    self.send_keys_anywhere(Keys.RIGHT)

                    self.send_keys_anywhere(Keys.TAB, 15, pause=.001)
                    self.send_keys_anywhere(Keys.ENTER)

                    # Chega até os campos padrão

                print('\033[1;31m DIGITE F8 p/ prosseguir \033[m')
                which_one = press_key_b4('f8')
                now_process.kill()
            print('-' * 30)
            print(f'already declared {_cliente}')
            print('-' * 30)

    def loga_cert(self):
        """
        :return: mixes the two functions above (show_actual_tk_window, mensagem)
        """
        from threading import Thread
        from pyautogui import hotkey
        from time import sleep

        driver = self.driver
        while True:
            try:
                driver.get(
                    'https://cav.receita.fazenda.gov.br/autenticacao/login')
                driver.set_page_load_timeout(30)
                break
            except TimeoutException:
                driver.refresh()
            finally:
                sleep(1)

        activate_window('eCAC - Centro Virtual de Atendimento')
        """
        while True:
            try:
                driver.get('https://cav.receita.fazenda.gov.br/')
                driver.set_page_load_timeout(5)
                break
            except TimeoutException:
                driver.refresh()
            finally:
                sleep(1)
        """
        # initial = driver.find_element_by_id('caixa1-login-certificado')
        driver.get(
            'https://sso.acesso.gov.br/authorize?response_type=code&client_id=cav.receita.fazenda.gov.br&'
            'scope=openid+govbr_recupera_certificadox509+govbr_confiabilidades&'
            'redirect_uri=https://cav.receita.fazenda.gov.br/autenticacao/login/govbrsso')
        initial = driver.find_element_by_link_text('Certificado digital')

        print('ativando janela acima, logando certificado abaixo, linhas 270')
        sleep(2)
        # self.thread_pool_executor(initial.click, [hotkey, 'enter'])

        t = Thread(target=initial.click)
        t.start()
        tt = Thread(target=sleep(2.5))
        tt.start()
        # B4 enter, ir pra baixo por causa do certificado do castilho
        tb4 = Thread(target=hotkey('down'))
        tb4.start()
        tt2 = Thread(target=sleep(2))
        tt2.start()
        t2 = Thread(target=hotkey('enter'))
        t2.start()

    def loga_simples(self, CNPJ, CPF, CodSim, CLIENTE):
        driver = self.driver
        driver.get(
            'https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')

        driver.get(
            'https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')
        while str(driver.current_url.strip()).endswith('id=60'):

            self.tags_wait('body')
            self.tags_wait('html')
            self.tags_wait('input')

            # driver.find_elements_by_xpath("//*[contains(text(), 'CNPJ:')]")[0].click()
            # pygui.hotkey('tab', interval=0.5)
            cpcp = driver.find_element_by_name(
                'ctl00$ContentPlaceHolder$txtCNPJ')
            cpcp.clear()
            cpcp.send_keys(CNPJ)

            cpfcpf = driver.find_element_by_name(
                'ctl00$ContentPlaceHolder$txtCPFResponsavel')
            cpfcpf.clear()
            cpfcpf.send_keys(CPF)

            cod = driver.find_element_by_name(
                'ctl00$ContentPlaceHolder$txtCodigoAcesso')
            cod.clear()
            cod.send_keys(CodSim)

            cod_caract = driver.find_element_by_id(
                'txtTexto_captcha_serpro_gov_br')
            btn_som = driver.find_element_by_id(
                'btnTocarSom_captcha_serpro_gov_br')
            sleep(2.5)
            btn_som.click()
            sleep(.5)
            cod_caract.click()
            print(f'PRESSIONE ENTER P/ PROSSEGUIR, {CLIENTE}')
            press_key_b4('enter')
            while True:
                try:
                    submit = driver.find_element_by_xpath(
                        "//input[@type='submit']").click()
                    break
                except (NoSuchElementException, ElementClickInterceptedException):
                    print('sleepin'
                          'g, line 167. Cadê o submit?')
                    driver.refresh()
                    sleep(5)
            sleep(5)

    def change_ecac_client(self, CNPJ):
        """:return: vai até ao site de declaração do ECAC."""
        driver = self.driver

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
        month_compt = compt[:2]
        year_compt = compt[2:]

        driver = self.driver
        current_url = self.current_url
        link_gera_das, download_protocolos_das = 'Das/PorPa', '/Consulta'

        if option == 2:

            self.get_sub_site(download_protocolos_das, current_url)
            driver.implicitly_wait(5)

            if now_year != year_compt:
                self.send_keys_anywhere(year_compt)
                self.find_submit_form()
                sleep(3.5)

            comp_clic = driver.find_elements_by_class_name('pa')
            lenc = len(comp_clic) - 1
            comp_clic[lenc].click()
            for i in range(3):
                sleep(2)
                self.send_keys_anywhere(Keys.TAB)
                self.send_keys_anywhere(Keys.ENTER)

        elif option == 1:
            # gera das
            venc_month_compt = int(month_compt) + 1
            venc = self.get_last_business_day_of_month(
                venc_month_compt, int(year_compt))
            retifica_p_dia = f'{venc}{venc_month_compt:02d}{year_compt}'
            self.get_sub_site(link_gera_das, current_url)
            self.tags_wait('input')
            driver.implicitly_wait(10)
            periodo = driver.find_element_by_id('pa')
            periodo.send_keys(compt)
            self.find_submit_form()
            sleep(2.5)
            # if  len(driver.find_elements_by_id('msgBox')) == 0 # CASO NÃO EXISTA O DAS
            consolida = driver.find_element_by_id('btnConsolidarOutraData')
            consolida.click()
            sleep(2.5)

            validade_id = 'txtDataValidade'
            driver.execute_script(
                f"document.getElementById('{validade_id}').focus();")
            validade_change = driver.find_element_by_id(validade_id)
            for e, val in enumerate(retifica_p_dia):
                validade_change.send_keys(val)
                if e == 0:
                    sleep(.25)

            sleep(1)
            driver.find_element_by_id('btnDataValidade').click()
            # coloquei a validade
            # gerei das
            driver.implicitly_wait(5)
            self.find_submit_form()
            # GERAR DAS
        else:
            tk_msg(f'Tente outra opção, linha 550 +-, opc: {option}')

    def opta_script(self):
        driver = self.driver
        try:
            # #################################################### opta
            self.get_sub_site('/RegimeApuracao/Optar', self.current_url)
            # driver.execute_script("""window.location.href += '/RegimeApuracao/Optar'""")

            anocalendario = Select(driver.find_element_by_id('anocalendario'))

            anocalendario.select_by_value('2021')
            self.find_submit_form()

            # competencia
            competencia, caixa = '0', '1'

            driver.find_element_by_css_selector(
                f"input[type='radio'][value='{competencia}']").click()
            self.find_submit_form()
            sleep(2.5)
            # driver.find_element_by_id('btnSimConfirm').click()

            try:
                driver.implicitly_wait(10)
                self.click_ac_elementors(
                    driver.find_element_by_class_name('glyphicon-save'))
            except NoSuchElementException:
                input('Não consegui')
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

    def the_print(self):

        len_nome = len(self.socios_now__nome)
        print(self.empresa_now)
        print(f'{"CNPJ":<10}{"Nome":>10}{"CPF":>38}{"COTA":>21}{"COTA %":>10}')

        total_calc = sum(int(v) for v in self.socios_now__cota)

        for ins in range(len(self.socios_now__cnpj)):

            soc_cnpj = self.socios_now__cnpj[ins]
            soc_nome = self.socios_now__nome[ins]
            soc_cpf = self.socios_now__cpf[ins]
            soc_cota = self.socios_now__cota[ins]
            print(f'{soc_cnpj:<16}', end='')
            print(f'{soc_nome:<{40 - len_nome}}', end='')
            print(f'{soc_cpf:>9}', end='')
            print(f'{soc_cota:>10}', end='')

            cota = int(soc_cota) / total_calc
            print('      ', cota)
        print(self.socios_now__tipo)
        print('-' * 60)
        print()


Defis()
