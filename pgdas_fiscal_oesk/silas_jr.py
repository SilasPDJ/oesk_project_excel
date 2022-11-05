import pyautogui as pygui
from time import sleep

from default.interact import *
from default.sets import InitialSetting
from default.webdriver_utilities.wbs import WDShorcuts
from pgdas_fiscal_oesk.contimatic import Contimatic

# from pgdas_fiscal_oesk.relacao_nfs import iss_plan_exists, NfCanceled
from pyperclip import paste
# from default.webdriver_utilities import *
from win10toast import ToastNotifier

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


class JR(Contimatic):

    def __init__(self, *args, compt):
        __r_social, __cnpj, = args
        __client = __r_social

        self.compt_used = compt
        self.client_path = self.files_pathit(__client)

        registronta = self.registronta()
        print(__client)
        # input(registronta)
        print(__client)
        self.abre_ativa_programa('JR ')

        all_xls_inside = self.files_get_anexos_v4(
            self.client_path, file_type='xlsx')
        relacao_notas = all_xls_inside[0] if len(
            all_xls_inside) == 1 else IndexError()
        self.activating_client(self.formatar_cnpj(__cnpj))
        pygui.getActiveWindow().maximize()
        # Agora vai ser por cnpj...
        self.start_walk_menu()
        foritab(2, 'right')
        foritab(7, 'down')
        pygui.hotkey('right')
        foritab(7, 'down')
        pygui.hotkey('enter')

        # access ISS lançamento
        ToastNotifier().show_toast("Pressione F9 para ativar o próximo cliente", duration=10)
        press_key_b4('f9')
