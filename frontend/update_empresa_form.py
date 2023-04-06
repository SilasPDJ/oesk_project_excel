import streamlit as st
from backend.models import SqlAchemyOrms
from backend.main import COMPT_ORM_OPERATIONS, EMPRESAS_ORM_OPERATIONS


# Define a function to generate a Streamlit form for a given SQL ORM model
def generate_form():
    razao_social_dict = EMPRESAS_ORM_OPERATIONS.get_ids_dictonary()

    id_mapper = st.selectbox(
        'Razão Social', razao_social_dict, format_func=lambda x: razao_social_dict[x])
    _empresa = EMPRESAS_ORM_OPERATIONS.get_from_id(id_mapper)

    with st.form(key='my_form'):
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

        # Add a submit button to the form
        submit_button = st.form_submit_button(label='Submit')

        # Return the form field values as a dictionary when the form is submitted
        if submit_button:
            EMPRESAS_ORM_OPERATIONS.update_from_id(id_mapper)

    # TODO: adicionar empresa
