import os
import requests
import pandas as pd
import pdfplumber
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class BorderToCoastScraper:
    BASE_URL = "https://www.bordertocoast.org.uk/publications/?_sfm_publication_document_type=Fund+Holdings&sf_paged={}"
    DOMAIN = "https://www.bordertocoast.org.uk"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    def __init__(self, start_page=1, end_page=1, save_folder="Data/raw_data/bordertocoast_data/pdf"):
        """
        Initializes the scraper.
        :param start_page: First page to scrape
        :param end_page: Last page to scrape
        :param save_folder: Folder to save downloaded files
        """
        self.start_page = start_page
        self.end_page = end_page
        self.save_folder = save_folder
        os.makedirs(self.save_folder, exist_ok=True)

    def get_document_links(self):
        """
        Scrapes document links from the Border to Coast publications page.
        :return: List of properly formatted document links
        """
        document_links = []

        for page in range(self.start_page, self.end_page + 1):
            url = self.BASE_URL.format(page)
            response = requests.get(url, headers=self.HEADERS)
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all <a> tags with document links
            links = soup.find_all("a", href=True)
            for link in links:
                href = link["href"].strip()

                # Convert relative URLs to absolute
                full_url = href if href.startswith("http") else urljoin(self.DOMAIN, href)

                # Only add valid document links
                if full_url.endswith((".pdf", ".xls", ".xlsx")):
                    document_links.append(full_url)

            print(f"✅ Scraped page {page}: Found {len(document_links)} documents so far.")

        # Remove duplicates
        document_links = list(set(document_links))
        print(f"✅ Total unique documents found: {len(document_links)}")
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
            try:
                response = requests.get(link, headers=self.HEADERS, timeout=10)
                response.raise_for_status()

                with open(filename, "wb") as f:
                    f.write(response.content)

                file_paths.append(filename)
                print(f"📥 Downloaded: {filename}")

            except requests.exceptions.RequestException as e:
                print(f"❌ Failed to download {link}: {e}")

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


def webscraper(start_page=1,end_page=2):
    # Initialize scraper
    scraper = BorderToCoastScraper(start_page=start_page, end_page=end_page)
    document_links = scraper.get_document_links()
    
    if document_links:
        files = scraper.download_files(document_links)
        
        #extractor = DataExtractor()
        for file in files:
            if file.endswith(".pdf"):
                print(f"Extracting data from {file}...")

            elif file.endswith((".xls", ".xlsx")):
                print(f"Extracting Excel data from {file}...")

    else:
        print("❌ No documents found.")

# Main Execution
if __name__ == "__main__":
    webscraper()
