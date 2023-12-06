from llama_index import VectorStoreIndex, SimpleDirectoryReader
from openai import OpenAI
from llama_index.llms import OpenAI
from llama_index.response_synthesizers import get_response_synthesizer
from utils.llm_utils.custom_rag import RAGStringQueryEngine, qa_prompt
import openai
import os


# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")
def get_the_llm_response_for_mdm(txt_path):
    # Load documents and build index
    documents = SimpleDirectoryReader(input_files=[txt_path]).load_data()
    index = VectorStoreIndex.from_documents(documents)

    # llm = OpenAI(model="gpt-3.5-turbo-instruct")
    llm = OpenAI(model="gpt-4")
    index = VectorStoreIndex.from_documents(documents)
    synthesizer = get_response_synthesizer(response_mode="compact")
    retriever = index.as_retriever()
    query_engine = RAGStringQueryEngine(
        retriever=retriever,
        response_synthesizer=synthesizer,
        llm=llm,
        qa_prompt=qa_prompt,
    )

    response = query_engine.query("Describe the MDM Level for this patient based on the given MDM Rules. give Corresponding CPT Code and it's descrition")
    # response = query_engine.query("Given the patient's medical history and symptoms, provide a detailed explanation of the Medical Decision Making (MDM) level. Include information about potential CPT codes, relevant diagnoses, and the reasoning behind the recommended procedures.")
    

    
    
    return response