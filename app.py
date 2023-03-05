from backend.database.db_interface import DBInterface
import pandas as pd
import sqlalchemy as db
import streamlit as st
from backend.models import SqlAchemyOrms
from backend.database import MySqlInitConnection

# st.set_page_config(page_title='OESK Contábil')
st.set_page_config(page_title="My Streamlit App",
                   page_icon=":guardsman:", layout="wide")

# st.markdown("# OESK Contábil :flag-br:")

# st.sidebar.markdown("# Main page 🎈")


HOME = "Home"
UPDATE_EMPRESAS = "Update Empresas"
UPDATE_COMPT = "Update COMPT"

page = st.sidebar.selectbox(
    'Select a Page', [HOME, UPDATE_EMPRESAS, UPDATE_COMPT], 2)  # in this file
st.header(page)
st.sidebar.title(f"{page} :flag-br:")

conn_obj = MySqlInitConnection()
engine = conn_obj.engine
# Session = conn_obj.Session


db_interface = DBInterface(conn_obj)
EMPRESAS_ORM_OPERATIONS = db_interface.EmpresasOrmOperations(
    db_interface.conn_obj)
COMPT_ORM_OPERATIONS = db_interface.ComptOrmOperations(db_interface.conn_obj)

if page == HOME:
    # st.header("Welcome to the CRUD App!")
    st.write("Use the sidebar to navigate to other pages.")

# Update Empresas page
elif page == UPDATE_EMPRESAS:
    st.code("hi")

    cnpj = st.selectbox("Select a cnpj",
                        EMPRESAS_ORM_OPERATIONS.generate_df_v2(1, 2))
    # cnpj = st.selectbox("Select a cnpj", conn_obj.pd_sql_query_select(
    #     SqlAchemyOrms.MainEmpresas.cnpj,))
    empresa = EMPRESAS_ORM_OPERATIONS.find_by_cnpj(cnpj)
    razao_social = st.text_input("Razão Social", value=empresa.razao_social)

    df = EMPRESAS_ORM_OPERATIONS.generate_df_v2(1, 3)
    # for e, col in enumerate(df.columns):
    #     st.selectbox(f'select-{e}', df[col])

    if st.button("Update Empresas"):
        if not cnpj or not razao_social:
            st.warning("Please enter CNPJ and Razão Social.")
        else:
            updated = EMPRESAS_ORM_OPERATIONS.update_from_cnpj(
                cnpj, razao_social)
            if updated:
                st.success("Empresas updated successfully.")
            else:
                st.error("Failed to update Empresas.")

elif page == UPDATE_COMPT:
    # compt =

    # empresa = EMPRESAS_ORM_OPERATIONS.find_by_cnpj(cnpj)
    pass

# print(item.cnpj)


# print("oi")


# st.write(run_query(f'DESCRIBE {tables[0]};'))

# st.title("Cadastrar empresa")

# rows = run_query("SELECT * from usuario;")
# Print results.
# st.write(rows)


# Contents of ~/my_app/main_page.py
# Session.close()
