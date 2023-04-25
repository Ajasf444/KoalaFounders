import deta
import streamlit_authenticator as stauth
from config import DETA_KOALAFOUNDERS_DB_KEY

deta = deta.Deta(DETA_KOALAFOUNDERS_DB_KEY)
db = deta.Base('Users')


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
