import streamlit as st
from backend.models import SqlAchemyOrms
from backend.main import COMPT_ORM_OPERATIONS, EMPRESAS_ORM_OPERATIONS
from backend.database.db_interface import InitNewCompt


# Define a function to generate a Streamlit form for a given SQL ORM model
def generate_form(key, compt: str):
    """Gera o formulário para criar empresa, e já inicializa a competência dela

    Args:
        key (str): form_key
        compt (str): %m-%Y InitNewCompt
    """

    imposto_a_calcular = st.selectbox('Selecione o imposto Principal a Calcular',
                                      ['ICMS', 'ISS', 'SEM_MOV', 'LP'])
    # O correto seria realmente juntar os dois
    with st.form(key=key):
        # Generate a form field for each column in the model
        form_values = {}
        for column in SqlAchemyOrms.MainEmpresas.__table__.columns:
            column_name = column.name
            column_type = column.type.python_type

            if column_name != 'id':
                if column_type == str:
                    field_value = st.text_input(
                        column_name, )
                elif column_type == int:
                    field_value = st.number_input(
                        column_name, )
                elif column_type == bool:
                    field_value = st.checkbox(
                        column_name, )
                else:
                    field_value = st.text_input(
                        column_name, )

                form_values[column_name] = field_value

        # Add a submit button to the form
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            # TODO: validação do formulário
            # TODO: inicializar a competencia após adicionar aqui
            client_id = EMPRESAS_ORM_OPERATIONS.insert(form_values)
            if client_id:
                st.success('Inserido com sucesso')
                init_compt = InitNewCompt(compt)
                if init_compt.add_new_client(client_id, imposto_a_calcular):
                    st.success(
                        f"Competência {compt} para {form_values['razao_social']} criada")
                    st.warning(
                        'Anexos padrões ou sugeridos são: I p/ ICMS e III p/ ISS')
                else:
                    # st.error(
                    #     f"Competência para {form_values['razao_social']} já existente")
                    pass
                # TODO juntar o update com o create numa classe??
