import requests
from authorizing import generate_authorization
import os
import pandas as pd

def get_contacts(category='contacts', fields='all_fields'):
	authorization = generate_authorization()
	params={'limit': 4000}

	url_dict = {'contacts': 'https://api.tomtoday.com/api/contacts/categories/1/contacts',
		'companies': 'https://api.tomtoday.com/api/contacts/categories/2/contacts' }

	url = url_dict[category]

	response = requests.get(url, headers=authorization, params=params)

	response_data = response.json()['data']

	contacts = pd.json_normalize(response_data)

	if fields == 'all_fields':
		return_data = contacts.to_csv()

	else:
		fields_list = fields.split(',')

		try: 
			return_data =  contacts[fields_list].to_csv()
		except KeyError:
			return_data = "Error: dat veld bestaat niet in contacten"

	return return_data










if __name__ == '__main__':
	print(get_contacts())