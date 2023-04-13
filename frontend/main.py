from datetime import date
from . import st_page_config
from typing import List, Tuple
import streamlit as st
from backend.main import get_years_range, get_months_range_dict


def get_year_month_inputs() -> Tuple[st.selectbox, st.selectbox]:
    year_range, _date_now = get_years_range()
    months_dict = get_months_range_dict()
    cols = st.columns(2)
    with cols[1]:
        year = st.selectbox('ANO', year_range, list(
            year_range).index(_date_now.year))
    with cols[0]:
        month = st.selectbox('MES', months_dict,
                             format_func=lambda x: months_dict[x], index=_date_now.month-1)
    return year, month


def display_anexos_selector():
    anexos = ['I', 'II', 'III', 'IV', 'V']
    if not st.session_state.get('anexos_input'):
        __anexos = {anx: anx for anx in anexos}
        __anexos[''] = "SEM_MOV"
        st.session_state['anexos_input'] = __anexos

    st.sidebar.write("Anexos de somente:")
    cols = st.sidebar.columns(3)
    if cols[0].button("ICMS"):
        st.session_state['anexos_input'] = {anx: anx for anx in anexos[:2]}
    if cols[1].button("ISS"):
        st.session_state['anexos_input'] = {anx: anx for anx in anexos[2:]}
    if cols[2].button("Sem Mov"):
        st.session_state['anexos_input'] = {'': "SEM_MOV"}
    if st.session_state.get('anexos_input'):
        _anexos = list(st.session_state.get('anexos_input').keys())
        return st.sidebar.multiselect(
            "Filtrar quais anexos?", _anexos, _anexos, format_func=lambda opt: st.session_state['anexos_input'][opt])
    else:
        return ['']+anexos


def display_entradas_saidas_selector(opts: List):
    cols = st.columns(2)

    with cols[0]:
        nf_s = st.sidebar.selectbox("NF SAÍDAS", opts)
    with cols[1]:
        nf_e = st.sidebar.selectbox("NF ENTRADAS", opts)
    return nf_s, nf_e


def display_status_buttons(text: str, can_display: bool, container: st.container):
    with container:
        if can_display:
            st.markdown(
                '<div style="display: flex; align-items: center;">'
                '<div style="width: 10px; height: 10px; border-radius: 50%; background-color: green; margin-right: 5px;"></div>'
                f'<span style="font-weight: bold;">{text}</span>'
                '</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="display: flex; align-items: center;">'
                '<div style="width: 10px; height: 10px; border-radius: 50%; background-color: red; margin-right: 5px;"></div>'
                f'<span style="font-weight: bold;">{text}</span>'
                '</div>',
                unsafe_allow_html=True)


def add_label_to_stcode(label: str, align=None):
    """Add label to st.code

    Args:
        label (str): text to add as label
        align (str, optional): [right, left, center]. Defaults to None.
    """
    _divlabel = '<div data-testid="stMarkdownContainer" class="css-184tjsw e16nr0p34">'
    if align:
        st.write(
            f'{_divlabel}<p style="margin:0;text-align:{align}">{label}</p></div>', unsafe_allow_html=True)
    else:
        st.write(
            f'{_divlabel}<p style="margin:0;">{label}</p></div>', unsafe_allow_html=True)


def display_success_msg(main_container: st, msg: str):
    cols = main_container.columns(2)
    # ❎
    if main_container.button("❌"):
        main_container.empty()
    main_container.success(
        msg)


def page_empresa_forms(compt_as_date: date):
    # TODO: refatorar p/ classe
    from .forms.create_empresa import generate_form as create_form
    from .forms.update_empresa import generate_form as update_form

    cols = st.columns(2)
    with cols[0]:
        st.header('Selecione cliente para atualizar')
        update_form('update_form')

    with cols[1]:
        st.header('Crie um cliente novo')
        create_form('create_form', compt_as_date.strftime("%m-%Y"))
