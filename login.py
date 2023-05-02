import streamlit as st
import streamlit_authenticator as stauth
import utilities.database as db
import time

# Bring up Emoji window by pressing Windows key + .

# get user credentials


def startup():
    credentials = db.get_credentials()
    authenticator = stauth.Authenticate(
        credentials=credentials, cookie_name='KoalaChatFounders', key='KCF_123')
    st.session_state['authenticator'] = authenticator


def display_UI(authenticator):
    name, authentication_status, username = authenticator.login(
        'Login', 'main')

def layer():
    # run the login section
    if 'authenticator' not in st.session_state:
        startup()

    authenticator = st.session_state['authenticator']

    if not st.session_state['authentication_status']:
        display_UI(authenticator)

    username = st.session_state['username']
    name = st.session_state['name']
    authentication_status = st.session_state['authentication_status']
    return authenticator, username, name, authentication_status