import pandas as pd
import sqlalchemy as db
import streamlit as st
from backend.models import SqlAchemyOrms
from backend.database import MySqlInitConnection

# st.set_page_config(page_title='OESK Contábil')
st.set_page_config(page_title="My Streamlit App",
                   page_icon=":guardsman:", layout="wide")

# st.title("Hello")
st.markdown("# OESK Contábil :flag-br:")

st.sidebar.title("OESK Contábil :flag-br:")
# st.sidebar.markdown("# Main page 🎈")


HOME = "Home"
UPDATE_EMPRESAS = "Update Empresas"
UPDATE_COMPT = "Update COMPT"

page = st.sidebar.selectbox(
    'Select a Page', [HOME, UPDATE_EMPRESAS, UPDATE_COMPT], 2)  # in this file


conn_obj = MySqlInitConnection()
engine = conn_obj.engine
Session = conn_obj.Session()


Empresas = SqlAchemyOrms.MainEmpresas

df = conn_obj.pd_sql_query_select(
    Empresas.cnpj,
    Empresas.razao_social,
    Empresas.cpf,)


def update_empresas(cnpj: str, razao_social: str):
    empresa = Session.query(
        SqlAchemyOrms.MainEmpresas).filter_by(cnpj=cnpj).first()
    if empresa:
        empresa.razao_social = razao_social
        Session.commit()
        return True


if page == HOME:
    st.title("Welcome to the CRUD App!")
    st.write("Use the sidebar to navigate to other pages.")

# Update Empresas page
elif page == UPDATE_EMPRESAS:
    st.title("Update Empresas")
    st.code("hi")

    cnpj = st.selectbox("Select a cnpj", conn_obj.pd_sql_query_select(
        Empresas.cnpj,))

    empresa = Session.query(
        SqlAchemyOrms.MainEmpresas).filter_by(cnpj=cnpj).first()
    razao_social = st.text_input("Razão Social", value=empresa.razao_social)

    if st.button("Update Empresas"):
        if not cnpj or not razao_social:
            st.warning("Please enter CNPJ and Razão Social.")
        else:
            updated = update_empresas(cnpj, razao_social)
            if updated:
                st.success("Empresas updated successfully.")
            else:
                st.error("Failed to update Empresas.")

elif page == UPDATE_COMPT:
    pass

# print(item.cnpj)


# print("oi")


# st.write(run_query(f'DESCRIBE {tables[0]};'))

# st.title("Cadastrar empresa")

# rows = run_query("SELECT * from usuario;")
# Print results.
# st.write(rows)


# Contents of ~/my_app/main_page.py
Session.close()
