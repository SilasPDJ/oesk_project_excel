from backend.main import *
from frontend.main import *

from decimal import Decimal
from default.sets import Initial, get_compt, compt_to_date_obj
from backend.database.db_interface import DBInterface
import pandas as pd
import sqlalchemy as db
import streamlit as st
from backend.models import SqlAchemyOrms
from backend.database import MySqlInitConnection
from streamlit_tags import st_tags, st_tags_sidebar


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

st.sidebar.title(f"{page} :flag-br:")
_COMPT_AS_DATE = st.sidebar.date_input("Qual competencia?",
                                       compt_to_date_obj(get_compt(-1)))


filtrar_quais_anexos = display_anexos_selector()


MAIN_PATH = handle_uploaded_files()

conn_obj = MySqlInitConnection()
engine = conn_obj.engine
# Session = conn_obj.Session


db_interface = DBInterface(conn_obj)
EMPRESAS_ORM_OPERATIONS = db_interface.EmpresasOrmOperations(
    db_interface.conn_obj)
COMPT_ORM_OPERATIONS = db_interface.ComptOrmOperations(db_interface.conn_obj)


@st.cache_data
def sum_values(v1, v2):
    return v1+v2


if page == HOME:
    st.header(page)
    # st.header("Welcome to the CRUD App!")
    st.write("Use the sidebar to navigate to other pages.")

# Update Empresas page
elif page == UPDATE_EMPRESAS:
    st.header(page)
    st.code("hi")

    cnpj = st.selectbox("Select a cnpj",
                        EMPRESAS_ORM_OPERATIONS.generate_df_v2(2, 3))
    # cnpj = st.selectbox("Select a cnpj", conn_obj.pd_sql_query_select_fields(
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
    title_columns = st.columns(2)
    with title_columns[0]:
        st.header(page)
    with title_columns[1]:
        _status_message = st.empty()
        container_status_message = _status_message.container()

    num_cols = 4
    columns = st.columns(num_cols)
    # empresa = EMPRESAS_ORM_OPERATIONS.find_by_cnpj(cnpj)
    # razao_social = st.text_input("Razão Social", value=empresa.razao_social)

    # cnpj = st.selectbox("Select a cnpj",
    #                     EMPRESAS_ORM_OPERATIONS.generate_df_v2(1, 2))
    # ------------------------------------- VS --------------------------
    # EMPRESAS_ORM_OPERATIONS.generate_df_v2(1, 2)
    # -------------------------------------------------------------------
    # ------------------------ Realiza as condições para exibir
    cnpjs = EMPRESAS_ORM_OPERATIONS.generate_df_v2().iloc[:, 2]

    clientes_obj = conn_obj.pd_sql_query_select_fields(
        SqlAchemyOrms.MainEmpresas.razao_social)
    # filtrar_quais_clientes = display_clientes_sidebar_selector()
    filtered_cnpjs = []
    for i, cnpj, in enumerate(cnpjs[1:]):
        form_key = f"form_{i:04d}"

        # dados = EMPRESAS_ORM_OPERATIONS.find_by_cnpj(cnpj)

        other_values = COMPT_ORM_OPERATIONS.filter_by_cnpj_and_compt(
            cnpj, _COMPT_AS_DATE)
        if other_values:
            #  if EMPRESAS_ORM_OPERATIONS.filter_by_kwargs(
            #                         id=other_values.main_empresa_id).razao_social in filtrar_quais_clientes:
            if other_values.anexo in filtrar_quais_anexos:
                filtered_cnpjs.append(cnpj)

    # --- Realiza a exibição baseado nas condições acima
    for i, cnpj in enumerate(filtered_cnpjs):

        form_key = f"form_{i:04d}"
        dados = EMPRESAS_ORM_OPERATIONS.find_by_cnpj(cnpj)
        other_values = COMPT_ORM_OPERATIONS.filter_by_cnpj_and_compt(
            cnpj, _COMPT_AS_DATE)
        # if other_values:
        razao_social = dados.razao_social
        with columns[i % num_cols]:
            with st.form(key=form_key):
                if st.form_submit_button("Alterar Status"):
                    other_values.declarado = not other_values.declarado
                    updated = COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt(
                        cnpj, other_values, ['declarado'])
                    if updated:
                        display_success_msg(
                            container_status_message, "Status de declaração alterado!")
                    else:
                        _status_message.error("Falha em conexão")
                # with div_container:
                # display_status_buttons()
                # with div_esta_declarado:
                display_status_buttons(
                    "Declarado", other_values.declarado, st.container())
                display_status_buttons(
                    "Envio", other_values.envio, st.container())

                # with div_is_sent:
                st.code(razao_social)
                st.code(cnpj)
                # other_values.main_empresa_id
                # formatted_number = "${:,.2f}".format(my_number)
                other_values.sem_retencao = float(
                    other_values.sem_retencao)
                other_values.com_retencao = float(
                    other_values.com_retencao)
                other_values.valor_total = float(
                    other_values.valor_total)
                beta_cols = st.columns(2)
                with beta_cols[0]:
                    other_values.sem_retencao = st.number_input(
                        "Sem retenção: ", 0., 9999999., other_values.sem_retencao, 100.00)
                with beta_cols[1]:
                    other_values.com_retencao = st.number_input(
                        "Com retenção: ", 0., 9999999., other_values.com_retencao, 100.00)

                valor_total = sum_values(
                    other_values.sem_retencao, other_values.com_retencao) or other_values.valor_total
                # other_values.valor_total = st.number_input(
                #     "Valor Total: ", 0., 9999999., valor_total, 100.00, disabled=True)
                other_values.valor_total = valor_total
                st.code("R${:,.2f}".format(valor_total).replace(
                    ",", "X").replace(".", ",").replace("X", "."))

                _anexo = other_values.anexo
                other_values.anexo = st.text_input(
                    "Anexo: ", other_values.anexo)
                other_values.imposto_a_calcular = "SEM_MOV" if _anexo == "" else "ICMS" if _anexo in [
                    'I', 'II'] else "ISS"
                other_values.nf_saidas = st.text_input(
                    "NF Saídas: ", other_values.nf_saidas)
                other_values.nf_entradas = st.text_input(
                    "NF Entradas:", other_values.nf_entradas)

                # other_values.envio = st.text_input(
                #     "Envio: ", other_values.envio)
                # other_values.imposto_a_calcular = st.text_input("Inposto a calcular",
                #                                                 other_values.imposto_a_calcular, disabled=True)
                confirm_changes = True
                if confirm_changes:
                    if st.form_submit_button():
                        updated = COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt(cnpj,
                                                                                  other_values)
                        if updated:
                            display_success_msg(
                                container_status_message, "Status de declaração alterado!")
                        else:
                            _status_message.error(
                                "Failed to update Competencias.")
                # cnpj = st.text_input(
                #     "Exibindo CNPJ", EMPRESAS_ORM_OPERATIONS.find_by_razao_social(razao_social).cnpj, disabled=True)

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
