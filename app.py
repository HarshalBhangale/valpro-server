from flask import Flask, request, jsonify
from prop_valuation import compute_valuation  # Import the function from the module

app = Flask(__name__)

@app.route('/valuation', methods=['POST'])
def valuation():
    data = request.json  # Get JSON data from the request body
    response = {}

    # Extract data from request
    address = data.get('address')
    property_type = data.get('property_type')
    industrial_size = data.get('industrial_size')
    industrial_subtype = data.get('industrial_subtype')
    office_grade = data.get('office_grade')
    distance = data.get('distance')
    expense = data.get('expense')

    # Check if necessary data is available
    if property_type:
        # Call the imported function
        response['valuation'] = compute_valuation(address, property_type, industrial_size, industrial_subtype, office_grade, distance, expense)
    else:
        response['error'] = "Property type is required."

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
