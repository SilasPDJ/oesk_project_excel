from ast import List
from typing import Tuple
import pandas as pd
import streamlit as st
import os
from decimal import Decimal
from default.sets import Initial, get_compt, compt_to_date_obj
from backend.database.db_interface import DBInterface
import pandas as pd
import sqlalchemy as db
import streamlit as st
from backend.models import SqlAchemyOrms
from backend.database import MySqlInitConnection
from datetime import datetime

conn_obj = MySqlInitConnection()
engine = conn_obj.engine
db_interface = DBInterface(conn_obj)
EMPRESAS_ORM_OPERATIONS = db_interface.EmpresasOrmOperations(
    db_interface.conn_obj)
COMPT_ORM_OPERATIONS = db_interface.ComptOrmOperations(db_interface.conn_obj)


# Set the path to the uploads directory
main_path = os.path.dirname(os.path.realpath(__file__))
UPLOADS_PATH = os.path.join(main_path, 'uploads')

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOADS_PATH):
    os.makedirs(UPLOADS_PATH)


def get_years_range() -> Tuple[range, datetime.now]:
    now_year = datetime.now().year
    return range(now_year-5, now_year+3), datetime.now()


def get_months_range_dict() -> dict:
    import locale
    import calendar
    locale.setlocale(locale.LC_TIME, '')
    months_dict = {'': ''}
    months_dict.update(
        {i: calendar.month_name[i].upper() for i in range(1, 13)})
    return months_dict


def permitir_ser_declarado(filtered_cnpjs, compt: datetime.date, is_permited):
    """Permite a realização de rotinas para os clientes, permissão fica como True

    Args:
        filtered_cnpjs (_type_): _description_
        compt (datetime.date): _description_

    Returns:
        _type_: _description_
    """
    # _COMPT_AS_DATE
    permitir_ok = False
    for cnpj in filtered_cnpjs:
        permitir_ok = COMPT_ORM_OPERATIONS.update_fieldict_from_cnpj_compt(
            cnpj, compt, {'pode_declarar': is_permited})
    if permitir_ok:
        return True
    else:
        return False


#  List[SqlAchemyOrms.MainEmpresas]

def obtem_dados_empresa() -> list:
    if not st.session_state.get('EMPRESAS_DADOS'):
        st.session_state['EMPRESAS_DADOS'] = EMPRESAS_ORM_OPERATIONS.query_all()
    return st.session_state['EMPRESAS_DADOS']


def execute_query():
    import json
    DATA_FILENAME = f"{UPLOADS_PATH}\\queries.json"
    if not os.path.exists(DATA_FILENAME):
        with open(DATA_FILENAME, mode='w', encoding='utf-8') as f:
            json.dump([], f)
    else:

        queries = json.load(open(DATA_FILENAME))
        for q in queries:
            if st.button(q):
                del st.session_state['query']
                st.session_state['query'] = st.text_input('write query', q)
    if not st.session_state.get('query'):
        st.session_state['query'] = st.text_input('write query')

    if st.button("Clique"):
        a = db_interface.search(st.session_state['query'])
        st.write(a)
    if st.button('Salvar'):
        with open(DATA_FILENAME, mode='a', encoding='utf-8') as f:
            json.dump([st.session_state['query']], f)
        del st.session_state['query']


def handle_uploaded_files():
    if len(os.listdir(UPLOADS_PATH)) < 1:
        data_files = st.sidebar.file_uploader(
            "MAIN_PATH", help="Arquivo principal do sistema", accept_multiple_files=False, label_visibility='collapsed')

        def main():
            # file_details = {"FileName": datafile.name, "FileType": datafile.type}
            # df = pd.read_csv(datafile)
            file_details = {"CAMINHO_PRINCIPAL": datafile.name}
            st.sidebar.write(file_details)

        if data_files is not None:
            if isinstance(data_files, list):
                for datafile in data_files:
                    main()
            else:
                datafile = data_files
                main()
    else:
        file = os.listdir(UPLOADS_PATH)[0]
        with open(file) as f:
            file_details = {"CAMINHO_PRINCIPAL": f.read()}
            st.sidebar.write(file_details)
