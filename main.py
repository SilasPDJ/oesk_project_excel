# from __backend import Backend, PgdasDeclaracaoFull
# from __backend import COMPT, CONS, TOTAL_CLIENTES, IMPOSTOS_POSSIVEIS
# from __backend import consultar_compt, consultar_geral, getfieldnames
# from __backend import main_folder, main_file

# from __backend_v2 import Consulta_DB
import pandas as pd
from __backend_v2 import ComptGuiManager
from __backend_v2 import GIAS_GISS_COMPT, IMPOSTOS_POSSIVEIS, VENC_DAS
# usar class Rotinas
# from __backend import *

import tkinter as tk
from default.interact.autocomplete_entry import AutocompleteEntry
from default.sets import InitialSetting, get_compt
from pgdas_fiscal_oesk.gshopee_excel_values import ShopeeExcel
from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
from ttkwidgets import autocomplete as ttkac

from threading import Thread
import os
import sys
import subprocess
import clipboard
import json

entry_row = 1

COMPT = get_compt(int(sys.argv[1])) if len(
    sys.argv) > 1 else get_compt(-1)


def get_pendencias(CLI):
    report = os.path.join(CLI, 'DAS_EM_ABERTO.json')
    if os.path.exists(report):
        data = json.load(open(report, 'rb'))

        df_data = []
        for idx, item in enumerate(data):
            mes = list(item.keys())[0]
            numero_parcelamento = item[mes]
            valor = item['em_aberto'].replace(',', '.')

            df_data.append({
                'meses': mes,
                'numero_parcelamento': numero_parcelamento,
                'valor': valor
            })

        df = pd.DataFrame(df_data)

if __name__ == "__main__":
    # PgDasmailSender(compt=COMPT)
    html = get_pendencias(
        r'O:\OneDrive\_FISCAL-2021\2023\07-2023\Wagner Duque')
    html
