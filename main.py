# from __backend import Backend, PgdasDeclaracaoFull
# from __backend import COMPT, CONS, TOTAL_CLIENTES, IMPOSTOS_POSSIVEIS
# from __backend import consultar_compt, consultar_geral, getfieldnames
# from __backend import main_folder, main_file

# from __backend_v2 import Consulta_DB
from __backend_v2 import ComptGuiManager
from __backend_v2 import GIAS_GISS_COMPT, IMPOSTOS_POSSIVEIS, VENC_DAS
# usar class Rotinas
# from __backend import *

import tkinter as tk
from default.interact.autocomplete_entry import AutocompleteEntry
from default.sets import InitialSetting, get_compt
from pgdas_fiscal_oesk.gshopee_excel_values import ShopeeExcel
from ttkwidgets import autocomplete as ttkac

from threading import Thread
import os
import sys
import subprocess
import clipboard

entry_row = 1

COMPT = get_compt(int(sys.argv[1])) if len(
    sys.argv) > 1 else get_compt(-1)


if __name__ == "__main__":
    ShopeeExcel(compt=COMPT)
