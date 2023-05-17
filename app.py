from frontend.main import *
from backend.main import *
from backend.main import BackUtils
from unicodedata import decimal

from streamlit_tags import st_tags, st_tags_sidebar
from frontend.menu import display_menu

# st.set_page_config(page_title='OESK Contábil')

# st.markdown("# OESK Contábil :flag-br:")

PAGE_HOME = "Home"
PAGE_FORM_EMPRESAS = "Create/Update Empresas"
PAGE_UPDT_COMPT = "Update COMPT"
PAGE_ENVIADOS = "Clientes Enviados"

# page = st.sidebar.selectbox(
#     'Select a Page', [PAGE_HOME, PAGE_FORM_EMPRESAS, PAGE_UPDT_COMPT, PAGE_ENVIADOS], 1)  # in this file
page = display_menu()

st.sidebar.markdown('**Anexos padrões: ICMS: I | ISS: III**')
st.sidebar.title(f"{page} :flag-br:")
_COMPT_AS_DATE = st.sidebar.date_input("Qual competencia?",
                                       compt_to_date_obj(get_compt(-1)))
back_utils = BackUtils(_COMPT_AS_DATE)

filtrar_quais_anexos = display_anexos_selector()
envio_multiselect = st.sidebar.multiselect(
    "Enviados: ", [True, False], [True, False])
if not envio_multiselect:
    envio_multiselect = [True, False]

_GERAL = back_utils.return_dados_gerais()
# CNPJS = GERAL['cnpj'].to_list()

GERAL_FILTER = _GERAL.loc[(_GERAL['anexo'].isin(
    filtrar_quais_anexos)) & _GERAL['envio'].isin(envio_multiselect)]
filtered_cnpjs = GERAL_FILTER['cnpj'].to_list()
GERAL = GERAL_FILTER
# filtrar_quais_anexos
# envio_multiselect


@ st.cache_data
def sum_values(v1, v2): return v1+v2


if page == PAGE_HOME:
    # st.header(page)
    st.header('Welcome to Home Page')
    # TODO^: adicionar e criar competencia
    div_cols = st.columns(2)
    with div_cols[1]:
        year_input, month_input = get_year_month_inputs()
    GERAL

elif page == PAGE_FORM_EMPRESAS:
    page_empresa_forms(_COMPT_AS_DATE)

elif page == PAGE_UPDT_COMPT:
    # corrigir LAYOUT coluna dos valores nret, sret para o TAB
    show_only_status = st.sidebar.checkbox("Mostrar somente status")

    title_columns = st.columns((1, 2, 1))
    with title_columns[0]:
        st.header(page)

    num_cols = 3 if not show_only_status else 5
    columns = st.columns(num_cols)
    # empresa = EMPRESAS_ORM_OPERATIONS.find_by_cnpj(cnpj)
    # razao_social = st.text_input("Razão Social", value=empresa.razao_social)

    # cnpj = st.selectbox("Select a cnpj",
    #                     EMPRESAS_ORM_OPERATIONS.generate_df_v2(1, 2))
    # ------------------------------------- VS --------------------------
    # EMPRESAS_ORM_OPERATIONS.generate_df_v2(1, 2)
    # -------------------------------------------------------------------
    ENTRADAS_SAIDAS_OPTIONS = [
        "", "NÃO HÁ", "OK", "OK0", "PENDENTE", "NAOPRCISA"]
    # filtro_opts_entradas, filtro_opts_saidas = display_entradas_saidas_selector(
    #     ENTRADAS_SAIDAS_OPTIONS)

    # ------------------------ Realiza as condições para exibir
    clientes_obj = conn_obj.pd_sql_query_select_fields(
        SqlAchemyOrms.MainEmpresas.razao_social)

    with title_columns[2]:
        st.write(f"Mostrando {len(filtered_cnpjs):02d} resultados")
        _status_message = st.empty()
        container_status_message = _status_message.container()

    if show_only_status or len(filtrar_quais_anexos) <= 3:
        # continuar

        with title_columns[1]:
            st.markdown("### Altera permissão de todos os selecionados")
            allow_cols = st.columns(5, gap='small')
            with allow_cols[0]:
                if st.button("COM Permissão"):
                    if back_utils.permitir_ser_declarado(filtered_cnpjs, True):
                        display_success_msg(container_status_message,
                                            'PERMISSÕES CONCEDIDAS')
            with allow_cols[1]:
                if st.button("SEM Permissão", type='primary'):
                    if back_utils.permitir_ser_declarado(filtered_cnpjs, True):
                        display_success_msg(container_status_message,
                                            'PERMISSÕES REMOVIDAS')
                    back_utils.permitir_ser_declarado(
                        filtered_cnpjs, _COMPT_AS_DATE, False)

    # --- Realiza a exibição baseado nas condições acima
    lista_para_atualizar = []
    # itterrows não serve no meu caso
    for i, dado in enumerate(GERAL.itertuples()):
        cnpj = dado.cnpj
        form_key = f"form_{i:04d}"
        other_values = COMPT_ORM_OPERATIONS.filter_by_cnpj_and_compt(
            cnpj, _COMPT_AS_DATE)
        # if other_values:
        razao_social = dado.razao_social

        submit_bts_cols = st.columns(3)
        with columns[i % num_cols]:
            with st.form(key=form_key):

                submit_bts_cols = st.columns(3, gap='small')
                with submit_bts_cols[0]:
                    if st.form_submit_button("Status"):
                        other_values.declarado = not other_values.declarado
                        updated = COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt(
                            cnpj, other_values, ['declarado'])
                        if updated:
                            display_success_msg(
                                container_status_message, "Status de declaração alterado!")
                        else:
                            _status_message.error("Falha em conexão")
                with submit_bts_cols[1]:
                    if st.form_submit_button("Envio"):
                        other_values.envio = not other_values.envio
                        updated = COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt(
                            cnpj, other_values, ['envio'])
                        if updated:
                            display_success_msg(
                                container_status_message, "Status de envio alterado!")
                        else:
                            _status_message.error("Falha em conexão")
                with submit_bts_cols[2]:
                    # TODO pertmir todos... da seleção
                    if st.form_submit_button("Permit"):
                        other_values.pode_declarar = not other_values.pode_declarar
                        updated = COMPT_ORM_OPERATIONS.update_from_cnpj_and_compt(
                            cnpj, other_values, ['pode_declarar'])
                        if updated:
                            display_success_msg(
                                container_status_message, "Autorização alterada!")
                        else:
                            _status_message.error("Falha em conexão")

                status_cols = st.columns(2)
                with status_cols[0]:
                    display_status_buttons(
                        "Declarado", other_values.declarado, st.container())
                    display_status_buttons(
                        "Envio", other_values.envio, st.container())
                    display_status_buttons(
                        "Autorizado", other_values.pode_declarar, st.container())
                with status_cols[1]:
                    # add_label_to_stcode("CNPJ: ", align="center")
                    # st.code(cnpj)
                    st.text_input("CNPJ", cnpj)
                # with div_is_sent:
                st.code(razao_social)
                # other_values.main_empresa_id
                # formatted_number = "${:,.2f}".format(my_number)
                if not show_only_status:
                    other_values.sem_retencao = float(
                        other_values.sem_retencao)
                    other_values.com_retencao = float(
                        other_values.com_retencao)
                    other_values.valor_total = float(
                        other_values.valor_total)
                    inner_cols_values = st.columns(2)
                    with inner_cols_values[0]:
                        other_values.sem_retencao = st.number_input(
                            "Sem retenção: ", 0., 9999999., other_values.sem_retencao, 100.00)
                    with inner_cols_values[1]:
                        other_values.com_retencao = st.number_input(
                            "Com retenção: ", 0., 9999999., other_values.com_retencao, 100.00)

                    valor_total = sum_values(
                        other_values.sem_retencao, other_values.com_retencao) or other_values.valor_total
                    # other_values.valor_total = st.number_input(
                    #     "Valor Total: ", 0., 9999999., valor_total, 100.00, disabled=True)
                    other_values.valor_total = valor_total
                    with inner_cols_values[1]:
                        add_label_to_stcode("Valor Total")
                        st.code("R${:,.2f}".format(valor_total).replace(
                            ",", "X").replace(".", ",").replace("X", "."))
                    with inner_cols_values[0]:
                        _anexo = other_values.anexo
                        other_values.anexo = st.text_input(
                            "Anexo: ", other_values.anexo)
                    other_values.imposto_a_calcular = "SEM_MOV" if _anexo == "" else "ICMS" if _anexo in [
                        'I', 'II'] else "ISS"
                    # inner_cols_nfs = st.columns(2)
                    # with inner_cols_nfs[0]:
                    #     other_values.nf_saidas = st.selectbox(
                    #         "NF Saídas", ENTRADAS_SAIDAS_OPTIONS, ENTRADAS_SAIDAS_OPTIONS.index(other_values.nf_saidas.upper()))
                    # with inner_cols_nfs[1]:
                    #     other_values.nf_entradas = st.selectbox(
                    #         "NF Entradas:", ENTRADAS_SAIDAS_OPTIONS, ENTRADAS_SAIDAS_OPTIONS.index(other_values.nf_entradas.upper()))
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

elif page == PAGE_ENVIADOS:
    # CNPJS = EMPRESAS_ORM_OPERATIONS.query_all()
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

        cols = st.columns([1, 1, 1, 2, 1])
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
        with cols[4]:
            if other.nf_saidas.upper() == 'OK':
                st.write('nf_saídas: ✅')
            else:
                st.write('nf_saídas: ❌')

# print(item.cnpj)


# print("oi")


# st.write(run_query(f'DESCRIBE {tables[0]};'))

# st.title("Cadastrar empresa")

# rows = run_query("SELECT * from usuario;")
# Print results.
# st.write(rows)


# Contents of ~/my_app/main_page.py
# Session.close()
