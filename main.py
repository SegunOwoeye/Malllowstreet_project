# Web Scraping
from web_scrapers import bordercoast_data_webscraping
from web_scrapers import brunel_data_webscraping

# Data Analysis
from Data_Analyzer.Brunel_LGPS_data_analysis import run as Brunel_DA_run
from Data_Analyzer.Bordertocoast_LGPS_data_analysis import run as Bordertocoast_DA_run

# Misc Library Import
from misc.complete_file_del import run as del_unecessary_files
from misc.pdf_to_txt import PDFToTXTConverter
from misc.data_explaination import run as explain_data_run

import os


# Used for webscraping Data
def check_raw_data():
    # Define the path to the data folder
    data_folder_1 = "Data/raw_data/bordertocoast_data/pdf"
    data_folder_2 = "Data/raw_data/brunel_data"
    #data_folder_3 = "Data/raw_data/lgpscentral_data/pdf"

    # Check if the folder exists
    if not os.path.exists(data_folder_1):
        # Do bordertocoast_data web scraping
        bordercoast_data_webscraping.webscraper()

    if not os.path.exists(data_folder_2):
        # Do brunel_data web scraping
        brunel_data_webscraping.webscraper()

    """if not os.path.exists(data_folder_3):
        # Do lgpscentral_data web scraping
        lgpscenral_data_webscraping.webscraper()"""
        



# Processing and analysing data files
def lgps_data_analyzer():
    # Data Analysis for Brunel
    Brunel_DA_run()   

    # Data Analysis for Boardertocoast 
    Bordertocoast_DA_run()



# Main Function of Program
### If there has been no webscraping raw_data_generated = False
### If there has been webscraping raw_data_generated = True

def main(raw_data_generated=False):
    # Webscrapes if there's no data
    if raw_data_generated == False: # No Webscraping Done
        # [1] Gathering data
        check_raw_data()

        # [2] Delete Unecessary Files
        del_unecessary_files()

        

    # [3] Data Analysis
    lgps_data_analyzer()


    # [4] Generate an explaination of the data
    explain_data_run()



main()