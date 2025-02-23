import pandas as pd
import PyPDF2
import re

class LGPSPDFProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.data = []
        self.current_fund_type = None

    def extract_text(self):
        """Extracts text from each page of the PDF using PyPDF2."""
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                self.process_page(text)

    def process_page(self, text: str):
        """Processes the text of a page, identifies fund types and extracts data."""
        # Check for a fund type at the top of the page
        fund_type_match = re.search(r"(All World Climate Factor Fund|Global Active Emerging Market Bond Fund|Global Active Investment Grade Corporate Bond Multi Manager Fund|Global Active Multi Asset Credit Fund|Global Equity Active Multi Manager Fund|Global Ex UK Passive Equity Fund|Global Multi Factor Equity Index Fund|Global Sustainable Equity Active Broad Fund|Global Sustainable Equity Active Targeted Fund|Global Sustainable Equity Active Thematic Fund|UK Equity Passive Fund|Emerging Markets Equity Active Multi Manager Fund)", text, re.IGNORECASE)
        if fund_type_match:
            self.current_fund_type = fund_type_match.group(0)

        # Extract rows of data under the current fund type
        data_lines = re.findall(r"(\w+)\s+([A-Z0-9]+)\s+([A-Z0-9]+)\s+([A-Z0-9]+)\s+(.+?)\s+(\d+[,.\d]*)\s+(\d+[,.\d]*)\s+(\w+)\s+([\d.]+)", text)
        for line in data_lines:
            self.data.append((self.current_fund_type,) + line)

    def to_dataframe(self) -> pd.DataFrame:
        """Converts the extracted data to a pandas DataFrame."""
        columns = ["Fund Type", "Country", "Security Identifier", "SEDOL", "ISIN", "Description", "Market Value", "Shares", "Currency", "Rate"]
        df = pd.DataFrame(self.data, columns=columns)
        return df

    def save_to_csv(self, output_path: str):
        """Saves the extracted data to a CSV file."""
        df = self.to_dataframe()
        df.to_csv(output_path, index=False)

if __name__ == '__main__':
    pdf_processor = LGPSPDFProcessor('Data/raw_data/lgpscentral_data/pdf/2024-08_ACS-Investments_v1.pdf')
    pdf_processor.extract_text()
    df = pdf_processor.to_dataframe()
    pdf_processor.save_to_csv('Data/processed_data/lgpscentral_data/LGPS_Fund_Data.csv')
    print('Data extraction completed and saved to LGPS_Fund_Data.csv')
