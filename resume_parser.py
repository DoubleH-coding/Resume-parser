import re
import PyPDF2
from docx import Document
import spacy

nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_resume(file_path):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file format"}
    
    # Basic information extraction
    doc = nlp(text)
    name = ""
    email = ""
    phone = ""
    skills = []
    
    # Extract name (first proper noun)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break
    
    # Extract email and phone
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email.group(0) if email else ""
    
    phone = re.search(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', text)
    phone = phone.group(0) if phone else ""
    
    # Simple skills detection (customize this list)
    skill_keywords = ['python', 'java', 'c++', 'machine learning', 'flask', 'django']
    for skill in skill_keywords:
        if skill.lower() in text.lower():
            skills.append(skill)
    
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "raw_text": text[:500] + "..."  # Show first 500 chars
    }
