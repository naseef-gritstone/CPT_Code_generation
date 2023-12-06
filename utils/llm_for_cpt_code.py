
from llama_index import (
    SimpleDirectoryReader,
    ServiceContext,
    get_response_synthesizer,
    VectorStoreIndex
)
from llama_index.indices.document_summary import DocumentSummaryIndex
from llama_index.llms import OpenAI
import os
import openai
import ast
import re


client = openai.api_key = "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"


# summary_query_prompt  = """give the exact  CPT codes as array for the below patient details"""


summary_query_prompt = """
# give the exact  CPT codes as array for the below patient details and provide the reason


remaing_mederp_prompt = "Parse the specified data to find Current Procedural Terminology (CPT) and organize them into a JSON format. Populate the following fields with appropriate values. Ensure that the key names remain unchanged. If information is unavailable, use 'nill':

CPT Codes (array of objects containing 'code', 'description' for each procedure) """


def detect_cpt_codes_(file_path, model, temperature):

    document = SimpleDirectoryReader(input_files=[file_path]).load_data()
    
    doc_unique_id = "current_doc"

    document[0].doc_id = doc_unique_id
    print("entered on tree index for objective extraction")
    # # LLM Predictor (gpt-3.5-turbo)
    chatgpt = OpenAI(temperature=temperature, model=model)
    service_context = ServiceContext.from_defaults(
        llm=chatgpt, chunk_size=1024)

    # default mode of building the index
    response_synthesizer = get_response_synthesizer(
        response_mode="tree_summarize", use_async=False
    )
    summary_query = (
        summary_query_prompt
    )
    doc_summary_index = DocumentSummaryIndex.from_documents(
        document,
        service_context=service_context,
        response_synthesizer=response_synthesizer,
        summary_query=summary_query
    )
    # print("doc", doc)

    response_llm = doc_summary_index.get_document_summary(doc_unique_id)
    # Extract the list using ast.literal_eval
    try:
        # Use regular expression to extract content between '[' and ']'
        match = re.search(r'\[([^\]]*)\]', response_llm)
        if match:
            try:
                result_list = ast.literal_eval(match.group(0))
                if isinstance(result_list, list):
                    # result_list = [item.strip() for item in result_list]
                    return result_list, response_llm
                else:
                    print(
                        "unable to convert llm response for the cpt codes to  the list", response_llm)
            except (SyntaxError, ValueError) as e:
                print(f"Error extracting list: {e}")
        else:
            print("No list found in the string.")

        # print(result_list)

    except (SyntaxError, ValueError) as e:
        print(f"Error extracting list: {e}")
        return False, str(e)
    # return response_llm