from flask import Flask, Response
import pandas as pd
from extract_data import get_contacts
import os


app = Flask(__name__)

@app.route('/convert', methods=['GET'])
def return_contacts():
    contacts = get_contacts()
    return contacts

if __name__ == '__main__':
    app.run()