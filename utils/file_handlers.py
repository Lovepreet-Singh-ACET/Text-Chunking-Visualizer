import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_file(uploaded_file):
    """Extract text from a plain text file."""
    return io.StringIO(uploaded_file.getvalue().decode("utf-8")).read()
