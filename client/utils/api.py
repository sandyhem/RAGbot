import requests
from config import API_URL

def upload_pdfs_api(files):
    files_payload = [("files", (f.name,f.read(),"application/pdf")) for f in files]
    return requests.post(f"{API_URL}/upload_pdfs/", files=files_payload)

def ask_question_api(question, role):
    data = {"question": question, "role": role}
    return requests.post("http://localhost:8000/ask/", data=data)

def clear_knowledge_api():
    response = requests.post("http://localhost:8000/clear_knowledge/")
    return response
