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


# to fazendo um teste

# class SimplesNacionalUtilities(WDShorcuts, NewSetPaths, ExcelToData):


class SimplesNacionalUtilities(InitialSetting, WDShorcuts):

    def __init__(self, driver, compt):
        # super().__init__(driver)

        WDShorcuts.__init__(self, driver)
        self.driver = driver

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
        link_gera_das, download_protocolos_das = self.link_gera_das, self.download_protocolos_das

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
            return False

    def opta_script(self):
        driver = self.driver
        try:
            # #################################################### opta
            self.get_sub_site('/RegimeApuracao/Optar', self.current_url)
            # driver.execute_script("""window.location.href += '/RegimeApuracao/Optar'""")

            from selenium.webdriver.support.ui import Select
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

    def certif_feito(self, save_path, add=''):
        """
        certificado de que está feito
        :param save_path: nome da pasta vinda de _files_path_v2
        :param add: um adicional no nome do arquivo
        :return: caminho+ nome_arquivo jpeg
        """
        client_name = save_path[save_path.index('-')-2: save_path.index('-')+2]
        type_arquivo = 'png'
        try:
            save = r'{}\\{}-SimplesNacionalDeclarado.{}'.format(
                save_path, add, type_arquivo)
            print(save, '---------> SAVE')
            return save
        except FileNotFoundError:
            print('NÃO CONSEGUI RETORNAR SAVE')

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
            press_keys_b4('enter')
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

    # Loga certificado do ecac, padrão

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
        try:
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
        except AttributeError:
            initial.click()
            driver.get("https://cav.receita.fazenda.gov.br/ecac/")
            driver.back()
            driver.get("https://cav.receita.fazenda.gov.br/autenticacao/login")
            ldc = self.webdriverwait_by_id("login-dados-certificado")

            self.click_ac_elementors(ldc.find_elements_by_css_selector("p")[1])

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

    def compt_typist(self, compt):
        driver = self.driver
        self.tags_wait('body', 'input')
        # self.webdriverwait_by_tag()
        onlif = 'declaracao'
        if onlif not in driver.current_url:
            driver.execute_script(
                f"""window.location.href += '{onlif}?clear=1'""")

        driver.implicitly_wait(10)
        periodo = self.webdriverwait_by_id('pa', 20)
        periodo.send_keys(compt)
        self.find_submit_form()

    def compt_typist_valtotal(self, valor_total=None):
        driver = self.driver
        compt = self.compt
        VALOR_ZERADO = 0
        valor_total = 0 if valor_total is None else valor_total

        self.webdriverwait_by_tag("input")
        self.send_keys_anywhere(valor_total)
        self.send_keys_anywhere(Keys.TAB)
        self.send_keys_anywhere(VALOR_ZERADO)
        try:
            self.find_submit_form()
        except NoSuchElementException:
            driver.find_elements_by_class_name(
                'btn-success')[1].click()

    def compt_already_declared(self, compt):
        driver = self.driver
        try:
            js_confirm = driver.find_element_by_id('jsMsgBoxConfirm')
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

    def trata_money_excel(self, faturado):
        try:
            faturado = f'{float(faturado):,.2f}'
        except ValueError:
            print('Já é string')
        finally:
            faturado = faturado.lower().strip()
            if 'nan' in faturado or 'zerou' in faturado:
                faturado = 'SEM VALOR DECLARADO'
                return faturado
            faturado = faturado.replace('.', 'v')
            faturado = faturado.replace(',', '.')
            faturado = faturado.replace('v', ',')
            return faturado


class PgdasDeclaracao(SimplesNacionalUtilities):
    def __init__(self, *args, compt, driver, all_valores=None):

        __r_social, __cnpj, __cpf, __cod_simples, __valor_competencia = args

        # __anexo,  __valor_n_ret, __valor_ret, already_declared

        # competencia declarada
        self.compt = compt

        self.client_path = self.files_pathit(__r_social.strip(), self.compt)
        # self.client_path = self.pathit(self.compt, main_path, __r_social)

        # drivers declarados
        self.driver = driver(self.client_path)
        # self.driver.maximize_window()

        # self.driver.maximize_window;()
        super().__init__(self.driver, self.compt)
        if __cod_simples is None:

            self.loga_cert()
            self.change_ecac_client(__cnpj)
        else:
            self.loga_simples(__cnpj, __cpf, __cod_simples, __r_social)
        if self.driver.current_url == "https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/AvisoMensagens.aspx":
            print("pressione f9 para continuar")
            press_keys_b4("f9")
            try:
                self.driver.find_element_by_name(
                    "ctl00$ContentPlaceHolder$btnContinuarSistema").click()
            except NoSuchElementException:
                self.driver.refresh
        self.current_url = self.driver.current_url
        self.link_gera_das, self.download_protocolos_das = 'Das/PorPa', '/Consulta'

        # loga e digita competencia de acordo com o BD
        self.compt_typist(self.compt)

        # declara compt de acordo com o valor
        if not self.compt_already_declared(self.compt):

            if __valor_competencia == 0:
                self.declaracao_sem_movimento(str(__valor_competencia))

            else:

                self.declaracao_anexos(
                    all_valores, __valor_competencia, __cnpj)

        else:
            print('is already declared')

    def declaracao_sem_movimento(self, valor_zerado):
        driver = self.driver
        compt = self.compt
        self.compt_typist_valtotal(valor_zerado)

        # transmitir
        self.webdriverwait_by_tag('button')
        self.find_submit_form()
        self.webdriverwait_by_tag("body", 30)
        self.webdriverwait_by_tag("body", 30)
        self.find_submit_form()

        self.certif_feito(self.client_path, add="-SemMovimento")
        self.simples_and_ecac_utilities(2, compt)

    def declaracao_anexos(self, __valores_de_anexos, valor_competencia, cnpj):
        def new_seleciona_anexo(which_one):
            self.driver.execute_script(f"""
                let elnow = document.querySelector("a[data-atividade='{cnpj}-{which_one}']");
                elnow.parentElement.classList.contains('active') ? null : elnow.click();
            """)
            # Só ativa se ainda não estiver ativado

        # https://www.contabeis.com.br/ferramentas/simples-nacional/6920601/
        driver = self.driver
        compt = self.compt
        valor_competencia = self.trata_money_excel(valor_competencia)
        self.compt_typist_valtotal(valor_competencia)

        exibe_tutti = self.webdriverwait_by_id('btn-exibe-todos', 30)
        exibe_tutti.click()

        for tres_valores in __valores_de_anexos:
            print(tres_valores)
            print('\n\n')

            ANEXO = tres_valores["anexo"]
            com_ret = sem_ret = 0
            if ANEXO == 'I':
                # exceto para exterior
                sem_ret = 1
                com_ret = 2
                # 3 => exterior
                pass
            elif ANEXO == 'II':
                # venda de mercadorias industrializadas exceto para exterior
                sem_ret = 4
                com_ret = 5
                print('venda')
            elif ANEXO == 'III':

                # print("maioria ISS")
                sem_ret = 14
                com_ret = 15
                # input(sem_ret)
                # input(f'anexo is {ANEXO}')

            elif ANEXO == 'IV':
                sem_ret = 17
                com_ret = 18
                # 18 com ret a ouutro mun

            elif ANEXO == 'V':

                pass
            else:
                raise ValueError(f'Anexo is invalido {ANEXO}')

            if tres_valores.get("valor_n_retido") != 0:
                new_seleciona_anexo(sem_ret)
            if tres_valores.get("valor_retido") != 0:
                new_seleciona_anexo(com_ret)

        self.find_submit_form()

        # Aqui ele já acha os input text e envia os valores para ele, ordenadamente
        # Porém preciso checar caso tenha mais de um anexo
        # Além disso, preciso somar caso os anexos se repitam, porém pretendo
        # fazer isso no backend
        inputs_text = self.driver.find_elements_by_css_selector(
            "input[type='text']")
        _count = 0
        for tres_valores in __valores_de_anexos:
            v_n_ret = self.trata_money_excel(
                tres_valores.get("valor_n_retido"))
            v_ret = self.trata_money_excel(tres_valores.get("valor_retido"))

            if tres_valores.get("valor_n_retido") != 0:
                inputs_text[_count].clear()
                inputs_text[_count].send_keys(v_n_ret)
                _count += 1
                # new_seleciona_anexo(sem_ret)
            if tres_valores.get("valor_retido") != 0:
                inputs_text[_count].clear()
                inputs_text[_count].send_keys(v_ret)
                _count += 1
                # new_seleciona_anexo(com_ret)
        input('SECURITY')
        # self.find_submit_form()
        self.driver.find_elements_by_class_name('btn-success')[1].click()

        self.driver.implicitly_wait(30)
        sleep(3.5)
        try:
            self.find_submit_form()
        except NoSuchElementException:
            driver.find_elements_by_class_name('btn-success')[1].click()

        self.driver.implicitly_wait(30)

        for i in range(2):
            driver.find_elements_by_class_name('btn-success')[1].click()

            sleep(2)
        # self.driver.save_screenshot(self.certif_feito(self.client_path))
        driver.find_elements_by_class_name('btn-success')[2].click()

        # driver.find_elements_by_class_name('btn-success')[1].click()

        # TODO Gera DAS, pode virar um método???
        # self.get_sub_site(self.link_gera_das, self.current_url)

        # self.send_keys_anywhere(self.compt)
        # self.send_keys_anywhere(Keys.ENTER)
        # driver.find_elements_by_class_name('btn-success')[1].click()

        self.simples_and_ecac_utilities(2, self.compt)
