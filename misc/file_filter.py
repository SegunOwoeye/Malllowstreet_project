import os


def delete_unwanted_files(folder_path, keywords, file_extensions  = ['.xls', '.xlsx', '.pdf']):
    """
    Deletes all Excel files in the specified folder that do not contain any of the specified keywords in their filenames.
    :param folder_path: The path to the folder containing the Excel files.
    :param keywords: A list of keywords to look for in the filenames. If a filename does not contain any of these keywords, it will be deleted.
    """
    for filename in os.listdir(folder_path):
        if any(filename.lower().endswith(ext) for ext in file_extensions):
            if not any(keyword.lower() in filename.lower() for keyword in keywords):
                file_path = os.path.join(folder_path, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {filename}")
                except Exception as e:
                    print(f"Failed to delete {filename}: {e}")

if __name__ == '__main__':
    folder_path = "Data/raw_data/bordertocoast_data"
    keywords = ["Equities", "Portfolio", "Emerging"]
    delete_unwanted_files(folder_path, keywords)

