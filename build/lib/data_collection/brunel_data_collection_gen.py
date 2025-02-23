import os
import pandas as pd


class FileDataExtractor:
    """
    A class to search for files in a directory and extract data from Excel files.
    """

    def __init__(self, pattern="*.xlsx", recursive=False):
        self.directory = "Data/raw_data/brunel_data"
        self.pattern = pattern
        self.recursive = recursive
        self.file_list = []


    def search_files(self):
        """
        Search for files in a specific directory matching a given pattern.

        Args:
            directory (str): The directory to search in.
            pattern (str): The pattern to match files (e.g., '*.txt', 'file_*.csv'). Default is '*' (all files).
            recursive (bool): Whether to search recursively in subdirectories. Default is True.

        Returns:
            list: A list of matching file paths.
        """
        matched_files = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                if self.pattern == "*" or file.endswith(self.pattern.replace("*", "")):
                    matched_files.append(os.path.join(root, file))
            if not self.recursive:
                break
        return matched_files


    def extract_excel_data(self):
        files = self.search_files()
        file_list = []
        for file in files:
            file_list.append(file)
        
        try:
            # Iterativley going through all the excel files stored and storing their data in a dictionary
            data_dictionary_list = []
            for i in range(len(file_list)):
                # Load the Excel file to check available sheet names
                excel_data = pd.ExcelFile(file_list[i])
                #print(excel_data.sheet_names)  # Displays all sheet names in the Excel file
                df = pd.read_excel(file_list[i], sheet_name=excel_data.sheet_names) # Load data from a specific sheet into a DataFrame
                data_dictionary_list.append({"file_name": file_list[i], "data": df})

            # Display the first few rows of the extracted data
            return data_dictionary_list
        
        except AttributeError as e:
            print(f"Current File {file_list[i]} isn't easily tabulated: {e}")





if __name__ == "__main__":

    main = FileDataExtractor()
    print(main.extract_excel_data())







