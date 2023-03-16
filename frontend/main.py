from typing import List
import streamlit as st


def display_anexos_selector():
    __anexos = {anx: anx for anx in ['I', 'II', 'III', 'IV', 'V']}
    __anexos.update({'': "SEM_MOV"})
    _anexos = list(__anexos.keys())
    return st.sidebar.multiselect(
        "Filtrar quais anexos?", _anexos, _anexos, format_func=lambda opt: __anexos[opt])


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
