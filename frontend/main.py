import streamlit as st


def display_anexos_selector():
    __anexos = {anx: anx for anx in ['I', 'II', 'III', 'IV', 'V']}
    __anexos.update({'': "SEM_MOV"})
    _anexos = list(__anexos.keys())
    return st.sidebar.multiselect(
        "Filtrar quais anexos?", _anexos, _anexos, format_func=lambda opt: __anexos[opt])


def display_clientes_sidebar_selector(arg):
    return st.sidebar.multiselect("Filtrar quais clientes? ", arg)


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


def display_success_msg(main_container: st, msg: str):
    cols = main_container.columns(2)
    # ❎
    if main_container.button("❌"):
        main_container.empty()
    main_container.success(
        msg)
