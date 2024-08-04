import streamlit as st
import pytesseract
from PIL import Image
import json
import pickle

# Set the path for tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

st.title("CUSTAMIZABLE BILLING SYSTEM")

# Upload image file
uploaded_file = st.file_uploader("UPLOAD THE BILL", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image file
    image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(image)
    
    # Display the extracted text
    st.text_area("EXTRACTION OF TEXT", text, height=200)
    
    # Split the text by new lines and filter out empty lines
    lines = [line for line in text.split('\n') if line.strip()]
    
    # Initialize a list to hold the dictionaries for each row
    data_list = []
    
    # Process each line to extract the key-value pairs
    for line in lines:
        values = line.split()
        if len(values) == 4:
            row_data = {headers[i]: values[i] for i in range(4)}
            data_list.append(row_data)
    
    # Convert the list of dictionaries into JSON format
    json_data = json.dumps(data_list, indent=4)
    
    # Display the JSON data
    st.json(json_data)
    
    # Provide an option to download the JSON data
    json_bytes = json_data.encode('utf-8')
    st.download_button(label='Download JSON', data=json_bytes, file_name='data.json', mime='application/json')

    # Dump the JSON data into a pickle file
    with open('json_data.pkl', 'wb') as f:
        pickle.dump(json_data, f)
