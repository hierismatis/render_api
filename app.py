from flask import Flask, Response, request
import pandas as pd
import extract_data
import os


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home(): 
    return "<h1>He rens dikke sukkel</h1>"

@app.route('/contacts', methods=['GET'])
def contact_data():
    fields = request.args.get('fields', 'all_fields')
    data = extract_data.get_contacts(fields=fields)
    return data

if __name__ == '__main__':
    app.run()