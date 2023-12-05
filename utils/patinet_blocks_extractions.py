blocks = {
    "History of Present Illness": {
        "start_word_list": ["history of present illness",  "history of present lliness" ],
        "end_word_options": ["past medical history","surgical history", "assessment and plan"]
    },
    "AssessmentAndPlan": {
        "start_word_list": ["assessment:"],
        "end_word_options" : ["icd:","cpt codes:"]
    },
    "Vitals": {
        "start_word_list": ["vitals"],
        "end_word_options": ["physical examination"]
    },
     "Orders": {
        "start_word_list": ["orders:"],
        "end_word_options": ["Right ankle pain", "Left ankle pain", "Foot discomfort","labs ordered","assessment and plan",]
    },
     "Radiology Ordered": {
        "start_word_list": ["radiology ordered"],
        "end_word_options": ["radiology reviewed:",]
    },
    "E&M_Time_Factor": {
        "start_word_list": ["e and m time factor/ medical decision making notes:", "E and M Time Factor/ Medical Decision Making Notes:"],
        "end_word_options": ["follow up:","Follow up:"]

    }
}


def clean_string(value):
    # Check if the value is None or consists of unwanted characters
    if value is None or value.strip() in ['', '\n', '/n', '\t', '/t']:
        return None
    else:
        return value.strip()

from utils.azure_form_recognition import form_recognition_for_ocr
from utils.pdf_extraction_dependencies import process_raw_text


def patient_detail_extraction(pdf_path, file_name):
    endpoint = 'https://venex-formrecognizer.cognitiveservices.azure.com/'
    key = '883e40e7002947caad4b0695be22b71d'

    artifacts_directory = "artifacts/extracted_text"
    raw_text, file_name= form_recognition_for_ocr(pdf_path, file_name,endpoint, key, artifacts_directory)



    # Create a dictionary to store block values for the current file
    file_blocks_values = {}
    raw_text = raw_text.lower()
    # Iterate through all blocks
    for key, value in blocks.items():
        if key == "AssessmentAndPlan":
            if "assessment:" in raw_text:
                start_index = raw_text.find("assessment:")
                new_text_from_assessment = raw_text[start_index:]
                result = process_raw_text(
                    new_text_from_assessment, start_word_list=value["start_word_list"], end_word_list=value["end_word_options"])
        else:
            result = process_raw_text(
                    raw_text, start_word_list=value["start_word_list"], end_word_list=value["end_word_options"])


        # Process the PDF file and extract text based on the block
        # pdf_file_path = os.path.join(pdf_file_path)
        
        # Store the result in the dictionary for the current block
        file_blocks_values[key] = result

    # Print or use the block values for the current file
    # print("filename: ", filename)
    block_dict = {}
    extracted_block_content = ''
    for block_name, content in file_blocks_values.items():
        content = clean_string(content)
        block_dict[block_name] = content
        extracted_block_content += f'{block_name}:\n{content}\n'
    # txt_path = f"extracted_text/{file_name}.txt"
    all_block_txt_path = f"artifacts/extracted_text/extract_block/all_blocks/{file_name}.txt"

    with open(all_block_txt_path, "w",  encoding="utf-8", errors="ignore") as file:
        file.write(extracted_block_content)


    extracted_block_content = ''
    # multiple cpt code needed blocks 
    mutlti_cpt_block_list  = ["Orders", "Radiology Ordered", "E&M_Time_Factor"]
    for key in block_dict:
        if key in mutlti_cpt_block_list and block_dict[key] is not None:
            extracted_block_content +=  f'\n{block_dict[key]}\n'

    order_block_txt_path = f"artifacts/extracted_text/extract_block/orders_block/{file_name}.txt"

    with open(order_block_txt_path, "w",  encoding="utf-8", errors="ignore") as file:
        file.write(extracted_block_content)

    return all_block_txt_path, order_block_txt_path, block_dict



