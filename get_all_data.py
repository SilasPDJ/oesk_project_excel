import pandas as pd
# from default.sets.pathmanager import Dirs

MAIN_FILE = r'C:\Users\Silas\OneDrive\_FISCAL-2021\__EXCEL POR COMPETENCIAS__\NOVA_FORMA_DE_DADOS.xlsm'

go_pandas = pd.read_excel(MAIN_FILE, sheet_name='')



def dale():
    for k, items in df.items():
        for e, val in enumerate(items.values()):
            # if e >= a_partir_atual:
            yield val


for d in dale():
    print(d)
# Dirs()
