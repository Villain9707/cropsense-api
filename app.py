from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Importing pickle files
model = pickle.load(open('classifier.pkl', 'rb'))
ferti = pickle.load(open('fertilizer.pkl', 'rb'))


@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from the POST request
    data = request.get_json()

    temp = data.get('temp')
    humi = data.get('humid')
    mois = data.get('mois')
    soil = data.get('soil')
    crop = data.get('crop')
    nitro = data.get('nitro')
    pota = data.get('pota')
    phosp = data.get('phos')

    # Check if any input is missing or not numeric
    if None in (temp, humi, mois, soil, crop, nitro, pota, phosp) or not all(val.isdigit() for val in (
    str(temp), str(humi), str(mois), str(soil), str(crop), str(nitro), str(pota), str(phosp))):
        return jsonify({'error': 'Invalid input. Please provide numeric values for all fields.'}), 400

    # Convert values to integers
    input_data = [int(temp), int(humi), int(mois), int(soil), int(crop), int(nitro), int(pota), int(phosp)]

    # Get prediction
    prediction = ferti.classes_[model.predict([input_data])[0]]

    # Return the prediction as a response
    return jsonify({'prediction': prediction})


if __name__ == "__main__":
    app.run(debug=True)
