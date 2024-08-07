from pdfminer.high_level import extract_text

# Path to the PDF file
pdf_path = r'Document Analysis/data/celebrity.pdf'

# Extract text from the PDF
extracted_text = extract_text(pdf_path)

# # Store the extracted text in a variable
text_variable = extracted_text
# print(text_variable[1380:1400])
# Print the extracted text (optional)
with open(r'Document Analysis/data/celebrity.txt', 'w', encoding="utf-8") as file:
    file.write(text_variable)

