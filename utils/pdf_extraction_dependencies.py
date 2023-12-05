#Reading the PDF file 
import os
import PyPDF2
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def split_string_between_two_strings(input_string, start_string, end_string):
    start_index = input_string.find(start_string)
    end_index = input_string.find(end_string)
    # print("start_index", start_index)
    # print("end index", end_index)
    try:
        result = input_string[start_index + len(start_string):end_index]
        return result
    except Exception as e:
        print(e)

def process_raw_text(raw_text, start_word_list, end_word_list):
    # result_text = extract_text_from_pdf(pdf_file_path)
    result_text = raw_text.lower()

    start_word = None
    for each in start_word_list:
        if each in result_text:
            start_word = each
            break

    if not start_word:
        print("Starting word element not found in extracted text")
        return None  # or return a default value or raise an exception, depending on your needs

    end_word = None
    for each in end_word_list:
        if each in result_text:
            end_word = each
            break

    if not end_word:
        print("End word element not found in extracted text")
        return None  # or return a default value or raise an exception, depending on your needs

    result = split_string_between_two_strings(result_text, start_word, end_word)
    return result
