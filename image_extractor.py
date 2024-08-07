import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO

# Path to the PDF file
pdf_path = r'Document Analysis\data\institute.pdf'

# Open the PDF file
pdf_document = fitz.open(pdf_path)

# Iterate through each page in the PDF
for page_num in range(len(pdf_document)):
    # Get the page
    page = pdf_document.load_page(page_num)
    # Get the images on the page
    images = page.get_images(full=True)

    # Iterate through each image
    for img_index, img in enumerate(images):
        # Get the XREF of the image
        xref = img[0]
        # Extract the image bytes
        base_image = pdf_document.extract_image(xref)
        image_bytes = base_image["image"]

        # Use PIL to open the image
        image = Image.open(BytesIO(image_bytes))

        # Print the dimensions of the image
        print(f"Page {page_num + 1}, Image {img_index + 1}: {image.size}")

pdf_document.close()
