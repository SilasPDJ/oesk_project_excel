import streamlit as st
from backend.models import SqlAchemyOrms
from backend.main import COMPT_ORM_OPERATIONS, EMPRESAS_ORM_OPERATIONS


# Define a function to generate a Streamlit form for a given SQL ORM model
razao_social_dict = EMPRESAS_ORM_OPERATIONS.get_ids_dictonary()


def generate_form(key):

    id_mapper = st.selectbox(
        'Razão Social', razao_social_dict, format_func=lambda x: razao_social_dict[x])
    _empresa = EMPRESAS_ORM_OPERATIONS.get_from_id(id_mapper)

    with st.form(key=key):
        buttons_container = st.container()
        # Generate a form field for each column in the model
        form_values = {}
        for column in SqlAchemyOrms.MainEmpresas.__table__.columns:
            column_name = column.name
            column_type = column.type.python_type

            if column_name != 'id':
                if column_type == str:
                    field_value = st.text_input(
                        column_name, getattr(_empresa, column_name))
                elif column_type == int:
                    field_value = st.number_input(
                        column_name, getattr(_empresa, column_name))
                elif column_type == bool:
                    field_value = st.checkbox(
                        column_name, getattr(_empresa, column_name))
                else:
                    field_value = st.text_input(
                        column_name, getattr(_empresa, column_name))
                form_values[column_name] = field_value

        imposto_a_calcular = st.selectbox('Selecione o imposto Principal a Calcular',
                                          ['ICMS', 'ISS', 'SEM_MOV', 'LP'])

        with buttons_container:
            cols = st.columns(2)
            with cols[0]:
                # Add a submit button to the form
                if st.form_submit_button(label='Atualizar'):
                    if EMPRESAS_ORM_OPERATIONS.update_from_id(id_mapper, form_values):
                        st.success('Atualizado com sucesso')
                        from backend.database.db_interface import InitNewCompt
                        init = InitNewCompt('03-2023')
                        if init.add_compt_tonew_client(getattr(_empresa, 'id'), imposto_a_calcular):
                            st.success(
                                f"Competência para {form_values['razao_social']} criada")
                        else:
                            st.error(
                                f"Competência para {form_values['razao_social']} já existente")

            with cols[1]:
                if st.form_submit_button('EXCLUIR', type='primary'):
                    if EMPRESAS_ORM_OPERATIONS.delete_from_id(id_mapper):
                        st.warning(f'{form_values} foi EXCLUÍDO com sucesso')
