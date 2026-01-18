from langchain_openai import ChatOpenAI
from src.config import settings
from src.rag.prompts import admission_prompt

def generate_decision(context_text: str, question: str):
    """
    Calls the LLM with the manually constructed context.
    """
    # 1. Initialize LLM
    llm = ChatOpenAI(
        model_name=settings.openai_model,
        temperature=0,
        api_key=settings.OPENAI_API_KEY
    )
    
    # 2. Format the Prompt
    # FIX: Changed 'input=' to 'question=' to match the {question} placeholder
    final_prompt_value = admission_prompt.format(
        context=context_text,
        question=question 
    )
    
    # 3. Call LLM
    response_message = llm.invoke(final_prompt_value)
    
    return response_message.content

