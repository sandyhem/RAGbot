import logging
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from modules.load_vectorstore import load_vectorstore, get_vectorstore
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Ragbot API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def catch_exception_middleware(request: Request, call_next):
    try:
       return await call_next(request)
    except Exception as e:
        logger.exception("Unhandled exception occurred")
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error", "error": str(e)}
        )
    

@app.post("/upload_pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        logger.info(f"Received {len(files)} files for upload")
        load_vectorstore(files)
        logger.info("document loaded successfully into chroma db -vectorstore")
        return {"message": "Files processed and vectorstore updated"}
    except Exception as e:
        logger.exception("Error processing files in pdf upload")
        return JSONResponse(
            status_code=500,
            content={"message": "Error processing files", "error": str(e)}
        )
    
@app.post("/ask/")
async def ask_questtion(question: str = Form(...)):
    try:
        logger.info(f"User question: {question}")
        from langchain.embeddings import HuggingFaceBgeEmbeddings
        from modules.load_vectorstore import PERSIST_DIR

        vectorstore = get_vectorstore(
            persist_directory=PERSIST_DIR,
            embedding_function=HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L12-v2")
        )
        chain = get_llm_chain(vectorstore)
        result = query_chain(chain, question)
        logger.info("Response generated successfully")
        return result

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(
            status_code=500,
            content={"message": "Error processing question", "error": str(e)}
        )

@app.get("/test")
async def test():
    return {"message": "Hello, World!"}
