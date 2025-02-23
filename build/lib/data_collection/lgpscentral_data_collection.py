import os
import pandas as pd
import pdfplumber

class PDFToExcelConverter:
    """
    A class to parse specific tabular data from a PDF file and convert it into an Excel file.
    """

    def __init__(self, file_path: str, output_directory: str = "Data/extracted_data"):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path).replace(".pdf", ".xlsx")
        self.output_directory = output_directory

        # Ensure the output directory exists
        os.makedirs(self.output_directory, exist_ok=True)

        # Define fixed headers as per the PDF structure
        self.fixed_header = [
            "Date", "Fund Name", "SEDOL", "Security Description", 
            "Max of Local Price", "Shares/Par", "Base Value"
        ]

    def extract_text_from_pdf(self) -> list:
        """
        Extract tabular data from the PDF file using pdfplumber.

        Returns:
            list: A list of rows extracted from the PDF, including headers and data rows.
        """
        extracted_data = []
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        lines = [line.strip() for line in text.split('\n') if line.strip()]
                        extracted_data.extend(lines)
                        print(f"Extracted {len(lines)} lines from page {page_num + 1}")
        except Exception as e:
            print(f"Failed to extract text from {self.file_name}: {e}")
        return extracted_data

    def parse_to_dataframe(self, extracted_data: list) -> pd.DataFrame:
        """
        Parse the extracted text into a structured DataFrame using fixed headers.

        Args:
            extracted_data (list): Raw lines of text extracted from the PDF.

        Returns:
            pd.DataFrame: A DataFrame with the structured data.
        """
        data_rows = []

        for line in extracted_data:
            # Split the line into columns, considering possible whitespace and formatting issues
            columns = line.split(maxsplit=6)  # Split into exactly 7 columns
            
            # Check if the line is a valid data row (not a header or malformed row)
            if len(columns) == len(self.fixed_header) and columns[0] != "Date":
                data_rows.append(columns)
            elif len(columns) != len(self.fixed_header):
                print(f"Skipping malformed row: {line}")

        # Create a DataFrame from the data rows
        df = pd.DataFrame(data_rows, columns=self.fixed_header)
        
        # Convert numeric columns to appropriate types
        numeric_columns = ["Max of Local Price", "Shares/Par", "Base Value"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')

        return df

    def save_to_excel(self, df: pd.DataFrame):
        """
        Save the parsed DataFrame to an Excel file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
        """
        output_path = os.path.join(self.output_directory, self.file_name)
        try:
            df.to_excel(output_path, index=False)
            print(f"Saved data to {output_path}")
        except Exception as e:
            print(f"Failed to save Excel file: {e}")

    def convert(self):
        """
        Full conversion pipeline from PDF to Excel.
        """
        extracted_data = self.extract_text_from_pdf()
        df = self.parse_to_dataframe(extracted_data)
        if not df.empty:
            self.save_to_excel(df)
        else:
            print("No valid data extracted from the PDF.")

# Example usage:
file_path = 'Data/raw_data/bordertocoast_data/Emerging-Markets-Equity-Alpha-Fund-March-2024-Fund-Holdings.pdf'
converter = PDFToExcelConverter(file_path)
converter.convert()
