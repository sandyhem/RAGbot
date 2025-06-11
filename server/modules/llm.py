import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA


# Load environment variables from .env file
load_dotenv()

# Initialize the Groq model with the API key from environment variables

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_chain(vectorstore):
    """
    Create a retrieval-augmented generation (RAG) chain using the Groq model.
    
    Args:
        vectorstore: The vector store to use for retrieval.
    
    Returns:
        A retrieval-augmented generation chain.
    """
    llm = ChatGroq(
        model="llama3-70b-8192", 
        api_key=GROQ_API_KEY
    )

    retriever= vectorstore.as_retriever(
        search_kwargs={
            "k": 3,  # Number of documents to retrieve
        }
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
