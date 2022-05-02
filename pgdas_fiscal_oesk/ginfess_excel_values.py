# from default import NewSetPaths, ExcelToData
from default.sets.init_email import EmailExecutor
from default.sets import InitialSetting
from win32com import client as win32
import os
from time import sleep


class ExcelValuesPreensh(EmailExecutor, InitialSetting):

    def __init__(self, *args, main_xl_path, compt):
        # TODO: PQ TESTE e AQUI não funcionam da mesma forma?????????????
        # ---------- README: tentar fazer como o botão do F5 e
        #                    só Reabrir o main_gui quando terminar o excel
        #                    provavelmente é isso
        a = __r_social, __cnpj, __cpf, all_valores, = args
        self.main_xl_path = main_xl_path
        self.compt = compt

        self.client_path = self.files_pathit(__r_social.strip(), self.compt)
        self.excel_iss_file = os.path.join(
            self.client_path, f'{__cnpj}.xlsx')
        # wb = excel.Workbooks.Open(excel_iss_file)

        # create filter in Excel Worksheet
        # excel = win32.gencache.EnsureDispatch('Excel.Application')
        self.excel = excel = win32.Dispatch("Excel.Application")

        # excel can be visible or not
        excel.Visible = True
        # wb = self.excel.Workbooks.Open(self.main_xl_path)
        wb = self.excel.Workbooks.Open(main_xl_path)
        wb.Sheets(self.compt)
        excel.SendKeys("%cfsl")  # localizar agora
        excel.SendKeys(__r_social)
        excel.SendKeys("{ENTER}")
        excel.SendKeys("{ENTER}")
        sleep(.5)
        excel.SendKeys("{ESC}")
        # excel.Range("2:5").Select()
        range_atual = excel.Range(excel.Selection.Address)
        range_atual.Offset(1, 5).Select()
        # ESCREVE VALOR não retido----------------------

        range_atual.Offset(1, 6).Select()
        # ESCREVE VALOR retido

        print(excel.Selection.Address)
