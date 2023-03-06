from default.sets import get_compt, compt_to_date_obj
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
    columns = st.columns(2)
    # empresa = EMPRESAS_ORM_OPERATIONS.find_by_cnpj(cnpj)
    # razao_social = st.text_input("Razão Social", value=empresa.razao_social)

    # cnpj = st.selectbox("Select a cnpj",
    #                     EMPRESAS_ORM_OPERATIONS.generate_df_v2(1, 2))
    # ------------------------------------- VS --------------------------
    with columns[0]:
        razao_social = st.selectbox(
            "Selecione uma razão social", EMPRESAS_ORM_OPERATIONS.generate_df().iloc[:, 0])

        # EMPRESAS_ORM_OPERATIONS.generate_df().iloc[:, 1]
        cnpj = st.text_input(
            "Exibindo CNPJ", EMPRESAS_ORM_OPERATIONS.find_by_razao_social(razao_social).cnpj, disabled=True)

        _COMPT = st.date_input("Qual competencia?",
                               compt_to_date_obj(get_compt(-1)))

        other_values = COMPT_ORM_OPERATIONS.filter_by_cnpj_and_compt(
            cnpj, _COMPT)
        if other_values:
            # other_values.main_empresa_id
            # formatted_number = "${:,.2f}".format(my_number)

            other_values.declarado = st.text_input(
                "Está Declarado?", other_values.declarado)
            other_values.nf_saidas = st.text_input(
                "NF Saídas: ", other_values.nf_saidas)
            # TODO, mudar para nf_entradas
            other_values.nf_entradas = st.text_input(
                "NF Entradas:", other_values.nf_entradas)

            other_values.sem_retencao = st.number_input(
                "Sem retenção: ", other_values.sem_retencao or 0)

            other_values.com_retencao = st.number_input(
                "Com retenção: ", other_values.com_retencao or 0)
            other_values.valor_total = st.number_input(
                "Valor Total: ", other_values.valor_total or 0)
            other_values.anexo = st.text_input("Anexo: ", other_values.anexo)
            other_values.envio = st.text_input("Envio: ", other_values.envio)
            other_values.imposto_a_calcular = st.text_input("Inposto a calcular",
                                                            other_values.imposto_a_calcular, disabled=True)
            if st.button("Enviar"):
                updated = COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt(cnpj,
                                                                          other_values)
                if updated:
                    st.success("Empresas updated successfully.")
                else:
                    st.error("Failed to update Competencias.")

        # date = st.date_input("date", other_values.compt)

    # razao_social = st.text_input("Razão Social", value=empresa.razao_social)

    # empresa = EMPRESAS_ORM_OPERATIONS.filter_by_kwargs(cnpj="cnpj", razao_social="razao_social")
    # empresa.cnpj
    # COMPT_ORM_OPERATIONS.filter_by_kwargs()

# print(item.cnpj)


# print("oi")


# st.write(run_query(f'DESCRIBE {tables[0]};'))

# st.title("Cadastrar empresa")

# rows = run_query("SELECT * from usuario;")
# Print results.
# st.write(rows)


# Contents of ~/my_app/main_page.py
# Session.close()
