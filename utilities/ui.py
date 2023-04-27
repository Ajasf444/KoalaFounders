import streamlit as st
import utilities.database as db
from utilities import queries


def set_main_ui():
    """Sets the UI for the app."""
    hide_streamlit_style = """ <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.title('TCM KoalaChat Founders')

def set_sidebar_ui(authenticator):
    username = st.session_state['username']
    name = authenticator.credentials['usernames'][username]['name']
    # container widget with expanding button
    with st.sidebar.expander('Options'):
        st.write(f'Welcome {name}!')
        # reset username button
        # reset password button
        # logout button
        option = st.selectbox('Account Options', ['Select an Option',
                              'Reset Password', 'Update User Details (WIP)'])
        match option:
            case '':
                pass
            case 'Reset Password':
                try:
                    if authenticator.reset_password(username, 'Reset Password', 'main'):
                        db.update_password(authenticator)
                        st.success('Password updated')
                except Exception as e:
                    st.error(e)
            case 'Update User Details (WIP)':
                pass
        authenticator.logout('Logout', 'main')
