import asyncio
from login import UI_login
import streamlit as st
from utilities import ui
from utilities.queries import create_query, ask_koala
from utilities import database as db
import datetime as dt
# run the login section
name, _, username, authenticator = UI_login()


def main():
    """Runs the main app."""
    # TODO: throw this information in an initialize history function
    if 'input_history' not in st.session_state:
        st.session_state.input_history = []
    if 'output_history' not in st.session_state:
        st.session_state.output_history = []

    user_info = db.fetch_user_info(username)
    queries_left = user_info['queries_left']
    query_reset_date = user_info['query_reset_date']

    # TODO: update queries left based on query_reset_date

    able_to_query = queries_left > 0

    # TODO: check if API limit has been reached
    st.title('TCM KoalaChat Founders')

    if able_to_query:
        st.write(f'Queries left: {queries_left}')
        query = st.text_input('Enter your query:')
        authorized_user = True
        api_limit_reached = False
        # TODO: add API limit checks that reset monthly and check if user is authorized
        if authorized_user and not api_limit_reached:
            if query:
                placeholder = st.empty()
                data = create_query(query, st.session_state.input_history,
                                    st.session_state.output_history, False)
                with st.spinner('Awaiting response...'):
                    response = asyncio.run(ask_koala(data))
                with placeholder.container():
                    st.markdown('KoalaChat response:')
                    st.write(response)
                    st.session_state.input_history.append(query)
                    st.session_state.output_history.append(response)
            else:
                pass
    else:
        st.markdown(
            'You have reached your API limit for this month. Please try again next month.')


if st.session_state['authentication_status']:
    ui.set_main_ui()
    ui.set_sidebar_ui(authenticator)
    main()
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect.')
elif st.session_state['authentication_status'] is None:
    st.info('Please enter your username and password.')
