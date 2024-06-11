import streamlit as st
import pandas as pd
import numpy as np
from pdf2image import convert_from_path
import google.generativeai as genai
from google.colab import userdata
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os
import re
import ast
from io import BytesIO
import xlsxwriter

GOOGLE_API_KEY = "AIzaSyCXaH9uGUWlRcwdKXZ3F-CKIZZU_BnWPQI"

genai.configure(api_key=GOOGLE_API_KEY)
system_prompt = """
               You are a specialist in comprehending receipts.
               Input images in the form of receipts will be provided to you,
               and your task is to respond to questions based on the content of the input image.
               """
attributes = []

# Model Configuration
MODEL_CONFIG = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

## Safety Settings of Model
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

def image_format(image_path):
    img = Path(image_path)

    if not img.exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [
        {
            "mime_type": "image/png",  ## Mime type are PNG - image/png. JPEG - image/jpeg. WEBP - image/webp
            "data": img.read_bytes()
        }
    ]
    return image_parts

model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=MODEL_CONFIG,
                              safety_settings=safety_settings)

def gemini_output(image_path, system_prompt, user_prompt):
    image_info = image_format(image_path)
    input_prompt = [system_prompt, image_info[0], user_prompt]
    response = model.generate_content(input_prompt)
    return response.text

st.set_page_config(
    page_title="XtractData",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)
col1, col2 = st.columns((3, 3))
with open("custom_style.css") as style_file:
    st.markdown(f"<style>{style_file.read()}</style>", unsafe_allow_html=True)

if 'dummy_data' not in st.session_state.keys():
    dummy_data = ['Invoice No', 'Name', 'Total']
    st.session_state['dummy_data'] = dummy_data
else:
    dummy_data = st.session_state['dummy_data']

def checkbox_container(data):
    colm = st.columns(2)
    with colm[0]:
        new_data = st.text_input('Add another attribute')
    cols = st.columns(3)
    if cols[0].button('  Add   '):
        if len(new_data) > 0 and new_data not in dummy_data:
            dummy_data.append(new_data)
        elif new_data in dummy_data:
            st.warning("Id already there")
    if cols[1].button('Select All'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = True
        st.experimental_rerun()
    if cols[2].button('UnSelect All'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = False
        st.experimental_rerun()
    for i in data:
        st.checkbox(i, key='dynamic_checkbox_' + i)

def get_selected_checkboxes():
    return [i.replace('dynamic_checkbox_', '') for i in st.session_state.keys() if
            i.startswith('dynamic_checkbox_') and st.session_state[i]]

def convert_list_to_string(lst):
    return ', '.join([str(item) for item in lst])

def main():
    attributes = get_selected_checkboxes()

    with col1:
        st.title("Invoice Entity Extractor")

        uploaded_files = st.sidebar.file_uploader("Upload a PDF file", accept_multiple_files=True, type="pdf")

        if uploaded_files:
            checkbox_container(dummy_data)

            st.divider()  # 👈 Draws a horizontal rule
            if st.button("Generate"):
                final_data = []
                df = pd.DataFrame()
                with tempfile.TemporaryDirectory() as temp_dir:
                    for i, uploaded_file in enumerate(uploaded_files):
                        try:
                            # Construct the full file path
                            file_path = os.path.join(temp_dir, uploaded_file.name)

                            # Save the file to the temporary directory
                            with open(file_path, 'wb') as f:
                                f.write(uploaded_file.getvalue())

                            # Load the PDF file using PyPDFLoader
                            loader = PyPDFLoader(file_path)
                            docs = loader.load()

                            pdf_path = file_path
                            images = convert_from_path(pdf_path)
                            image = images[0]
                            image_filename = f"image_{i + 1}.jpg"
                            image.save(image_filename, "JPEG")
                            attributes_string = convert_list_to_string(attributes)
                            user_prompt = attributes_string + "?. Give me in the form of dictionary"
                            image_path = image_filename

                            data = gemini_output(image_path, system_prompt, user_prompt)
                            pattern = r'({.*?})'
                            matches = re.findall(pattern, data, re.DOTALL)
                            extracted_dict = ast.literal_eval(matches[0])
                            print(extracted_dict)
                            print(attributes_string)
                            final_data.append(extracted_dict)

                        except Exception as e:
                            st.error(f"Error processing file {uploaded_file.name}: {e}")

                    df = pd.DataFrame(final_data)

                    # Convert DataFrame to Excel and then to bytes for download
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False)
                    output.seek(0)

                    # Provide the download button
                    st.download_button(
                        label="Download file",
                        data=output,
                        file_name="output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

    with col2:
        if uploaded_files:
            if len(attributes) > 0:
                df = pd.DataFrame('', index=range(5), columns=attributes)
                styler = df.style.set_properties(**{'border': '1px solid black', 'text-align': 'center'})

                st.dataframe(styler)

if __name__ == "__main__":
    main()
