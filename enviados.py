import streamlit as st
from backend.main import *
from frontend.main import *
# TODO: Conectar com app.py
from decimal import Decimal
from default.sets import Initial, get_compt, compt_to_date_obj
from backend.database.db_interface import DBInterface
import pandas as pd
import sqlalchemy as db
import streamlit as st
from backend.models import SqlAchemyOrms
from backend.database import MySqlInitConnection
from streamlit_tags import st_tags, st_tags_sidebar
_COMPT_AS_DATE = st.sidebar.date_input("Qual competencia?",
                                       compt_to_date_obj(get_compt(-1)))

conn_obj = MySqlInitConnection()
engine = conn_obj.engine
# Session = conn_obj.Session


db_interface = DBInterface(conn_obj)
EMPRESAS_ORM_OPERATIONS = db_interface.EmpresasOrmOperations(
    db_interface.conn_obj)
COMPT_ORM_OPERATIONS = db_interface.ComptOrmOperations(db_interface.conn_obj)


CNPJS = EMPRESAS_ORM_OPERATIONS.generate_df_v2().iloc[:, 2]
clientes_obj = conn_obj.pd_sql_query_select_fields(
    SqlAchemyOrms.MainEmpresas.razao_social)
CNPJS = EMPRESAS_ORM_OPERATIONS.query_all()
other_values = COMPT_ORM_OPERATIONS.filter_all_by_compt(
    _COMPT_AS_DATE)

# for i, dados in enumerate(CNPJS[1:]):

#     cnpj = dados.cnpj
#     form_key = f"form_{i:04d}"

#     # dados = EMPRESAS_ORM_OPERATIONS.find_by_cnpj(cnpj)
#     # ✅
#     other_values = COMPT_ORM_OPERATIONS.filter_by_cnpj_and_compt(
#         cnpj, _COMPT_AS_DATE)

#     cols = st.columns(2)
#     with cols[0]:
#         st.write(dados.razao_social)
#     with cols[1]:
#         if other_values.envio:
#             st.write("ENVIO: ✅")
#         else:
#             st.write("ENVIO: ❌")
other_values = COMPT_ORM_OPERATIONS.filter_all_by_compt_order_by(
    _COMPT_AS_DATE, ['envio asc'])

other_values = COMPT_ORM_OPERATIONS.filter_all_by_compt_order_by(
    _COMPT_AS_DATE, ['envio asc'])

for other in other_values:
    dados = EMPRESAS_ORM_OPERATIONS.filter_by_kwargs(id=other.main_empresa_id)
    cnpj = dados.cnpj

    cols = st.columns([1, 1, 1, 2])
    with cols[3]:
        st.write(dados.razao_social)
    with cols[1]:
        if other.declarado:
            st.write("DECLARADO: ✅")
        else:
            st.write("DECLARADO: ❌")
    with cols[2]:
        if other.envio:
            st.write("ENVIO: ✅")
        else:
            st.write("ENVIO: ❌")
    with cols[0]:
        st.code(other.valor_total)
