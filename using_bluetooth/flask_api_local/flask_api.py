from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient


app = Flask(__name__ )

# Connect to MongoDB
client = MongoClient('mongodb+srv://jakebentley2001:Sonicpower4@serverlessinstance0.hzqw4sr.mongodb.net/?retryWrites=true&w=majority&appName=ServerlessInstance0')
db = client['IOT_DEVICE']
collection = db['muscle_data']

@app.route('/')
def index():
    return render_template('tester_index.html')

@app.route('/get_recording', methods=['GET'])
def get_recording():
    record_number = request.args.get('record_number')

    if record_number:
        try:
            document = collection.find_one({"record_number": record_number})
            if document:
                sensor_data = document['data'][1]
                time_data = document['data'][0]
                return jsonify({"record_number": record_number, "data": sensor_data})
            else:
                return jsonify({"error": "Record not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Error retrieving record: {str(e)}"}), 500
    else:
        return jsonify({"error": "Missing record_number parameter"}), 400
    
    
@app.route('/save-coordinates', methods=['POST'])
def save_coordinates():
    data = request.json
    formatted_coordinates = [[round(point['lat'], 4), round(point['lng'], 4)] for point in data]
    print('Received coordinates:', formatted_coordinates)
    return 'Coordinates received successfully.'

if __name__ == "__main__":
    app.run(debug=True)
