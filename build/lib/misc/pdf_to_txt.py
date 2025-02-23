import os
import pdfplumber

class PDFToTXTConverter:
    def __init__(self, input_folder: str, output_folder: str):
        """
        Initialize the converter with input and output folder paths.
        
        :param input_folder: Path to the folder containing PDF files.
        :param output_folder: Path to the folder to save TXT files.
        """
        self.input_folder = input_folder
        self.output_folder = output_folder
        self._create_output_folder()

    def _create_output_folder(self):
        """Create the output folder if it doesn't already exist."""
        os.makedirs(self.output_folder, exist_ok=True)

    def _get_pdf_files(self):
        """Retrieve all PDF files in the input directory."""
        return [
            f for f in os.listdir(self.input_folder) 
            if f.lower().endswith('.pdf')
        ]

    def _extract_text_from_pdf(self, pdf_file_path: str) -> str:
        """Extract text content from a PDF file using pdfplumber."""
        all_text = ''
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                all_text += page.extract_text() or ''
        return all_text

    def _save_text_to_file(self, text: str, txt_file_path: str):
        """Save the extracted text to a TXT file."""
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

    def convert_all_pdfs(self):
        """Convert all PDF files in the input folder to TXT files in the output folder."""
        pdf_files = self._get_pdf_files()

        if not pdf_files:
            print("No PDF files found in the input directory.")
            return

        for file_name in pdf_files:
            pdf_file_path = os.path.join(self.input_folder, file_name)
            txt_file_path = os.path.join(self.output_folder, file_name.replace('.pdf', '.txt'))

            print(f"Converting '{file_name}' to TXT...")
            text = self._extract_text_from_pdf(pdf_file_path)
            self._save_text_to_file(text, txt_file_path)
            print(f"Saved as '{txt_file_path}'")

        print("All PDF files have been converted to TXT files.")


# Example usage
if __name__ == '__main__':
    input_folder = 'Data/raw_data/bordertocoast_data/pdf'   # Replace with your input folder path
    output_folder = 'Data/raw_data/bordertocoast_data/txt' # Replace with your output folder path

    converter = PDFToTXTConverter(input_folder, output_folder)
    converter.convert_all_pdfs()
