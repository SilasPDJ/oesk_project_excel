# from default.interact import press_key_b4
# from pgdas_fiscal_oesk.ginfess_excel_values import ExcelValuesPreensh
# from pgdas_fiscal_oesk.rotina_dividas_v3 import dividas_ativas_complete as rotina_dividas
# from pgdas_fiscal_oesk.send_dividas import SendDividas
# from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
# from pgdas_fiscal_oesk.silas_abre_g5_loop_v10 import G5
# # from pgdas_fiscal_oesk.silas_abre_g5_loop_v9_iss import G5
# from pgdas_fiscal_oesk.gias import GIA

from backend.database import MySqlInitConnection
from backend.models import SqlAchemyOrms
from default.sets import InitialSetting
import pandas as pd
import sys
from backend.database.db_create import TablesCreationInDBFromPandas as __TablesCreationInDBFromPandas
from backend.database.db_interface import DBInterface
from default.sets import calc_date_compt_offset, get_compt, compt_to_date_obj
from default.sets import get_all_valores

# from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
# from pgdas_fiscal_oesk.rotina_pgdas_v3 import PgdasDeclaracao as PgdasDeclaracaoFull
# from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
# from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui
# from selenium.common.exceptions import UnexpectedAlertPresentException
# from pgdas_fiscal_oesk.silas_jr import JR
from pgdas_fiscal_oesk import Consulta_DB as Consulta_DB


COMPT = get_compt(int(sys.argv[1])) if len(sys.argv) > 1 else get_compt(-1)
GIAS_GISS_COMPT = get_compt(int(sys.argv[2])) if len(
    sys.argv) > 2 else get_compt(-2)
IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']
# TODO: GUI para impostos possiveis


class Rotinas:
    def _create_all_datas_using_sheets(self, compt_inicial='07-2021'):
        tables_creation_obj = __TablesCreationInDBFromPandas(
            COMPT, compt_inicial)
        tables_creation_obj.init_db_with_excel_data()

    def consultar_para_main_application():
        pass


class Backend:
    conn_obj = MySqlInitConnection()
    engine = conn_obj.engine
    # Session = conn_obj.Session

    db_interface = DBInterface(conn_obj)
    EMPRESAS_ORM_OPERATIONS = db_interface.EmpresasOrmOperations(
        db_interface.conn_obj)
    COMPT_ORM_OPERATIONS = db_interface.ComptOrmOperations(
        db_interface.conn_obj)

    EMPRESAS = EMPRESAS_ORM_OPERATIONS.generate_df()
    # clients_list = EMPRESAS.iloc[:, 0].to_list()

    # EMPRESAS_ORM_OPERATIONS.
