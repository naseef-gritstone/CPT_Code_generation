
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import re


def process_dictionary_list(dictionary_list):
    unique_values = set()
    filtered_data = []
    for item in dictionary_list:
        value = item["Value"]
        if value not in unique_values:
            filtered_data.append(item)
            unique_values.add(value)

    return filtered_data




def read_pdf_as_bytes(file_path):
    with open(file_path, 'rb') as file:
        pdf_bytes = file.read()
    return pdf_bytes

def form_recognition_for_ocr(pdf_path, file_name ,endpoint, key, artifacts_directory):

    pdf_bytes = read_pdf_as_bytes(pdf_path)
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    poller = document_analysis_client.begin_analyze_document("prebuilt-document", pdf_bytes)

    result = poller.result()

    # key_value_list = []
    # for kv_pair in result.key_value_pairs:
    #     if kv_pair.key and kv_pair.value:
    #         temp_dic = {"Key": re.sub(r'\W+', ' ', kv_pair.key.content).strip(),
    #                     "Value": kv_pair.value.content,
    #                     # "page": kv_pair.key.bounding_regions[0].page_number,
    #                     # "confidence": kv_pair.confidence if kv_pair.confidence else 0
    #                     }
    #         key_value_list.append(temp_dic)

    # key_value_data = process_dictionary_list(key_value_list)

    raw_text = result.content

    # document_extracted_data = f"<document json data> \n {key_value_data} <Raw Data> \n {raw_text}"
    document_extracted_data = raw_text

    extracted_pdf_txt_path = f"{artifacts_directory}/{file_name}.txt"
    with open(extracted_pdf_txt_path, "w",  encoding="utf-8", errors="ignore") as file:
        file.write(document_extracted_data)

    return raw_text, file_name