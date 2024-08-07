import streamlit as st
from pdfminer.high_level import extract_text
from io import BytesIO
from document_analysis import generate_report



def main():
    st.title("🤖NewsReach")


    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
    
        pdf_path = 'temp.pdf'
        with open(pdf_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        
        extracted_text = extract_text(pdf_path)

      
        st.subheader("Extracted Text:")
        st.write(extracted_text)


        if st.button("Generate Report"):
            report = generate_report(extracted_text)
            st.subheader("Generated Report:")
            st.write(report)

if __name__ == "__main__":
    main()
