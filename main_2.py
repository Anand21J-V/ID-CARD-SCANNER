import streamlit as st
import pytesseract
from PIL import Image
import json
import pickle

# Set the path for tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

st.title("OCR Text Extraction and JSON Conversion")

# Upload image file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image file
    image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(image)
    
    # Display the extracted text
    st.text_area("Extracted Text", text, height=200)
    
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
        else:
            key, value = line.split(' ', 1)
            key = key.strip()
            value = value.strip()
        data[key] = value
    
    # Convert the dictionary into JSON format
    json_data = json.dumps(data, indent=4)
    
    # Display the JSON data
    st.json(json_data)
    
    # Provide an option to download the JSON data
    json_bytes = json_data.encode('utf-8')
    st.download_button(label='Download JSON', data=json_bytes, file_name='data.json', mime='application/json')

    # Dump the JSON data into a pickle file
    with open('json_data.pkl', 'wb') as f:
        pickle.dump(json_data, f)
