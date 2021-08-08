import pyautogui as pygui
from time import sleep

from default.interact import *
from default.sets import InitialSetting
from default.webdriver_utilities.wbs import WDShorcuts

from pgdas_fiscal_oesk.relacao_nfs import tres_valores_faturados, NfCanceled
from pyperclip import paste
# from default.webdriver_utilities import *

"""
from LE_NF_CANCELADAS_cor import main as nf_canceled
import ATIVA_EMPRESA
import PROGRAMA_REQUIRED
import NEEDED_PANDAS
from datetime import datetime
import os
"""

# um por um?
# vai p/ NEEDED_PANDAS

# ctrl_shift+M


class G5(InitialSetting):

    def __init__(self, *args, compt):
        __r_social, __cnpj, __cpf, __cod_simples, __valor_competencia, imposto_a_calcular = args
        __client = __r_social
        if imposto_a_calcular == 'ICMS':
            pass

        elif imposto_a_calcular == 'ISS':
            self.compt_used = compt
            self.client_path = self.files_pathit(__client)

            meus_3_valores_atuais = tres_valores_faturados(self.client_path)
            # Se tem 3valores[excel], tem XML. Se não tem, não tem
            # (pois o xml e excel vem do ginfess_download)....

            registronta = self.registronta(__client, self.compt_used)
            print(__client)
            input(registronta)
            print(__client)
            if meus_3_valores_atuais and registronta:
                all_xls_inside = self.files_get_anexos_v4(
                    self.client_path, file_type='xlsx')
                relacao_notas = all_xls_inside[0] if len(
                    all_xls_inside) == 1 else IndexError()
                self.activating_client(self.formatar_cnpj(__cnpj))
                # Agora vai ser por cnpj...
                self.start_walk_menu()

                # access ISS lançamento
                pygui.hotkey('right', 'down', 'enter', 'up',
                             'up', 'enter', interval=.1)
                sleep(3.5)

                foritab(2, 'down')
                # busca XML
                pygui.write(self.get_xml(__client))

                """IMPORTA ITENS OU NÃO"""
                # if 'LUCRO PRESUMIDO' in __client:
                # aqui mais pra frente irei validar melhor SE IMPORTA ITEMS OU NÃO
                w = pygui.getActiveWindow()
                pygui.click(w.center)
                pygui.move(-210, 80)  # Importar itens window 1
                pygui.click()
                foritab(2, 'tab')
                pygui.hotkey('enter')

                # window 2, mt legal
                sleep(2)
                w2 = pygui.getActiveWindow()
                pygui.click(w2.center, clicks=0)
                pygui.move(65, -160)  # Copiar configuração da nota...?
                pygui.click()
                pygui.hotkey('tab', 'enter')
                sleep(1)
                pygui.write('1')
                pygui.hotkey('enter')
                foritab(15, 'tab')
                print('Sleeping 2.5 pra enter, enter')
                sleep(2.5)
                foritab(2, 'enter', interval=1)
                sleep(1)
                pygui.hotkey('alt', 'f4')

                nfcanceladas = NfCanceled(relacao_notas)

                print('SLEEPING PARA IMPORTAR')
                self.importa_nfs()
                try:
                    qtd_els = nfcanceladas.conta_qtd_nfs()
                    sleep(qtd_els)
                except TypeError:
                    sleep(5.5)
                pygui.hotkey('enter')

                # vai sleepar dependendo da quantidade de notas, programar ainda isso

                # #### recente
                sleep(1)
                pygui.keyDown('shift')
                foritab(2, 'tab')
                pygui.keyUp('shift')

                pygui.hotkey('enter')
                sleep(2)
                #####
                """ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LE_NF_CANCELADAS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
                self.start_walk_menu()
                print('right down enter enter')
                pygui.hotkey('right', 'down', 'enter', 'enter', interval=.5)
                sleep(2)
                print('NF canceled')

                nfcanceladas.action()
                # Cancela

                # p.hotkey('alt', 'tab')
                print('NF canceled FORA')

                sleep(1)
                # generate PDF relat. Prestados 51
                self.start_walk_menu()
                foritab(3, 'right')
                foritab(6, 'down')

                foritab(5, 'enter', interval=.25)
                # generate pdf
                sleep(7.5)
                # self.most_recent_file()
                print('estou contando com o Adobe, pois o PDF do G5 é aberto nele...')

                all_keys('ctrl', 'shift', 's')
                sleep(6)
                all_keys('enter')
                sleep(1)
                all_keys('ctrl', 'x')
                [(pygui.hotkey('alt', 'f4'), sleep(1)) for i in range(2)]
                path_file_temp_file = f"C:\\tmp\\{paste()}"
                sleep(2)
                filenewname = f'{self.client_path}\\Registro_ISS-{__cnpj}.pdf'
                while True:
                    try:
                        self.move_file(path_file_temp_file, filenewname)
                        print('finally')
                        break
                    except PermissionError:
                        sleep(5)
                        break

                """save in adobe"""

    def get_xml(self, cliente):
        b = self.files_get_anexos_v4(self.client_path, file_type='xml')
        b = b[0]
        b = b.split('\\')
        file = f'\\\\{b[-1]}'
        final = '\\'.join(b[:-1]) + file
        return final

    def formatar_cnpj(self, cnpj):
        cnpj = str(cnpj)
        if len(cnpj) < 14:
            cnpj = cnpj.zfill(11)
        cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
        print(cnpj)  # 123.456.789-00
        return cnpj

    def registronta(self, client, compt_file):
        """
        :param client: CLIENTE
        :param compt_file: compt_file
        :return: se tiver pdf que tem ISS e REGISTRO
        """
        registronta = False
        for f in self.files_get_anexos_v4(self.client_path, file_type='xml'):
            return True

        for f in self.files_get_anexos_v4(self.client_path, file_type='csv'):
            return True

        for f in self.files_get_anexos_v4(self.client_path, file_type='pdf'):
            if 'ISS' in f.upper():
                registronta = False
                break
            else:
                registronta = True
        return registronta

    def abre_programa(self, name, path=False):
        """
        :param name: path/to/nameProgram
        :param path: False => contmatic, True => any path
        :return: winleft+r open
        """

        if path is False:
            programa = contmatic_select_by_name(name)
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

    def activating_client(self, client_cnpj):
        x, y = 30, 60
        sleep(2)
        pygui.click(x, y)
        sleep(.7)
        # ativa empresa

        comp = self.first_and_last_day_compt(self.compt_used, '-')[1]
        pygui.write(comp)

        foritab(6, 'tab')  # PESQUISA
        pygui.hotkey('enter')
        sleep(1.5)
        all_keys('shift', 'tab')
        sleep(1)
        foritab(6, 'down')  # PESQUISAR POR CGC[CNPJ]
        sleep(.5)
        foritab(1, 'tab')  # Digite a frase contida no texto
        all_keys(client_cnpj)
        print(f'{client_cnpj}:^~30')

        all_keys('ctrl', 'down')
        foritab(2, 'enter', interval=1)
        sleep(1)

        pygui.hotkey('tab', 'enter', interval=1)
        # Caso apareça aquela mensagem chata

        # ##################################################### PAREUI DAQUI, SELECIONEI JÁ... MAS TESTAR...
        # sleep(20)

    def importa_nfs(self):
        sleep(2.5)
        w3 = pygui.getActiveWindow()
        pygui.click(w3.center, clicks=0)
        pygui.move(0, 150)
        pygui.click()

    def start_walk_menu(self):
        x, y = 30, 30
        pygui.click(x, y)
