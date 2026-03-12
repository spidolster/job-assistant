import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a given PDF file path.
    Args:
        pdf_path (str): The path to the PDF file.
    Returns:
        str: The extracted text combined from all pages.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
    
    return text.strip()

# Optional: Add a function to handle in-memory uploaded files from Streamlit
def extract_text_from_uploaded_pdf(uploaded_file) -> str:
    """
    Extracts text from a Streamlit UploadedFile object.
    Args:
        uploaded_file: Streamlit UploadedFile object.
    Returns:
        str: The extracted text combined from all pages.
    """
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error extracting text from uploaded PDF: {e}")
        return ""
    
    return text.strip()
