from flask import Flask, Response
import pandas as pd


app = Flask(__name__)

@app.route('/convert', methods=['GET'])
def convert_excel_to_csv():
    # Pad naar het Excel-bestand in de directory van de API
    excel_pad = 'companies.xlsx'  # Geef de naam van het bestand in deze directory

    # Lees het Excel-bestand in met pandas
    try:
        df = pd.read_excel(excel_pad)
    except Exception as e:
        return f"Fout bij het lezen van het Excel-bestand: {str(e)}", 400
    
    # Converteer de DataFrame naar CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    # Return de CSV als een download
    return csv_buffer.getvalue()


if __name__ == '__main__':
    app.run(debug=True)