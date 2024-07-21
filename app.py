from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get data from the form
    origin = request.json.get('origin')
    destination = request.json.get('destination')
    cabin = request.json.get('cabin')
    show_pro_filter = request.json.get('showProFilter', False)

    # Prepare request data
    json_data = {
        'origin': origin,
        'destination': destination,
        'partnerPrograms': [
            'Air Canada', 'United Airlines', 'KLM', 'Qantas', 'American Airlines',
            'Etihad Airways', 'Alaska Airlines', 'Qatar Airways', 'LifeMiles',
        ],
        'stops': 2,
        'departureTimeFrom': '2024-07-09T00:00:00Z',
        'departureTimeTo': '2024-10-07T00:00:00Z',
        'isOldData': False,
        'limit': 302,
        'offset': 0,
        'cabinSelection': [cabin],
        'date': '2024-07-09T12:00:17.796Z',
    }

    # Make API request
    response = requests.post('https://cardgpt.in/apitest', json=json_data)
    data = response.json().get('data', [])

    # Example response processing
    results = []
    for entry in data:
        results.append({
            'partner_program': entry.get('partner_program'),
            'min_business_miles': entry.get('min_business_miles', 'N/A'),
            'min_business_tax': entry.get('min_business_tax', 'N/A'),
            'min_economy_miles': entry.get('min_economy_miles', 'N/A'),
            'min_economy_tax': entry.get('min_economy_tax', 'N/A'),
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
