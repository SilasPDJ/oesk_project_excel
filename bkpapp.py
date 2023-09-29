from frontend.main import *
from backend.main import *
from unicodedata import decimal

from streamlit_tags import st_tags, st_tags_sidebar


# st.set_page_config(page_title='OESK Contábil')

# st.markdown("# OESK Contábil :flag-br:")

PAGE_HOME = "Home"
PAGE_FORM_EMPRESAS = "Create/Update Empresas"
PAGE_ENVIADOS = "Clientes Enviados"

page = st.sidebar.selectbox(
    'Select a Page', [PAGE_HOME, PAGE_FORM_EMPRESAS, PAGE_ENVIADOS], 1)  # in this file
st.sidebar.markdown('**Anexos padrões: ICMS: I | ISS: III**')
st.sidebar.title(f"{page} :flag-br:")
_COMPT_AS_DATE = st.sidebar.date_input("Qual competencia?",
                                       compt_to_date_obj(get_compt(-1)))


filtrar_quais_anexos = display_anexos_selector()
# TODO: em vez de por anexos... por imposto_a_Calcular??????


@st.cache_data
def sum_values(v1, v2):
    return v1+v2


if page == PAGE_HOME:
    # st.header(page)
    st.header('Welcome to Home Page')
    # TODO^: adicionar e criar competencia
    div_cols = st.columns(2)
    with div_cols[1]:
        year_input, month_input = get_year_month_inputs()

elif page == PAGE_FORM_EMPRESAS:
    page_empresa_forms(_COMPT_AS_DATE)

elif page == PAGE_ENVIADOS:
    CNPJS = EMPRESAS_ORM_OPERATIONS.generate_df_v2().iloc[:, 2]
    clientes_obj = conn_obj.pd_sql_query_select_fields(
        SqlAchemyOrms.MainEmpresas.razao_social)
    CNPJS = EMPRESAS_ORM_OPERATIONS.query_all()
    other_values = COMPT_ORM_OPERATIONS.filter_all_by_compt(
        _COMPT_AS_DATE)

    other_values = COMPT_ORM_OPERATIONS.filter_all_by_compt_order_by(
        _COMPT_AS_DATE, ['envio asc'])

    other_values = COMPT_ORM_OPERATIONS.filter_all_by_compt_order_by(
        _COMPT_AS_DATE, ['envio asc'])

    for other in other_values:
        dados = EMPRESAS_ORM_OPERATIONS.filter_by_kwargs(
            id=other.main_empresa_id)
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
# print(item.cnpj)


# print("oi")


# st.write(run_query(f'DESCRIBE {tables[0]};'))

# st.title("Cadastrar empresa")

# rows = run_query("SELECT * from usuario;")
# Print results.
# st.write(rows)


# Contents of ~/my_app/main_page.py
# Session.close()
