import os
import requests
import pandas as pd
import pdfplumber
from bs4 import BeautifulSoup

class BrunelScraper:
    BASE_URL = "https://www.brunelpensionpartnership.org/document_category/holdings-report/page/{}/?s_year&is_document_search=1&post_type=document"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    def __init__(self, pages=1, save_folder="Data/raw_data/brunel_data"):
        """
        Initializes the scraper.
        :param pages: Number of pages to scrape
        :param save_folder: Folder to save downloaded files
        """
        self.pages = pages
        self.save_folder = save_folder
        os.makedirs(self.save_folder, exist_ok=True)

    def get_document_links(self):
        """
        Scrapes document links from the specified number of pages.
        :return: List of document links
        """
        document_links = []
        for page in range(1, self.pages + 1):
            url = self.BASE_URL.format(page)
            response = requests.get(url, headers=self.HEADERS)
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)

            for link in links:
                href = link["href"]
                if href.endswith((".pdf", ".xls", ".xlsx")):
                    document_links.append(href)

            print(f"✅ Scraped {len(document_links)} documents from page {page}")

        return document_links

    def download_files(self, links):
        """
        Downloads files from extracted links.
        :param links: List of file URLs
        :return: List of downloaded file paths
        """
        file_paths = []
        for link in links:
            filename = os.path.join(self.save_folder, os.path.basename(link))
            response = requests.get(link, headers=self.HEADERS)

            with open(filename, "wb") as f:
                f.write(response.content)

            file_paths.append(filename)
            print(f"📥 Downloaded: {filename}")

        return file_paths


class DataExtractor:
    @staticmethod
    def extract_pdf_data(pdf_path):
        """
        Extracts tables from a PDF file.
        :param pdf_path: Path to the PDF file
        :return: List of extracted tables
        """
        with pdfplumber.open(pdf_path) as pdf:
            all_tables = []
            for page in pdf.pages:
                tables = page.extract_tables()
                all_tables.extend(tables)

        return all_tables

    @staticmethod
    def extract_excel_data(excel_path):
        """
        Extracts data from an Excel file.
        :param excel_path: Path to the Excel file
        :return: Pandas DataFrame
        """
        df = pd.read_excel(excel_path, engine="openpyxl")
        return df


def webscraper(num_pages=1):
    # Initialize scraper
    scraper = BrunelScraper(pages=num_pages)
    document_links = scraper.get_document_links()
    
    if document_links:
        files = scraper.download_files(document_links)
        
        #extractor = DataExtractor()
        for file in files:
            if file.endswith(".pdf"):
                print(f"Extracting data from {file}...")
                #pdf_data = extractor.extract_pdf_data(file)
                

            elif file.endswith((".xls", ".xlsx")):
                print(f"Extracting Excel data from {file}...")
                #excel_data = extractor.extract_excel_data(file)
                

    else:
        print(" No documents found.")


# Main Execution
if __name__ == "__main__":
    webscraper()
    
