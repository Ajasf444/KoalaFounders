import asyncio
import datetime as dt
import functools
import streamlit as st
import json
import requests
import utilities.database as db
from dateutil.relativedelta import relativedelta as rd
from config import KOALACHAT_API_KEY


def _should_query_reset(query_reset_date):
    qrd = dt.datetime.strptime(query_reset_date, r'%m/%d/%Y').date()
    today = dt.date.today()
    return today > qrd


def _reset_queries(email):
    db._update({'queries_left': 1_000}, email)


def _update_query_reset_date(email):
    today = dt.date.today()
    current_month, current_year = today.month, today.year
    next_month = dt.date(current_year, current_month, 15) + rd(months=+1)
    db._update({'query_reset_date': next_month.strftime(r'%m/%d/%Y')}, email)


def query_setup(username):
    user_info = db.fetch_user_info(username)
    email = user_info['key']
    query_reset_date = user_info['query_reset_date']

    # TODO: update queries left based on query_reset_date
    if _should_query_reset(query_reset_date):
        _reset_queries(email)
        _update_query_reset_date(email)
        user_info = db.fetch_user_info(username)

    queries_left = user_info['queries_left']

    able_to_query = queries_left > 0
    return able_to_query, queries_left


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


async def ask_koala(data: dict) -> str:
    '''Sends a query to KoalaChat API and returns the response.'''
    loop = asyncio.get_event_loop()
    url = 'https://koala.sh/api/gpt/'
    headers = {
        # TODO: import KOALACHAT_API_KEY from Streamlit environment variables
        'Authorization': f'Bearer {KOALACHAT_API_KEY}',
        'Content-Type': 'application/json',
    }
    future = loop.run_in_executor(
        None, func=functools.partial(requests.post, url=url, headers=headers, data=json.dumps(data), timeout=600))
    response = await future
    return response.json().get('output')


def decrement_queries_left(username):
    queries_left = db.decrement_queries_left(username)
    return queries_left
