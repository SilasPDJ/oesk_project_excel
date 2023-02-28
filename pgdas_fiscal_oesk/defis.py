
# from pgdas_fiscal_oesk.silas_abre_g5_loop_v9_iss import G5
from default.webdriver_utilities.pre_drivers import pgdas_driver, pgdas_driver_ua, ginfess_driver

from default.sets import get_compt
from pgdas_fiscal_oesk import Consultar

from default.webdriver_utilities import WDShorcuts
from default.sets import InitialSetting
from pgdas_fiscal_oesk.defis_utils.legato import Legato
# from pgdas_fiscal_oesk.defis_utils.legato import transformers as tfms
from .rotina_pgdas_simplesnacional_utils import SimplesNacionalUtilities

import os

from default.interact import *

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, UnexpectedAlertPresentException, TimeoutException


from default.webdriver_utilities.pre_drivers import pgdas_driver, pgdas_driver_ua
from time import sleep

COMPT = get_compt(-1)
CONS = Consultar(COMPT)


class Defis(Legato, SimplesNacionalUtilities):
    def __init__(self):
        """
        :param compt: from GUI
        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        from default.webdriver_utilities.pre_drivers import pgdas_driver
        # O vencimento DAS(seja pra qual for a compt) está certo, haja vista que se trata do mes atual
        sh_name = 'DEFIS'

        self.compt = f"DEFIS_{self.y()}"

        # transcrevendo compt para que não confunda com PGDAS
        _path = os.path.dirname(CONS.MAIN_FILE)
        excel_file_name = os.path.join(_path,
                                       'DEFIS', f'{self.y()-1}-DEFIS-anual.xlsx')
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
            _qtd_empregados__inicio = self.after_READ['emps inicio'][i] or 0
            _qtd_empregados__final = self.after_READ['emps final'][i] or 0
            # Defis exclusivos

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
            self.socios_valor_isento = self.after_socio[SK[6]
                                                        ][cont_soc:__ate_soc]
            self.socios_valor_tributado = self.after_socio[SK[7]
                                                           ][cont_soc:__ate_soc]

            self._socios__soma_cotas = sum(int(v)
                                           for v in self.socios_now__cota)

            self.client_path = self.files_pathit(_cliente, self.compt)
            # if _cert_or_login == "certificado":
            #     continue
            if _ja_declared not in ['S', 'OK', 'FORA']:
                # TODO: conferir PDFs salvo, que nem declaração PGDAS
                print('-' * 60)
                # print(f'CNPJ: {CNPJ}, {CNPJ.strip()==self.socios_now__cnpj[0]}')
                self.the_print()

                __client_path = self.client_path
                self.driver = pgdas_driver(__client_path)
                driver = self.driver
                super().__init__(self.driver, self.compt, self.client_path)

                if _cert_or_login == 'certificado':
                    self.loga_cert()
                    # loga ECAC, Insere CNPJ
                    self.change_ecac_client(CNPJ)

                    self.current_url = driver.current_url
                    self.opta_script() if self.m() == 12 else None
                    self.driver.get(
                        "https://sinac.cav.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/defis.app/entrada.aspx")
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
                # apos continuar
                #
                cnpjtt = "%s%s.%s%s%s.%s%s%s/%s%s%s%s-%s%s" % tuple(
                    self.socios_now__cnpj[0])

                elscrpt = self.tag_with_text("a", cnpjtt).get_attribute("href")
                driver.execute_script(elscrpt)
                self.send_keys_anywhere(Keys.TAB, 11)

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
                self.send_keys_anywhere(Keys.TAB)

                # -- vai pra orientações gerais
                # se 3 => De toda MP
                driver.execute_script(
                    "javascript:mostraEscondeDados('ctl00_conteudo_todemp')")
                WebDriverWait(self.driver, 5)
                sm_tabs = 12
                try:
                    self.tag_with_text("a", "Inatividade em ")
                    sm_tabs += 1
                except NoSuchElementException:
                    print("sm_tabs still the same")
                self.send_keys_anywhere(
                    Keys.TAB, sm_tabs, pause=.001)  # sem mov pode fazer mudar

                self.send_keys_anywhere('0')
                self.send_keys_anywhere(Keys.TAB, pause=.01)
                self.send_keys_anywhere(_qtd_empregados__inicio)
                self.send_keys_anywhere(Keys.TAB, pause=.01)
                self.send_keys_anywhere(_qtd_empregados__final)
                # -- receita proveniente de exportação direta
                self.send_keys_anywhere(Keys.TAB, 2, pause=.01)
                self.send_keys_anywhere('0')

                for ins in range(len(self.socios_now__cnpj)-1):
                    self.driver.find_element(
                        By.CSS_SELECTOR, ("#ctl00_conteudo_InfEconEmpConteudo > div:nth-child(7) > p > a")).click()
                __cpfs_elements = self.driver.find_elements(
                    By.CLASS_NAME, "cpf")
                for ins in range(len(self.socios_now__cnpj)):
                    if __cpfs_elements[ins].tag_name == "input":
                        __cpfs_elements[ins].send_keys(
                            self.socios_now__cpf[ins])
                        if ins > 0:
                            self.send_keys_anywhere(Keys.TAB)
                        self.send_keys_anywhere(Keys.TAB)

                    __valisento = self.trata_sendvals(
                        self.socios_valor_isento[ins])
                    __valtributado = self.trata_sendvals(
                        self.socios_valor_tributado[ins])
                    __soc_cota = self.trata_sendvals(
                        self.socios_now__cota[ins])
                    if int(__soc_cota) % 1 > 0:
                        __sta = (int(__soc_cota) /
                                 self._socios__soma_cotas) * 1000
                    else:
                        __sta = (int(__soc_cota) /
                                 self._socios__soma_cotas) * 10

                    # self.send_keys_anywhere(self.socios_now__cpf[ins])
                    self.send_keys_anywhere(__valisento)

                    self.send_keys_anywhere(Keys.TAB)
                    self.send_keys_anywhere(
                        __valtributado)
                    self.send_keys_anywhere(Keys.TAB)
                    self.send_keys_anywhere(__sta)

                    # imposto de renda retido na fonte sobre os rendimentos
                    self.send_keys_anywhere(Keys.TAB)
                    self.send_keys_anywhere('0')
                for ___ in range(2):
                    self.send_keys_anywhere(Keys.TAB)
                    self.send_keys_anywhere('0')
                    # break

                # Chega até os campos padrão
                from win10toast import ToastNotifier
                ToastNotifier().show_toast("DIGITE F8 p/ prosseguir")
                print('\033[1;31m DIGITE F8 p/ prosseguir \033[m')
                which_one = press_key_b4('f8')
                # now_process.kill()
            print('-' * 30)
            print(f'already declared {_cliente}')
            print('-' * 30)

    def the_print(self):

        len_nome = len(self.socios_now__nome)
        print(self.empresa_now)
        print(f'{"CNPJ":<10}{"Nome":>10}{"CPF":>38}{"COTA":>21}{"COTA %":>10}')

        for ins in range(len(self.socios_now__cnpj)):

            soc_cnpj = self.socios_now__cnpj[ins]
            soc_nome = self.socios_now__nome[ins]
            soc_cpf = self.socios_now__cpf[ins]
            soc_cota = self.socios_now__cota[ins]
            soc_valisento = self.socios_valor_isento[ins]
            soc_valtributado = self.socios_valor_tributado[ins]
            print(f'{soc_cnpj:<16}', end='')
            print(f'{soc_nome:<{40 - len_nome}}', end='')
            print(f'{soc_cpf:>9}', end='')
            print(f'{soc_cota:>10}', end='')
            cota = int(soc_cota) / self._socios__soma_cotas
            print('      ', cota, end='')
            print(f'{soc_valisento:>8}', end='')
            print(f'{soc_valtributado:>8}', end='')
            print()
        print(self.socios_now__tipo)
        print('-' * 60)
        print()
