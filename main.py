# Web Scraping
from web_scrapers import bordercoast_data_webscraping
from web_scrapers import brunel_data_webscraping

# Data Analysis
from Data_Analyzer.Brunel_LGPS_data_analysis import run as Brunel_DA_run
from Data_Analyzer.Bordertocoast_LGPS_data_analysis import run as Bordertocoast_DA_run
from Data_Analyzer.data_compiler import compile_financial_data # 1st Report
from Data_Analyzer.fix_LGPS_btc_report import main as restructure_report # 2nd Report 
from Data_Analyzer.fix_LGPS_b_report import BrunelDataAnalyzer # 2nd Report
from Data_Analyzer.final_compliler import main as final_report # Final Report

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

    # Reports for Bordertocoast
    ## Compilling data together
    input_folderbtc1 = "Data/processed_data/bordertocoast_data/documents/"  # Adjusted path
    output_filebtc1 = "Data/processed_data/bordertocoast_data/reports/supporting_documents/LGPS_Compiled_Financial_Report.docx"
    compile_financial_data(input_folderbtc1, output_filebtc1)
    ## Restructuring Report
    input_folderbtc2 = "Data/processed_data/bordertocoast_data/reports/supporting_documents/"
    output_filebtc2 = "Data/processed_data/bordertocoast_data/reports/supporting_documents/"
    restructure_report(input_folderbtc2, output_filebtc2)
    ## Final Report
    input_folderbtc3 = "Data/processed_data/bordertocoast_data/reports/supporting_documents/"
    output_filebtc3 = "Data/processed_data/bordertocoast_data/reports/Output/"
    final_report(input_folderbtc3, output_filebtc3)

    
    # Reports for Brunel
    ## Compilling data together
    input_folderb1 = "Data/processed_data/brunel_data/documents/"  # Adjusted path
    output_fileb1 = "Data/processed_data/brunel_data/reports/supporting_documents/LGPS_Compiled_Financial_Report.docx"
    compile_financial_data(input_folderb1, output_fileb1)
    ## Final Report
    input_folderb2 = "Data/raw_data/brunel_data/"
    output_fileb2 = "Data/processed_data/brunel_data/reports/Output/"
    supporting_files_dir1 = 'Data/processed_data/brunel_data/reports/supporting_files/'
    BrunelDataAnalyzer(input_folderb2, output_fileb2, supporting_files_dir1).run_analysis()

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