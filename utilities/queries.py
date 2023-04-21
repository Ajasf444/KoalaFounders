import json
import requests
from config import KOALACHAT_API_KEY

def create_query(query: str, input_history: list[str], output_history: list[str], realtimedata: bool) -> dict:
    '''Creates a query to send to KoalaChat API.'''
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
        'Authorization': f'Bearer {KOALACHAT_API_KEY}',
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers = headers, data = json.dumps(data), timeout = 10)
    return response.json().get('output')

# url = 'https://koala.sh/api/gpt/'
# headers = {
#     'Authorization': f'Bearer {KOALACHAT_API_KEY}',
#     'Content-Type': 'application/json',
# }

# print(headers.get('Authorization'))

# data = {
#     'input': 'My name is Bob. What about yours?',
#     'inputHistory': ['Hello'],
#     'outputHistory': ['Hi! What is your name?'],
#     'realTimeData': False,
# }

# response = requests.post(url, headers = headers, data = json.dumps(data), timeout = 10)

# print(response.request.headers)
# print(response.request.body)

# response_json = response.json()
# print(response_json)
# print(response_json.get('output'))