import streamlit as st
import streamlit_authenticator as stauth
import utilities.database as db

# Bring up Emoji window by pressing Windows key + .

# get user credentials


def UI_login():
    credentials = db.get_credentials()

    authenticator = stauth.Authenticate(
        credentials=credentials, cookie_name='KoalaChatFounders', key='KCF_123')

    name, authentication_status, username = authenticator.login(
        'Login', 'main')

    return name, authentication_status, username, authenticator
