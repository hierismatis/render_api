import requests
from authorizing import generate_authorization
import os

def get_contacts():
	authorization = generate_authorization()
	params={'limit': 4000}

	URL = "https://api.tomtoday.com/api/contacts/categories/1/contacts"

	response = requests.get(URL, headers=authorization, params=params)

	response_data = response.json()['data']

	return response_data