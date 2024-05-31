# from flask import Flask, request, jsonify
# from prop_valuation import compute_valuation  # Import the function from the module

# app = Flask(__name__)

# @app.route('/valuation', methods=['POST'])
# def valuation():
#     data = request.json  # Get JSON data from the request body
#     response = {}

#     # Extract data from request
#     address = data.get('address')
#     property_type = data.get('property_type')
#     industrial_size = data.get('industrial_size')
#     industrial_subtype = data.get('industrial_subtype')
#     office_grade = data.get('office_grade')
#     distance = data.get('distance')
#     expense = data.get('expense')

#     # Check if necessary data is available
#     if property_type:
#         # Call the imported function
#         response['valuation'] = compute_valuation(address, property_type, industrial_size, industrial_subtype, office_grade, distance, expense)
#     else:
#         response['error'] = "Property type is required."

#     return jsonify(response)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from prop_valuation import compute_valuation  # Import the function from the module
import pandas as pd

app = Flask(__name__)
CORS(app)

# In-memory database for demonstration purposes
users = {}

property_data = {
    "industrial": {},
    "office": {}
}


def load_csv_data():
    
    industrial_cap_rates   =pd.read_csv('./updated_rentals_industrial/updated_caprates_industrial.csv')
    industrial_rentals   = pd.read_csv('./updated_rentals_industrial/updated_caprates_office.csv')
    office_cap_rates = pd.read_csv('./updated_rentals_industrial/updated_rentals_industrial.csv')
    office_rentals   = pd.read_csv('./updated_rentals_industrial/updated_rentals_office.csv')
    property_data['industrial']['cap_rates'] = industrial_cap_rates.to_dict(orient='records')
    property_data['industrial']['rentals'] = industrial_rentals.to_dict(orient='records')
    property_data['office']['cap_rates'] = office_cap_rates.to_dict(orient='records')
    property_data['office']['rentals'] = office_rentals.to_dict(orient='records')
load_csv_data()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and check_password_hash(users[username], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({"error": "User already exists"}), 400
    else:
        users[username] = generate_password_hash(password)
        return jsonify({"message": "User registered successfully"}), 201


    
@app.route('/property', methods=['GET'])
def get_property_data():
    address = request.args.get('address')
    # For simplicity, returning all property data. Implement specific address-based retrieval if needed.
    return jsonify(property_data), 200

@app.route('/valuation', methods=['POST'])
def valuation():
    data = request.json  # Get JSON data from the request body

    # Extract data from request
    address = data.get('address', 'default address')  # Default value for testing
    property_type = data.get('property_type')
    industrial_size = data.get('industrial_size', 0)  # Default value for testing
    industrial_subtype = data.get('industrial_subtype', '')  # Default value for testing
    office_grade = data.get('office_grade', 'A')  # Default value for testing
    distance = data.get('distance', 3000)  # Default value for testing
    expense = data.get('expense', 0.3)  # Default value for testing

    # Check if necessary data is available
    if not property_type:
        return jsonify({'error': 'Property type is required'}), 400

    # Call the imported function
    try:
        result = compute_valuation(address, property_type, industrial_size, industrial_subtype, office_grade, distance, expense)
        return jsonify({'valuation': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
