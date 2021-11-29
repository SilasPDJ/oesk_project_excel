import pyautogui as pygui
from time import sleep

from default.interact import *
# from default.sets import InitialSetting
from default.webdriver_utilities.wbs import WDShorcuts

# from pgdas_fiscal_oesk.contimatic import InitialSetting
from pgdas_fiscal_oesk.contimatic import Contimatic

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


class G5(Contimatic):

    def __init__(self, *args, compt):
        __r_social, __cnpj, __cpf, __cod_simples, __valor_competencia, imposto_a_calcular, nf_out = args
        __client = __r_social
        if imposto_a_calcular == 'ISS':
            self.compt_used = compt
            self.client_path = self.files_pathit(__client)

            meus_3_valores_atuais = tres_valores_faturados(self.client_path)
            # Se tem 3valores[excel], tem XML. Se não tem, não tem
            # (pois o xml e excel vem do ginfess_download)....

            registronta = self.registronta()
            print(__client)
            self.abre_ativa_programa('G5')
            if meus_3_valores_atuais and registronta and "ok" != nf_out.lower() != "s":
                self.activating_client(self.formatar_cnpj(__cnpj))
                # self.start_walk_menu()

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
                input('teste salve')

    def get_xml(self, cliente):
        b = self.files_get_anexos_v4(self.client_path, file_type='xml')
        b = b[0]
        b = b.split('\\')
        file = f'\\\\{b[-1]}'
        final = '\\'.join(b[:-1]) + file
        return final

    def importa_nfs(self):
        sleep(2.5)
        w3 = pygui.getActiveWindow()
        pygui.click(w3.center, clicks=0)
        pygui.move(0, 150)
        pygui.click()

    def start_walk_menu(self):
        x, y = 30, 30
        pygui.click(x, y)
