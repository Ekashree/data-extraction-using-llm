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
### API Keys
Create an Google API Key using following link:
https://aistudio.google.com/app/apikey

Add the generated API key in the google colab notebook.
On update of the API Key also update the app.py accordingly
### Usage
1. Open the google colab and install the relevant packages.
2. Upload the main.py and custom_style.css file on the google colab
3. Run the Streamlit application
4. On running the application, an IP address will be generated along with a link. Click on the link and paste the IP address in the text box and click on the submit.
5. Upload PDF files using the file uploader in the sidebar.
6. Select the attributes you want to extract from the PDFs.
7. Click the "Generate" button to process the uploaded files and extract the data.
8. Once the excel file is created, a download button will appear.
9. Click on the download button to download the excel sheet. By default the name of the output file is oulput.xlsx

invoice-entity-extractor/

├── app.py                    # Main application script

├── requirements.txt          # Required Python packages

├── custom_style.css          # Custom CSS for Streamlit UI

└── README.md                 # Project README file

### License
This project is licensed under the MIT License. See the LICENSE file for more information.
