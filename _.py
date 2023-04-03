from frontend.update_empresa_form import generate_form
from backend.models import SqlAchemyOrms
import streamlit as st
from backend.main import db_interface

if __name__ == "__main__":
    EMPRESAS_ORM_OPERATIONS = db_interface.EmpresasOrmOperations(
        db_interface.conn_obj)

    form_values = generate_form()
    if form_values:
        id = form_values.pop('id')
        EMPRESAS_ORM_OPERATIONS.update_from_id(
            SqlAchemyOrms.MainEmpresas, id, form_values)
