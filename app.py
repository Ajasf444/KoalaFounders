import streamlit as st


#TODO: environment variables
st.title('TCM KoalaChat Founders')

#TODO: add user verification

#streamlit input text box
query = st.text_input('Enter your query:')
#TODO: add API limit checks that reset monthly
print(query)

#TODO: conneect to backend

#TODO: setup database

st.markdown('Response')
st.text('hello, how are you?')
