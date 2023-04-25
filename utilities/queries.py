import streamlit as st
import json
import requests
from config import KOALACHAT_API_KEY

hide_streamlit_style = """ <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """
st.markdown(hide_streamlit_style, unsafe_allow_html = True)

def create_query(
    query: str, 
    input_history: list[str] = None, 
    output_history: list[str] = None, 
    realtimedata: bool = False,
) -> dict:
    '''Creates data dictionary to be used in a KoalaChat query.'''
    if not input_history:
        input_history = []
    if not output_history:
        output_history = []

    data = {
        'input': query,
        'inputHistory': input_history,
        'outputHistory': output_history,
        'realTimeData': realtimedata,
    }

    return data

def ask_koala(data: dict) -> str:
    '''Sends a query to KoalaChat API and returns the response.'''

    url = 'https://koala.sh/api/gpt/'
    headers = {
        'Authorization': f'Bearer {KOALACHAT_API_KEY}', #TODO: import KOALACHAT_API_KEY from Streamlit environment variables
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers = headers, data = json.dumps(data), timeout = 600)
    return response.json().get('output')
