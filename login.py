import streamlit as st
import streamlit_authenticator as stauth
import utilities.database as db
import time

# Bring up Emoji window by pressing Windows key + .

# get user credentials


def login_startup():
    credentials = db.get_credentials()
    authenticator = stauth.Authenticate(
        credentials=credentials, cookie_name='KoalaChatFounders', key='KCF_123')
    st.session_state['authenticator'] = authenticator


def UI_login(authenticator):
    name, authentication_status, username = authenticator.login(
        'Login', 'main')
    st.session_state['authentication_status'] = authentication_status
    st.session_state['username'] = username
    st.session_state['name'] = name
