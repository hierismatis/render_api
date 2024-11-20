import requests
from authorizing import generate_authorization
import os
import pandas as pd

def filter_by_field(df,fields):


	if fields == []:
		return_data = df.to_dict(orient='records')
		# return_data = df.to_csv(index=False)

	else:

		try: 
			return_data =  df[fields].to_csv(index=False)
		except KeyError:
			return_data = "Error: dat veld bestaat niet in contacten"

	return return_data

def get_contacts(category='contacts', fields=[]):
	authorization = generate_authorization()
	params={'limit': 4000}

	url_dict = {'contacts': 'https://api.tomtoday.com/api/contacts/categories/1/contacts',
		'companies': 'https://api.tomtoday.com/api/contacts/categories/2/contacts',
		'leads': 'https://api.tomtoday.com/api/contacts/categories/3/contacts'}

	url = url_dict[category]

	response = requests.get(url, headers=authorization, params=params)

	response_data = response.json()['data']

	contacts = pd.json_normalize(response_data)

	if category == 'contacts':
		contacts.drop(['gender','created_at', 'updated_at', 'f30', 'entity', 'birthdate', 'birthdate_day', 'birthdate_month', 'birthdate_year', 'birthplace', 'nationality', 'marital_status', 'street','housenumber','street2','city','state','zip','suburb','country','website','phone_cc','phone_number','phone_ext','identification','uuid','uuid_short','created_by','updated_by','deleted_at','phone_country','password','reset_password_token','expiration_date_for_password_reset_token','invoices_currency','invoices_open_balance','invoices_overdue_balance','external_contact_type','external_contact_id','expiration_notification_sent','from_public_form','verified','language','invoices_last_reminder_sent_at','authorized_to_sign','f18','f21','f25','f26','f28','f33','f34','f36','f37','f38','f39','f41','f42','f44','f45','f46','f47','f48','f49','f50','f53','f54','f55','f57','f58','f59','f61','f62','f63','f64','f66','f68','f369','f370','f371','f372','f373','f374','f375','f376','f377','accounting_list_id','accounting_edit_sequence','bisner_sync','bisner_hide','bisner_blocked','bisner_id','bisner_company_name','bisner_location_id','bisner_role_id','bisner_email','bisner_default_contract_for_extra_sales_id','pivot.category_id','pivot.contact_id','pivot.deleted_at'], axis=1, inplace=True)
		contacts = contacts.rename(columns={'f67': 'phone_number'})

	elif category == 'companies':
		contacts.drop(['created_at','updated_at','f26','f34','f61','f62','f63','entity','first_name','last_name','gender','birthdate','birthdate_day','birthdate_month','birthdate_year','birthplace','nationality','marital_status','street','housenumber','street2','city','state','zip','suburb','country','website','phone_cc','phone_number','phone_ext','identification','uuid','uuid_short','created_by','updated_by','deleted_at','phone_country','password','reset_password_token','expiration_date_for_password_reset_token','invoices_currency','invoices_open_balance','invoices_overdue_balance','external_contact_type','external_contact_id','expiration_notification_sent','from_public_form','verified','language','invoices_last_reminder_sent_at','authorized_to_sign','f18','f21','f30','f33','f36','f37','f38','f39','f41','f42','f44','f45','f46','f47','f48','f49','f50','f53','f54','f55','f57','f58','f59','f64','f66','f68','f369','f370','f371','f372','f373','f374','f375','f376','f377','accounting_list_id','accounting_edit_sequence','bisner_sync','bisner_hide','bisner_blocked','bisner_id','bisner_company_name','bisner_location_id','bisner_role_id','bisner_email','bisner_default_contract_for_extra_sales_id','pivot.category_id','pivot.contact_id','pivot.deleted_at'], axis=1, inplace=True)
		contacts = contacts.rename(columns={'f67': 'phone_number',
											'f25': 'kvk_nummer',
											'f28': 'IBAN'})
	return filter_by_field(contacts, fields)


def get_units(fields='all_fields'):
	authorization = generate_authorization()

	url = 'https://api.tomtoday.com/api/office-rental/units'
	units = pd.json_normalize(requests.get(url, headers=authorization).json()['data'])

	url = 'https://api.tomtoday.com/api/office-rental/floors'
	floors = pd.json_normalize(requests.get(url, headers=authorization).json()['data']).rename(columns={'id': 'floor_id'})

	url = 'https://api.tomtoday.com/api/office-rental/locations'
	locations = pd.json_normalize(requests.get(url, headers=authorization).json()['data']).rename(columns={'id': 'location_id'})

	floors_locations = pd.merge(floors, locations, on='location_id', how='left')

	units_floors_locations = pd.merge(units, floors_locations, on='floor_id', how='left')

	for column in ['address', 'postal_code', 'city', 'country']:
		units_floors_locations[column] = units_floors_locations[column].combine_first(units_floors_locations[f'{column}_x']).combine_first(units_floors_locations[f'{column}_y'])

	units_floors_locations.drop(['active_y', 'start_date_y', 'end_date_y', 'product_id', 'custom_price', 'number', 'postal_code_y', 'city_y', 'country_y', 'address_y','rent_accounting_account_id', 'rent_no_tax_accounting_account_id', 'rent_no_tax_accounting_costcenter_id','service_costs_accounting_account_id','service_costs_no_tax_accounting_account_id','service_costs_downpayment_accounting_account_id','service_costs_downpayment_no_tax_accounting_account_id','website_price','nvo','vvo','bvo', 'accounting_costcenter_id','discount_accounting_account_id','discount_no_tax_accounting_account_id','rent_invoice_group_id','rent_no_tax_invoice_group_id','service_costs_invoice_group_id','service_costs_no_tax_invoice_group_id','service_costs_downpayment_invoice_group_id','service_costs_downpayment_no_tax_invoice_group_id','discount_invoice_group_id','discount_no_tax_invoice_group_id','surface_price_service_costs','surface_price_service_costs_downpayment','map_coordinates','show_on_website_x','uuid_x','max_persons','desks','default_extra_sales_products', 'address_x', 'postal_code_x','city_x','country_x','start_date_x','end_date_x','active_x','use_interactive_map','show_on_website_y','show_prices','order','map_type','map_redirect_link_y','uuid_y','map_internal_default_zoom','map_external_default_zoom','short_label','address_on_floor','address_on_unit','product_category_id','has_keys','has_tags','accounting_journal_id','external_id', 'map_redirect_link_x', 'contact_id', 'contact',], axis=1, inplace=True)

	units_floors_locations = units_floors_locations.dropna(subset=['region'])

	units_floors_locations = units_floors_locations.rename(columns={'label_y': 'location_label',
																	'f25': 'kvk_nummer',
																	'f28': 'IBAN',
																	'label_x': 'floor_label'})

	return filter_by_field(units_floors_locations, fields)


# def get_relations():
# 	authorization = generate_authorization()

# 	url = 'https://api.tomtoday.com/api/contacts/'
# 	relations = pd.json_normalize(requests.get(url, headers=authorization).json())

# 	return relations


if __name__ == '__main__':
	print(get_contacts(category="companies"))

