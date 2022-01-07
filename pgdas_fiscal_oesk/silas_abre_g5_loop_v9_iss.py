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
            super().__init__(self.client_path)
            meus_3_valores_atuais = tres_valores_faturados(self.client_path)
            # Se tem 3valores[excel], tem XML. Se não tem, não tem
            # (pois o xml e excel vem do ginfess_download)....

            print(__client)
            self.abre_ativa_programa('G5 ')  # vscode's cause

            if self.registronta() and "ok" != nf_out.lower() != "s":
                self.activating_client(self.formatar_cnpj(__cnpj))
                # - SEM IMPORTA NF
                # self.start_walk_menu()
                if tres_valores_faturados(self.client_path):
                    self.mk_nf_canceladas()
                sleep(1)
                # generate PDF relat. Prestados 56 #51
                self.start_walk_menu()
                foritab(3, 'right')
                foritab(6, 'down')
                # foritab(5, 'enter', interval=.25)
                foritab(1, 'enter', interval=.25)
                foritab(1, 'enter', interval=.25)
                foritab(5, 'down', interval=.25)
                foritab(4, 'enter', interval=.25)
                # generate pdf
                sleep(7.5)
                # self.most_recent_file()

                self.save_foxit(__cnpj)
                # F4
                # TODO: Salvar dentro do local de salvar relatorio, client_path

    def save_foxit(self, add2file):
        filename = f"Registro_ISS-{add2file}"
        all_keys('ctrl', 'shift', 's')
        sleep(.5)
        pygui.write(filename)
        sleep(.25)
        pygui.hotkey('f4')
        sleep(.5)
        pygui.hotkey('ctrl', 'a')
        pygui.hotkey('delete')
        pygui.write(self.client_path)
        pygui.hotkey('enter')
        sleep(1)
        pygui.hotkey('f4', 'enter', 'enter', interval=.5)
        winexplorer = pygui.getActiveWindow()
        winexplorer.moveRel(0, 100)
        pygui.click(clicks=0)
        pygui.hotkey('enter', 'enter', 'enter', 'enter', 'enter')
        sleep(2)
        pygui.hotkey('return', 'return', duration=1, interval=1)

        # pygui.hotkey('alt', 'f4')

    def mk_nf_canceladas(self):
        all_xls_inside = self.files_get_anexos_v4(
            self.client_path, file_type='xlsx')
        relacao_notas = all_xls_inside[0] if len(
            all_xls_inside) == 1 else IndexError()

        nfcanceladas = NfCanceled(relacao_notas)
        sleep(2)
        self.start_walk_menu()
        print('right down enter enter')
        pygui.hotkey('right', 'down', 'enter', 'enter', interval=.5)
        sleep(2)
        print('NF canceled')

        nfcanceladas.action()

    def __get_xml(self, cliente):
        b = self.files_get_anexos_v4(self.client_path, file_type='xml')
        b = b[0]
        b = b.split('\\')
        file = f'\\\\{b[-1]}'
        final = '\\'.join(b[:-1]) + file
        return final

    def start_walk_menu(self):
        x, y = 30, 30
        pygui.click(x, y)
