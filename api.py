from flask import Flask, request, jsonify, send_file
from PIL import Image
import pytesseract
import json
import pickle
import io

app = Flask(__name__)

# Set the path for tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400
    
    try:
        # Open the image file
        image = Image.open(file.stream)
        
        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(image)
        
        # Split the text by new lines and filter out empty lines
        lines = [line for line in text.split('\n') if line.strip()]
        
        # Initialize an empty dictionary to hold the key-value pairs
        data = {}
        
        # Process each line to extract the key-value pairs
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                data[key] = value
            elif ' ' in line:
                key, value = line.split(' ', 1)
                key = key.strip()
                value = value.strip()
                data[key] = value
            else:
                # If no recognizable key-value pair, add the line as a key with empty value
                data[line.strip()] = ""
        
        # Convert the dictionary into JSON format
        json_data = json.dumps(data, indent=4)
        
        # Dump the JSON data into a pickle file
        with open('json_data.pkl', 'wb') as f:
            pickle.dump(json_data, f)
        
        # Return the JSON data
        return jsonify(data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download_json', methods=['GET'])
def download_json():
    try:
        # Read the JSON data from the pickle file
        with open('json_data.pkl', 'rb') as f:
            json_data = pickle.load(f)
        
        # Send the JSON data as a file
        return send_file(
            io.BytesIO(json_data.encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name='data.json'
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
