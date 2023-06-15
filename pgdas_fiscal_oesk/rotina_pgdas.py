# dale
from random import randint
from typing_extensions import override
# from default.sets import InitialSetting
# from default.webdriver_utilities.wbs import WDShorcuts
from default.interact import press_keys_b4, press_key_b4
from default.webdriver_utilities.pre_drivers import pgdas_driver, pgdas_driver_ua, default_qrcode_driver
from .rotina_pgdas_simplesnacional_utils import SimplesNacionalUtilities
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium import webdriver
from time import sleep
from default.sets.pathmanager import HasJson
# from . import *
# qualquer coisa me devolve

# class SimplesNacionalUtilities(WDShorcuts, NewSetPaths, ExcelToData):


class PgdasDeclaracao(SimplesNacionalUtilities):
    def __init__(self, *args, compt, all_valores=None, driver: webdriver.Remote = None):
        __r_social, __cnpj, __cpf, __cod_simples, __valor_competencia, proc_ecac = args
        # __anexo,  __valor_n_ret, __valor_ret, already_declared

        # competencia declarada
        self.compt = compt
        self.client_path = self.files_pathit(__r_social.strip(), self.compt)
        print(
            "\033[1;31m Estou procurando declarações. EXCLUIR CASO RETIFICAR\033[m")
        # self.client_path = self.pathit(self.compt, main_path, __r_social)
        if not self.walget_searpath("PGDASD-DECLARACAO", self.client_path, 2):
            # drivers declarados
            try:
                assert driver is None, 'Driver is None'
                self.driver = pgdas_driver(self.client_path)
            except AssertionError as e:
                self.driver = driver
            finally:
                super().__init__(self.driver, self.compt, self.client_path)

            # self.driver.maximize_window;()

            [print('\033[1;33m', __cod_simples, '\033[m')for i in range(1)]

            if __cod_simples is None or __cod_simples == '-' or proc_ecac.lower().strip() == 'sim':

                self.loga_cert()
                self.change_ecac_client(__cnpj)
                self.enable_download_in_headless_chrome(self.files_pathit(__r_social.strip(), self.compt))
            else:
                self.loga_simples(__cnpj, __cpf, __cod_simples, __r_social)
            if self.driver.current_url == "https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/AvisoMensagens.aspx":
                print("pressione f9 para continuar")
                press_keys_b4("f9")
                try:
                    self.driver.find_element(By.NAME,
                                             "ctl00$ContentPlaceHolder$btnContinuarSistema").click()
                except NoSuchElementException:
                    self.driver.refresh()
            self.current_url = self.driver.current_url
            self.link_gera_das, self.download_protocolos_das = 'Das/PorPa', '/Consulta'
            # antes da compt typist:
            try:
                self.tag_with_text('span', 'DEVEDOR')
                self.criar_json_das_atrasados()
                self.gerar_das_atrasados_sem_parc()
            except NoSuchElementException:
                pass
            self.opta_script() if self.m() == 12 else None

            # loga e digita competencia de acordo com o BD
            self.compt_typist(self.compt)
            try:
                self.webdriverwait_el_by(By.ID, "msgBox", 3)
                self.opta_script(False)
            except (NoSuchElementException, TimeoutException):
                print("No msgBox")
            else:
                self.compt_typist(self.compt)
            # declara compt de acordo com o valor
            if not self.compt_already_declared(self.compt):
                __valor_competencia = 0 if float(
                    __valor_competencia) == 0 else __valor_competencia

                if float(__valor_competencia) == 0:
                    self.declaracao_sem_movimento(__valor_competencia)

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
        self.webdriverwait_el_by(By.TAG_NAME, 'button')
        self.find_submit_form()
        self.webdriverwait_el_by(By.TAG_NAME, "body", 30)
        self.webdriverwait_el_by(By.TAG_NAME, "body", 30)
        try:
            self.find_submit_form()
        except TimeoutException:
            pass
        except NoSuchElementException as e:
            pass

        self.simples_and_ecac_utilities(2, compt)
        # driver.save_screenshot(self.certif_feito(
        #     self.client_path, add="SimplesNacional-SemMovimento"))

    def declaracao_anexos(self, __valores_de_anexos: list, valor_competencia, cnpj):
        def new_seleciona_anexo(which_one):
            # Só ativa se ainda não estiver ativado
            self.driver.execute_script(f"""
                let elnow = document.querySelector("a[data-atividade='{cnpj}-{which_one}']");
                elnow.parentElement.classList.contains('active') ? null : elnow.click();
            """)
            # clica nos que tavam marcados anteriormente

        # https://www.contabeis.com.br/ferramentas/simples-nacional/6920601/
        driver = self.driver
        compt = self.compt
        valor_competencia = self.trata_money_excel(valor_competencia)
        self.compt_typist_valtotal(valor_competencia)

        exibe_tutti = self.webdriverwait_el_by(By.ID, 'btn-exibe-todos', 30)
        exibe_tutti.click()
        self.driver.execute_script(
            'for (el of document.getElementsByClassName("active atividade item-grupo")) el.click();')

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

             # reseta para settar novamente...
            if float(tres_valores.get("sem_retencao")) != 0:
                new_seleciona_anexo(sem_ret)
            if float(tres_valores.get("com_retencao")) != 0:
                new_seleciona_anexo(com_ret)

        self.find_submit_form()

        # Aqui ele já acha os input text e envia os valores para ele, ordenadamente
        # Porém preciso checar caso tenha mais de um anexo
        # Além disso, preciso somar caso os anexos se repitam, porém pretendo
        # fazer isso no backend
        inputs_text = self.driver.find_elements(By.CSS_SELECTOR,
                                                "input[type='text']")
        _count = 0
        for tres_valores in __valores_de_anexos:
            v_n_ret = self.trata_money_excel(
                tres_valores.get("sem_retencao"))
            v_ret = self.trata_money_excel(tres_valores.get("com_retencao"))

            if float(tres_valores.get("sem_retencao")) != 0:
                inputs_text[_count].clear()
                inputs_text[_count].send_keys(v_n_ret)
                _count += 1
                # new_seleciona_anexo(sem_ret)
            if float(tres_valores.get("com_retencao")) != 0:
                if tres_valores["anexo"] == 'I':
                    print('Ainda não sei... Pressione F8 para prosseguir')
                    press_key_b4('F8')
                inputs_text[_count].clear()
                inputs_text[_count].send_keys(v_ret)
                _count += 1
                # new_seleciona_anexo(com_ret)
        # self.find_submit_form()
        self.driver.find_elements(By.CLASS_NAME, 'btn-success')[1].click()

        self.driver.implicitly_wait(30)
        sleep(3.5)
        try:
            self.find_submit_form()
        except NoSuchElementException:
            driver.find_elements(By.CLASS_NAME, 'btn-success')[1].click()

        self.driver.implicitly_wait(30)

        for i in range(2):
            driver.find_elements(By.CLASS_NAME, 'btn-success')[1].click()
            sleep(3)

        try:
            self.find_submit_form()
        except NoSuchElementException:
            driver.find_elements(By.CLASS_NAME, 'btn-success')[0].click()

        # self.driver.save_screenshot(self.certif_feito(
        #     self.client_path, add='SimplesNacional_declarado'))

        # driver.find_elements(By.CLASS_NAME, 'btn-success')[1].click()

        # TODO Gera DAS, pode virar um método???
        # self.get_sub_site(self.link_gera_das, self.current_url)

        # self.send_keys_anywhere(self.compt)
        # self.send_keys_anywhere(Keys.ENTER)
        # driver.find_elements(By.CLASS_NAME, 'btn-success')[1].click()

        self.simples_and_ecac_utilities(2, self.compt)

    def criar_json_das_atrasados(self):
        from bs4 import BeautifulSoup
        import os
        driver = self.driver
        try:
            self.tag_with_text('span', 'DEVEDOR')
            # return
        except NoSuchElementException as e:
            raise
        onlif = 'Debitos'
        if onlif not in driver.current_url:
            driver.execute_script(
                f"""window.location.href += '{onlif}'""")
        table_webelement = self.webdriverwait_el_by(
            By.TAG_NAME, 'form').find_element(By.TAG_NAME, 'table')
        # html = pd.read_html(table_data.get_attribute('innerHTML'))

        soup = BeautifulSoup(table_webelement.get_attribute(
            'innerHTML'), 'html.parser')
        print('~'*30)
        print('~'*30)
        print('~'*30)
        # input(soup)
        # HasJson.dump_json()
        list_parcs = []
        for tb__compt, exibi, val_em_aberto in zip(soup.select('tr td:nth-child(2)'), soup.select('tr td:nth-child(9)'), soup.select('tr td:nth-child(8)')):
            # print(exibi.text)
            # print(tb__compt.text)
            list_parcs.append({tb__compt.text: exibi.text,
                              'em_aberto': val_em_aberto.text})
        if len(list_parcs) >= 1:
            HasJson.dump_json(list_parcs, os.path.join(
                self.client_path, 'DAS_EM_ABERTO.json'))

    def gerar_das_atrasados_sem_parc(self):
        import os
        self.driver.get(self.current_url)

        das_json = HasJson.load_json(os.path.join(
            self.client_path, 'DAS_EM_ABERTO.json'))

        # list of compts pendentes:
        pend_compts = []
        for lspart in das_json:
            pend_compts.append(list(lspart.keys())[0])
        for e, lspart in enumerate(das_json):
            n_parc = lspart[pend_compts[e]]
            print_parcs = "\033[1;31mSem parcelamento\033[m" if n_parc == "0" else "\033[1;33mJÁ ESTÁ PARCELADO\033[m"
            print(
                n_parc, pend_compts[e], print_parcs)
            if n_parc == "0":
                self.simples_and_ecac_utilities(1, pend_compts[e])
                self.driver.get(self.current_url)
                # TODO: testar-me
        self.driver.get(self.current_url)


class PgdasDeclaracaoRetificaVarias(PgdasDeclaracao):
    def __init__(self, *args, compt, main_compt, all_valores=None):
        __r_social, __cnpj, __cpf, __cod_simples, __valor_competencia, proc_ecac = args
        # __anexo,  __valor_n_ret, __valor_ret, already_declared

        # competencia declarada
        self.compt = compt
        self.client_path = self.files_pathit(
            __r_social.strip(), compt, f"{main_compt.split('-')[1]}/{main_compt}_retificadoras")
        print(
            "\033[1;31m Estou procurando declarações. EXCLUIR CASO RETIFICAR\033[m")
        # self.client_path = self.pathit(self.compt, main_path, __r_social)
        if not self.walget_searpath("PGDASD-DECLARACAO", self.client_path, 2):
            # drivers declarados
            self.driver = pgdas_driver_ua(self.client_path)

            # self.driver.maximize_window;()

            SimplesNacionalUtilities.__init__(
                self, self.driver, self.compt, self.client_path)
            [print('\033[1;33m', __cod_simples, '\033[m')for i in range(1)]

            if __cod_simples is None or __cod_simples == '-' or proc_ecac.lower().strip() == 'sim':

                self.loga_cert()
                self.change_ecac_client(__cnpj)
            else:
                self.loga_simples(__cnpj, __cpf, __cod_simples, __r_social)
            if self.driver.current_url == "https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/AvisoMensagens.aspx":
                print("pressione f9 para continuar")
                press_keys_b4("f9")
                try:
                    self.driver.find_element(By.NAME,
                                             "ctl00$ContentPlaceHolder$btnContinuarSistema").click()
                except NoSuchElementException:
                    self.driver.refresh()
            self.current_url = self.driver.current_url
            self.link_gera_das, self.download_protocolos_das = 'Das/PorPa', '/Consulta'
            # antes da compt typist:
            try:
                self.tag_with_text('span', 'DEVEDOR')
                # self.criar_json_das_atrasados()
                # self.gerar_das_atrasados_sem_parc()
                # Não é importante nesta class...
            except NoSuchElementException:
                pass
            self.opta_script() if self.m() == 12 else None

            # loga e digita competencia de acordo com o BD
            self.compt_typist(self.compt)
            try:
                self.webdriverwait_el_by(By.ID, "msgBox", 3)
                self.opta_script(False)
            except (NoSuchElementException, TimeoutException):
                print("No msgBox")
            else:
                self.compt_typist(self.compt)
            # declara compt de acordo com o valor
            # podeRetificar nem pergunta...
            if not self.compt_already_declared(self.compt, pode_retificar=True):

                __valor_competencia = 0 if float(
                    __valor_competencia) == 0 else __valor_competencia

                if float(__valor_competencia) == 0:
                    self.declaracao_sem_movimento(__valor_competencia)

                else:

                    self.declaracao_anexos(
                        all_valores, __valor_competencia, __cnpj)

            else:
                print('is already declared')

    @override
    def compt_already_declared(self, compt, pode_retificar=False):
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
            if pode_retificar:
                which_one = 'f4'
            else:
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
