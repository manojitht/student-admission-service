from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from src.config import settings
from src.rag.vectorstore import get_vectorstore

def get_rag_chain():
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    llm = ChatOpenAI(
        model_name=settings.LLM_MODEL,
        temperature=0,
        api_key=settings.OPENAI_API_KEY
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

