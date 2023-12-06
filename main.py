import streamlit as st
import base64
from utils.patinet_blocks_extractions import patient_detail_extraction
from utils.llm_calling import get_the_llm_response_for_mdm
from utils.llm_for_cpt_code import detect_cpt_codes_
import pandas as pd
 

# Step 1: Read the Excel file into a pandas DataFrame
excel_file_path = 'xl_file/Agile_Charge_Details..xlsx'
df = pd.read_excel(excel_file_path)


def matching_xl_claim_id(file_id):  
    # Convert 'Claim ID' column to strings
    df['Claim ID'] = df['Claim ID'].astype(str)
    
    matching_indices = df[df['Claim ID'].str.lower().str.strip() == file_id.lower()].index
    
    if not matching_indices.empty:
        # Fetch values from the 'CPT' column for the matching indices
        matched_cpt_values = df.loc[matching_indices, 'CPT'].tolist()
        return matched_cpt_values
    else:
        print("Not matched idsd")


 
def display_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_content = base64.b64encode(pdf_file.read()).decode('utf-8')
        html_code = f'<iframe src="data:application/pdf;base64,{pdf_content}" width="100%" height="600px"></iframe>'
        st.markdown(html_code, unsafe_allow_html=True)
   
 
def main():    
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        pdf_binary_content = uploaded_file.read()
        file_name = uploaded_file.name
        file_id = file_name.split("/")[-1].split("_")[0]
        existing_cpt=matching_xl_claim_id(file_id)
        output_path = f"artifacts/uploaded_docs/{file_id}.pdf"

        # Write the binary content to the specified path
        with open(output_path, 'wb') as output_file:
            output_file.write(pdf_binary_content)
           
        display_pdf(output_path)
        st.markdown(f'<p style="color: yellow; font-size: 18px; font-weight: bold;">Existing CPT Code</p>', unsafe_allow_html=True)

        # Existing CPT CODE
        existing_cpt='\n'.join(map(str,existing_cpt))
        st.text_area(label = "", value=existing_cpt, height=100)

        all_block_txt_path, order_block_txt_path, block_dict = patient_detail_extraction(output_path, file_id)
        llm_response_for_mdm = get_the_llm_response_for_mdm(all_block_txt_path)


        st.markdown(f'<p style="color: yellow; font-size: 18px; font-weight: bold;">AI MDM Suggetion</p>', unsafe_allow_html=True)

        st.text_area(label = "", value=llm_response_for_mdm, height=200)
        if block_dict["Orders"] != None or block_dict["Radiology Ordered"] != None or block_dict["E&M_Time_Factor"] != None:
            # print("order block exist")
            print("order block path", order_block_txt_path)
            cpt_codes_list, llm_response_for_cpt_codes = detect_cpt_codes_(
                order_block_txt_path, model="gpt-4", temperature=0)
            try:
                extracted_block_content = ""
                for each in cpt_codes_list:
                    for block_name, content in each.items():
                        block_dict[block_name] = content
                        extracted_block_content += f'{block_name}:\n\n{content}\n'
            except:
                extracted_block_content = llm_response_for_cpt_codes
        else:
            extracted_block_content = ""

        st.markdown(f'<p style="color: yellow; font-size: 18px; font-weight: bold;">CPT Code Suggetion</p>', unsafe_allow_html=True)
        if extracted_block_content:
            
            st.text_area(label="", value=extracted_block_content, height=200)
        else:
            st.write("There are no CPT Codes.")

        if "WC002" in existing_cpt:
            st.markdown("<h4 style='color: White;'>This case is associated with Worker's Compensation</h4>", unsafe_allow_html=True)
            st.text_area(label = "", value="WC002", height=100)
        else:
            st.markdown("<h4 style='color: red;'>This case is not associated with Worker's Compensation</h4>", unsafe_allow_html=True)



if __name__ == "__main__":
    main()