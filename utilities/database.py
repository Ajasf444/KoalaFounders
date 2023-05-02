import deta
import streamlit as st
import streamlit_authenticator as stauth
import time
from config import DETA_KOALAFOUNDERS_DB_KEY

deta = deta.Deta(DETA_KOALAFOUNDERS_DB_KEY)
db = deta.Base('Users')

# TODO: make this function asynchronous


def _fetch_all_users():
    result = db.fetch()
    return result.items


def get_credentials():
    users = _fetch_all_users()
    login_info = [
        (user['username'], {
            'email': user['key'],
            'name': user['name'],
            'password': user['password'],
        }) for user in users
    ]
    credentials = {
        'usernames': dict(login_info),
    }
    return credentials


def fetch_user_info(username):
    result = db.fetch({'username': f'{username}'})
    return result.items[0]


def _update(updates, key):
    db.update(updates, key)


def update_password(authenticator):
    username = st.session_state['username']
    user_info = authenticator.credentials['usernames'][username]
    email, password = user_info['email'], user_info['password']
    _update({'password': password}, email)


def update_info(authenticator):
    username = st.session_state['username']
    # user_info = authenticator.credentials['usernames'][username]
    # print(user_info)
    # name, email = user_info['name'], user_info['email']
    db_info = fetch_user_info(username)
    print(db_info)
    db_email = db_info['key']
    # print(email, db_email)
    _update({'name': 'bacon'}, db_email)


def decrement_queries_left(username):
    user_info = fetch_user_info(username)
    email = user_info['key']
    queries_left = user_info['queries_left'] - 1
    _update({'queries_left': queries_left}, email)
    return queries_left
