import streamlit as st
from streamlit_option_menu import option_menu

PAGE_HOME = "Home"
PAGE_FORM_EMPRESAS = "Create/Update Empresas"
PAGE_UPDT_COMPT = "Update COMPT"
PAGE_ENVIADOS = "Clientes Enviados"


# 1. as sidebar menu

def display_menu():
    with st.sidebar:
        # selected = option_menu("Main Menu", ["Home", 'Settings'],
        #                        icons=['house', 'gear'], menu_icon="cast", default_index=1)
        # selected
        pass

        page = option_menu(None, [PAGE_HOME, PAGE_FORM_EMPRESAS, PAGE_UPDT_COMPT, PAGE_ENVIADOS],
                           icons=['house', 'cloud-upload',
                                  "list-task", None],
                           menu_icon="cast", default_index=0, orientation="horizontal",
                           styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "12px"},
            "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "black"},
        }
        )
        return page


display_menu()
