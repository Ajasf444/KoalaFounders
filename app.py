import asyncio
import streamlit as st
import login
from streamlit_chat import message
from utilities import ui, queries


def main():
    """Runs the main app."""
    # TODO: throw this information in an initialize history function
    initialize_history()

    able_to_query, queries_left = queries.query_setup(
        username)
    queries_left_box = create_queries_box(queries_left)

    if able_to_query:
        with st.form('query_form'):
            query = st.text_area('Enter your query:')
            submit = st.form_submit_button('Submit')
        if query and submit:
            data = queries.create_query(query, st.session_state.input_history,
                                        st.session_state.output_history, False)
            queries_left = queries.decrement_queries_left(username
                                                          )
            new_responses = st.empty()
            old_responses = st.empty()
            with old_responses.container():
                for i, user_input in enumerate(reversed(st.session_state.input_history), start=1):
                    message(user_input, is_user=True, key=str(i))
                    message(
                        st.session_state.output_history[-i], key=str(-i) + '_user')
            with new_responses.container():
                message(query, is_user=True)
                with queries_left_box.container():
                    st.write(f'Queries left: {queries_left}')
                with st.spinner('Awaiting response...'):
                    response = asyncio.run(queries.ask_koala(data))
                # st.markdown('KoalaChat response:')
                message(response)
                st.session_state.input_history.append(query)
                st.session_state.output_history.append(response)
        else:
            pass
    else:
        queries.next_available_month()


def initialize_history():
    if 'input_history' not in st.session_state:
        st.session_state.input_history = []
    if 'output_history' not in st.session_state:
        st.session_state.output_history = []


def create_queries_box(queries_left):
    box = st.empty()
    with box.container():
        st.write(f'Queries left: {queries_left}')
    return box


#### MAIN ####
# run the login layer
authenticator, username, name, authentication_status = login.layer()

if authentication_status:
    ui.set_main_ui()
    ui.set_sidebar_ui(authenticator)
    main()
elif authentication_status is False:
    st.error('Username/password is incorrect.')
elif authentication_status is None:
    st.info('Please enter your username and password.')
