import os
from pathlib import Path
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import shutil

# PERSIST_DIR: Directory where the Chroma vectorstore is saved (./chroma_db).
# UPLOAD_DIR: Directory where uploaded PDFs are stored (./uploaded_pdfs).

PERSIST_DIR= "./chroma_db"
UPLOAD_DIR = "./uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Purpose: Handles uploaded PDF files, 
# extracts their content, splits them into chunks, generates embeddings, 
# and stores them in a persistent Chroma vectorstore.

def load_vectorstore(files):
    clear_data() 
    file_paths=[]
   
    for file in files:
       save_path = Path(UPLOAD_DIR) / file.filename
       with open(save_path, "wb") as f:
              f.write(file.file.read())
       file_paths.append(str(save_path ))

    docs=[]
    for path in file_paths:
           loader = PyPDFLoader(path)
           docs.extend(loader.load())
   
      # chunking the documents 
    text_splitter = RecursiveCharacterTextSplitter(
             chunk_size=1000,
             chunk_overlap=100)
    texts = text_splitter.split_documents(docs)
    
    embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L12-v2")

    # storing the embeddings in a persistent vectorstore
    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
           vectorstore = Chroma(
               persist_directory=PERSIST_DIR,
               embedding_function=embeddings
           )
           vectorstore.add_documents(texts)
    else:
              vectorstore = Chroma.from_documents(
                documents=texts,
                embedding=embeddings,
                persist_directory=PERSIST_DIR
              )
              vectorstore.persist()
    return vectorstore

def get_vectorstore(persist_directory, embedding_function):
    from langchain.vectorstores import Chroma
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function
    )

def clear_data():
    import shutil
    # Remove uploaded PDFs
    shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    # Remove vectorstore
    shutil.rmtree(PERSIST_DIR, ignore_errors=True)
    os.makedirs(PERSIST_DIR, exist_ok=True)