import streamlit as st
from utilities.queries import create_query, ask_koala

hide_streamlit_style = """ <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """
st.markdown(hide_streamlit_style, unsafe_allow_html = True)

if 'input_history' not in st.session_state:
    st.session_state.input_history = []
if 'output_history' not in st.session_state:
    st.session_state.output_history = []

#TODO: environment variables
st.title('TCM KoalaChat Founders')

#TODO: add user verification

#streamlit input text box
query = st.text_input('Enter your query:')
authorized_user = True
api_limit_reached = False
#TODO: add API limit checks that reset monthly and check if user is authorized
if authorized_user and not api_limit_reached:
    #TODO: add a loading until response is received
    if query:
        placeholder = st.empty()
        data = create_query(query, st.session_state.input_history, st.session_state.output_history, False)
        with st.spinner('Awaiting response...'):
            response = ask_koala(data)
        with placeholder.container():
            st.markdown('KoalaChat response:')
            st.write(response)
            st.session_state.input_history.append(query)
            st.session_state.output_history.append(response)
    else:
        pass
else:
    st.markdown('You have reached your API limit for the month. Please try again next month.')


#TODO: conneect to backend

#TODO: setup database