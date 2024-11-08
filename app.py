from flask import Flask, Response, request
import pandas as pd
import extract_data
import os


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():     
    return "<h1>He Pedro kk sukkeltje</h1>"

@app.route('/contacts', methods=['GET'])
def contact_data():
    fields = request.args.get('fields', 'all_fields')
    data = extract_data.get_contacts(category='contacts', fields=fields)
    return data

@app.route('/companies', methods=['GET'])
def company_data():
    fields = request.args.get('fields', 'all_fields')
    data = extract_data.get_contacts(category='companies', fields=fields)
    return data

if __name__ == '__main__':
    app.run()