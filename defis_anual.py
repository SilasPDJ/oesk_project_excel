from pgdas_fiscal_oesk.defis_utils.visualizaTicket_gerar_socios import main as generate_excel_from_jucesp_tickets
# from pgdas_fiscal_oesk.defis_utils.jucespVisualizaTicket_v3 import VisualizaTicket as Jucesp3
from pgdas_fiscal_oesk.defis_utils.jucesp_consulta_passo_1 import ConsultaJucesp
from pgdas_fiscal_oesk.defis import Defis
from datetime import date
from datetime import datetime as dt


def diff_month(_from, now=None):
    if now is None:
        now = date(dt.now().year, dt.now().month, dt.now().day)
    return (now.year - _from.year) * 12 + now.month - _from.month


# _from = date(2019, 2, 1)
# # assert diff_month(now, _from) == 1
# print(diff_month(_from))



# ------------ etapas ...
# ConsultaJucesp()
# generate_excel_from_jucesp_tickets()  # method
Defis()
