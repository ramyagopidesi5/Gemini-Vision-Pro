from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini API and get response
def get_gemini_response(input_image, prompt):
    # Use the updated model name
    model = genai.GenerativeModel('gemini-1.5-flash')
    # The input to this model may require raw bytes or image data; adjust accordingly
    response = model.generate_content([input_image, prompt])
    return response.text

# Function to process the uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert uploaded file to PIL.Image.Image
        image = Image.open(uploaded_file)

        # Prepare the input in the expected format (raw bytes or other required format)
        image_data = {
            "mime_type": uploaded_file.type,  # Example: "image/jpeg"
            "data": uploaded_file.getvalue(),  # Raw bytes of the image
        }
        return image_data
    else:
        raise FileNotFoundError("No file uploaded")

# Define the input prompt
input_prompt = """
You are an expert pharmaceutical/Chemist where you need to see the tablets from the image 
and provide the details of every drug/tablet item with the below format:

1. Examine the image carefully and identify the tablets depicted.
2. Describe the uses and functionalities of each tablet shown in the image.
3. Provide information on the intended purposes, features, and typical applications of the tablets.
4. If possible, include any notable specifications or distinguishing characteristics of each tablet.
5. Ensure clarity and conciseness in your descriptions, focusing on key details and distinguishing features.
"""

# Initialize the Streamlit app
st.set_page_config(page_title="AI Chemist App")
st.header("AI Chemist App")

# Text input for additional user-defined prompt
user_input = st.text_input("Additional Prompt (Optional): ", key="input")

# File uploader for image input
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

# Button to process the input
submit = st.button("Tell me")

# If the submit button is clicked
if submit:
    try:
        # Process the uploaded file and get the response
        image_data = input_image_setup(uploaded_file)  # Prepare input in correct format
        combined_prompt = f"{input_prompt} {user_input}" if user_input else input_prompt
        response = get_gemini_response(image_data, combined_prompt)
        st.subheader("The Response is:")
        st.write(response)
    except FileNotFoundError:
        st.error("Please upload an image before submitting.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
