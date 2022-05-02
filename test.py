import os
from time import sleep
import pandas as pd
from pathlib import Path
import win32com.client as win32

# change to the path to the Excel file
f_path = "O:\OneDrive\_FISCAL-2021\__EXCEL POR COMPETENCIAS__"
f_name = 'DALDALE.xlsm'  # Excel File name
filename = os.path.join(f_path, f_name)
sheetname = '04-2022'  # change to the name of the worksheet

# create Excel object
excel = win32.gencache.EnsureDispatch('Excel.Application')
# excel can be visible or not
excel.Visible = True
# open Excel Workbook
wb = excel.Workbooks.Open(filename)
# create filter in Excel Worksheet
wb.Sheets(sheetname)


excel.SendKeys("%cfsl")  # localizar agora
excel.SendKeys("M Monteiro Intermediacao de Negocios Eireli")
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
