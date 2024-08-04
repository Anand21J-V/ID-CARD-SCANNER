import streamlit as st
from PIL import Image
import pytesseract
import json
import pickle
import cv2

# Specify the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def extract_text_from_image(image):
    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(image)
    # Convert the extracted text into a dictionary
    data = {'text': text}
    # Convert the dictionary into JSON format
    json_data = json.dumps(data)
    # Dump the JSON data into a pickle file
    with open('json_data.pkl', 'wb') as f:
        pickle.dump(json_data, f)
    return json_data

# Streamlit app
st.title("Text Extraction from Image using Tesseract OCR")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    # Open the image file
    image = Image.open(uploaded_file)
    # Display the image
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")
    st.write("Extracting text...")
    
    # Extract text from image
    json_data = extract_text_from_image(image)
    
    # Display the extracted text
    st.write("Extracted Text:")
    st.json(json.loads(json_data))
