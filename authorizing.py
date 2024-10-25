import requests
import base64
import os

# Haal de waarde van de omgevingsvariabelen op
TENNANT = os.getenv('TENNANT')
USER = os.getenv('USER')


def generate_authorization():
	combined_key = f"{TENNANT}:{USER}"

	combined_key_bytes = combined_key.encode("ascii")
	base64_bytes_key = base64.b64encode(combined_key_bytes)

	# Decoding and formatting authentication token
	auth_token = base64_bytes_key.decode("ascii")
	authorization = {"Authorization" : f"Basic {auth_token}"}

	return authorization



if __name__ == '__main__':
    print(generate_authorization())