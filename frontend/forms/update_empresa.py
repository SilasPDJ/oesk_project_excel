import streamlit as st
import datetime
from backend.models import SqlAchemyOrms
from backend.main import COMPT_ORM_OPERATIONS, EMPRESAS_ORM_OPERATIONS


# Define a function to generate a Streamlit form for a given SQL ORM model
razao_social_dict = EMPRESAS_ORM_OPERATIONS.get_ids_dictonary()


def generate_form(key, compt: datetime.date):

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
                        if not form_values.get('status_ativo'):
                            if COMPT_ORM_OPERATIONS.delete_from_id_empresa(id_mapper, compt):
                                st.warning(f'Competência {compt.strftime("%m-%Y")} excluída')

            with cols[1]:
                if st.form_submit_button('EXCLUIR', type='primary'):
                    if st.form_submit_button('CONFIRMAR'):
                        if EMPRESAS_ORM_OPERATIONS.delete_from_id(id_mapper):
                            st.warning(
                                f'{form_values} foi EXCLUÍDO com sucesso')
