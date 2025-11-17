import io
from PyPDF2 import PdfReader
from PIL import Image

def extract_file_content(uploaded_file):
    """
    Primește un st.file_uploader și returnează conținutul în funcție de tipul fișierului.
    """
    if uploaded_file is None:
        return None

    filename = uploaded_file.name
    extension = filename.split('.')[-1].lower()

    if extension in ["txt", "csv", "json"]:
        # Citește fișiere text
        content = uploaded_file.read().decode("utf-8")
        return {"type": "text", "content": content}

    elif extension == "pdf":
        # Citește fișiere PDF
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return {"type": "pdf", "content": text}

    elif extension in ["png", "jpg", "jpeg"]:
        # Fișiere imagine
        image = Image.open(uploaded_file)
        return {"type": "image", "content": image}

    else:
        # Alte tipuri
        return {"type": "binary", "content": uploaded_file.getbuffer()}