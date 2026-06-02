import PyPDF2

def extract_text_from_pdf(file_path):
    text = ""

    try:
        pdf = PyPDF2.PdfReader(file_path)

        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    except Exception as e:
        print("❌ Error extracting PDF:", e)

    return text
