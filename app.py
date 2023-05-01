import asyncio
import streamlit as st
from login import UI_startup, UI_login
from utilities import ui, queries
from utilities import database as db
import datetime as dt
from dateutil.relativedelta import relativedelta as rd

# run the login section
if 'authenticator' not in st.session_state:
    UI_startup()

authenticator = st.session_state['authenticator']

if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    UI_login(authenticator)

username = st.session_state['username']
name = st.session_state['name']
authentication_status = st.session_state['authentication_status']


def main():
    """Runs the main app."""
    # TODO: throw this information in an initialize history function
    if 'input_history' not in st.session_state:
        st.session_state.input_history = []
    if 'output_history' not in st.session_state:
        st.session_state.output_history = []

    # TODO: put in query_setup()
    able_to_query, queries_left = queries.query_setup(
        username)

    queries_left_box = st.empty()
    with queries_left_box.container():
        st.write(f'Queries left: {queries_left}')

    if able_to_query:
        with st.form('query_form'):
            query = st.text_input('Enter your query:')
            submit = st.form_submit_button('Submit')

        if query and submit:
            placeholder = st.empty()
            data = queries.create_query(query, st.session_state.input_history,
                                        st.session_state.output_history, False)
            queries_left = queries.decrement_queries_left(username
                                                          )
            with queries_left_box.container():
                st.write(f'Queries left: {queries_left}')
            with st.spinner('Awaiting response...'):
                response = asyncio.run(queries.ask_koala(data))
            with placeholder.container():
                st.markdown('KoalaChat response:')
                st.write(response)
                st.session_state.input_history.append(query)
                st.session_state.output_history.append(response)
        else:
            pass
    else:
        next_month = dt.date.today().replace(day=15) + rd(months=+1)
        st.error(
            f'You have reached your API limit for this month. Please try again on {next_month.strftime(r"%m/%d/%Y")}.')


if authentication_status:
    ui.set_main_ui()
    ui.set_sidebar_ui(authenticator)
    main()
elif authentication_status is False:
    st.error('Username/password is incorrect.')
elif authentication_status is None:
    st.info('Please enter your username and password.')
