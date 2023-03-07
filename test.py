from frontend.main import *
import streamlit as st

_status_message = st.empty()
container_status_message = _status_message.container()


if st.button("Tenta ai vai OXI"):
    display_success_msg(
        container_status_message, "Status de declaração alterado!")
