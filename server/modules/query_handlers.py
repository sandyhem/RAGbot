from logger import logger

def query_chain(chain,user_input:str):
    try:
        logger.debug(f"Running chain for input: {user_input}")
        prompt = f"""You are a helpful assistant. Answer the following question using the provided documents.
Question: {user_input}
If you use any sources, list them at the end."""

        result = chain({"query": prompt})
        response = {
            "response" : result["result"],
            "sources":[doc.metadata.get("source","") for doc in result["source_documents"]]
        }
        logger.debug(f"Chain response: {response}")
        return response
    except Exception as e:
        logger.exception("Error in query_chain")
        raise
