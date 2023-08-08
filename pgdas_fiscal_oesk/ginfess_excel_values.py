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

    def __init__(self, *args, compt, shall_sleep=False):
        # __r_social, __cnpj, __cpf = args
        __r_social = args[0]
        self.compt = compt

        self.client_path = self.files_pathit(__r_social.strip(), self.compt)
        self.excel_reports_exported()
        

    @property
    def excel_reports_exported(self):
        emission_report = self.walget_searpath(
            'emission_report', os.path.dirname(self.client_path), 1)
        export_report = self.walget_searpath(
            '[export_report]', os.path.dirname(self.client_path), 1)

        reports = emission_report + export_report

        return reports


    def gethe3values(self):
        from openpyxl import Workbook, load_workbook

        wb = load_workbook(self.excel_reports_exported, data_only=True, )
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
