import streamlit as st

# Define the initial values of your form fields
name = ""
email = ""
age = ""

# Render the first form
form1 = st.form("Form 1")
name = form1.text_input("Name")
email = form1.text_input("Email")
if form1.form_submit_button("Next"):
    # Render the second form if the "Next" button is clicked
    form2 = st.form("Form 2")
    age = form2.slider("Age", min_value=0, max_value=100, value=30)
    if form2.form_submit_button("Submit"):
        # Process the form data when the "Submit" button is clicked
        st.write(f"Name: {name}")
        st.write(f"Email: {email}")
        st.write(f"Age: {age}")
