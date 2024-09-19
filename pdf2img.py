import fitz  # PyMuPDF
import argparse
import os

def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    # Open the PDF file
    pdf = fitz.open(pdf_path)

    # Create a directory for the output if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through each page
    for page_number in range(len(pdf)):
        # Get the page
        page = pdf.load_page(page_number)

        # Render page to an image (pixmap) at the specified DPI
        pix = page.get_pixmap(dpi=dpi)

        # Save the image
        image_path = os.path.join(output_folder, f"page_{page_number+1}.png")
        pix.save(image_path)

    pdf.close()

def process_folder(folder_path, dpi):
    # List all PDF files in the folder
    for file in os.listdir(folder_path):
        if file.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file)
            output_folder = os.path.splitext(pdf_path)[0] + "_images"
            convert_pdf_to_images(pdf_path, output_folder, dpi)

def main():
    parser = argparse.ArgumentParser(description='Convert PDF pages in a folder to images.')
    parser.add_argument('--folder_path', type=str, required=True, help='Path to the folder containing PDF files')
    parser.add_argument('--dpi', type=int, default=300, help='DPI for converted images')
    args = parser.parse_args()

    folder_path = args.folder_path
    dpi = args.dpi
    process_folder(folder_path, dpi)

if __name__ == "__main__":
    main()
