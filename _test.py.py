import streamlit as st

from streamlit_tags import st_tags, st_tags_sidebar
keywords = st_tags(
    label='# Enter Keywords:',
    text='Press enter to add more',
    value=['Zero', 'One', 'Two'],
    suggestions=['five', 'six', 'seven',
                 'eight', 'nine', 'three',
                 'eleven', 'ten', 'four'],
    maxtags=4,
    key='1')

keyword = st_tags_sidebar(
    label='# Enter Keywords:',
    text='Press enter to add more',
    value=['Zero', 'One', 'Two'],
    suggestions=['five', 'six', 'seven',
                 'eight', 'nine', 'three',
                 'eleven', 'ten', 'four'],
    maxtags=4,
    key='2')

# Define the CSS style for the form
# css = """
#     .streamlitTeste {
#         border: 2px solid green;
#         border-radius: 5px;
#         padding: 10px;
#     }
# """

# # Add the form to the app with the CSS class
# style(css)
# with tag("div", class_="streamlitTeste"):
#     input_(type="text", label="Enter your name")
#     button(type="submit", label="Submit")
