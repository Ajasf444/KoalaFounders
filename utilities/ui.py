import streamlit as st
import utilities.database as db


def set_main_ui():
    """Sets the UI for the app."""
    hide_streamlit_style = """ <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def set_sidebar_ui(authenticator):
    username = st.session_state['username']
    # container widget with expanding button
    with st.sidebar.expander('Options'):
        # reset username button
        # reset password button
        # logout button
        option = st.selectbox('Account Options', ['',
                              'Reset Password', 'Reset Username'])
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
            case 'Reset Username':
                try:
                    st.write('baconator')
                except Exception as e:
                    st.error(e)
        authenticator.logout('Logout', 'main')
