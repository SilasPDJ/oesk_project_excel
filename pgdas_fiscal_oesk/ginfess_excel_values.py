# from default import NewSetPaths, ExcelToData
from default.sets.init_email import EmailExecutor
from default.sets import InitialSetting
from win32com import client as win32
import os
from time import sleep
import pandas as pd

# _wb_exists = self.walget_searpath
# f'{__r_social[:__r_social.find(" ")]}_{__cnpj}.xlsx'


class ExcelValuesPreensh(EmailExecutor, InitialSetting):
    shall_sleep = True

    def __init__(self, *args, main_xl_path, compt, shall_sleep=False):
        # TODO: PQ TESTE e AQUI não funcionam da mesma forma?????????????
        # ---------- README: tentar fazer como o botão do F5 e
        #                    só Reabrir o main_gui quando terminar o excel
        #                    provavelmente é isso
        a = __r_social, __cnpj, __cpf = args
        self.main_xl_path = main_xl_path
        self.compt = compt

        self.client_path = self.files_pathit(__r_social.strip(), self.compt)
        # self.excel_iss_file = os.path.join(
        #     self.client_path, f'{__cnpj}.xlsx')
        _wb_exists = self.walget_searpath(f'{__r_social[:__r_social.find(" ")]}_{__cnpj}.xlsx',
                                          self.client_path, 2)
        self.excel_iss_file = dict(
            enumerate(_wb_exists)).get(0, False)

        self.excel = excel = win32.Dispatch("Excel.Application")
        excel.Visible = True
        wb = self.excel.Workbooks.Open(main_xl_path)
        wb.Sheets(self.compt)
        if shall_sleep:
            sleep(2.5)
        if _wb_exists:
            v_clifolder_tot, v_clifolder_ret, v_clifolder_nret = self.gethe3values()
            # excel can be visible or not
            # wb = self.excel.Workbooks.Open(self.main_xl_path)
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
            excel.ActiveCell.FormulaR1C1 = v_clifolder_nret
            range_atual.Offset(1, 6).Select()
            # ESCREVE VALOR retido
            excel.ActiveCell.FormulaR1C1 = v_clifolder_ret

            print(excel.Selection.Address)

    def gethe3values(self):
        from openpyxl import Workbook, load_workbook

        wb = load_workbook(self.excel_iss_file, data_only=True, )
        ws = wb.active
        column_name = 'Valor'
        valores = []
        for column_cell in ws.iter_cols(1, ws.max_column):
            # ws.column_dimensions['C'].hidden = False
            if column_cell[0].value == column_name:
                for data in column_cell[-3:]:
                    valores.append(float(data.internal_value or 0))
                    # data.value

        return valores
