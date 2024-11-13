from flask import Flask, Response, request
import pandas as pd
import extract_data
import os


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():     
    return "verkeerde endpoint"

@app.route('/contacts', methods=['GET'])
def contact_data():
    fields = request.args.get('fields', 'all_fields')
    data = extract_data.get_contacts(category='contacts', fields=fields)
    
    response = Response(data, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    return response


@app.route('/companies', methods=['GET'])
def company_data():
    fields = request.args.get('fields', 'all_fields')
    data = extract_data.get_contacts(category='companies', fields=fields)
    
    response = Response(data, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    return response

@app.route('/units', methods=['GET'])
def units_data():
    fields = request.args.get('fields', 'all_fields')
    data = extract_data.get_real_estate(fields=fields)

    response = Response(data, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    return response


if __name__ == '__main__':
    app.run()