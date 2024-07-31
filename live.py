from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API key not found. Please set it in the .env file.")
    st.stop()
genai.configure(api_key=api_key)

# Function to get Gemini response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Function to set up input image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit setup
st.set_page_config(page_title="Gemini Image demo")
st.header("Gemini Image Based Applications")
input = st.text_input("Input Prompt: ", key="input_text")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Explain the image to me 👇 ")

input_prompt = """
You are an expert in GYM training and your task is to see the daily diet from the image and provide answers based on that image on which day how much/many things a person should take as per the diet chart.
Format:
1. How many things the person should take
2. How much the person should take

----
----
"""

if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input)
        st.subheader("The Response is")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
