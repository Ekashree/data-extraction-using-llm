## Data Extraction using LLM
This project is an Invoice Entity Extractor that processes uploaded PDF invoices, extracts relevant data using Google Generative AI (Gemini Pro Vision), and provides the extracted data for download in an Excel format. The application is built using Streamlit for the user interface, and it leverages various Python libraries for PDF processing and data manipulation.
### Features
* PDF Upload: Upload multiple PDF files.
* Attribute Selection: Select attributes to extract from the invoices.
* AI Processing: Extract data from invoices using Google Generative AI.
* Data Standardization: Ensure uniform data formats.
* Data Download: Download the extracted data in Excel format.
### Setup and Installation
* Python 3.7+
* Streamlit
* pandas
* numpy
* pdf2image
* google.generativeai
* PyPDFLoader
* xlsxwriter
### Installation
Clone the repository:
https://github.com/Ekashree/data-extraction-using-llm.git
### Usage
1. Run the Streamlit application:
streamlit run app.py
2. Open your web browser and navigate to http://localhost:8501.
3. Upload PDF files using the file uploader in the sidebar.
4. Select the attributes you want to extract from the PDFs.
5. Click the "Generate" button to process the uploaded files and extract the data.
6. Download the extracted data in Excel format by clicking the "Download file" button.

invoice-entity-extractor/

├── app.py                    # Main application script

├── requirements.txt          # Required Python packages

├── custom_style.css          # Custom CSS for Streamlit UI

└── README.md                 # Project README file

### License
This project is licensed under the MIT License. See the LICENSE file for more information.
