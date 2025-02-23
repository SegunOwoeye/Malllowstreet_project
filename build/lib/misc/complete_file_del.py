from misc.file_filter import delete_unwanted_files


def run():
    # Brunel Delete
    try: 
        folder_path1 = "Data/raw_data/brunel_data"
        keywords1 = ["Equities", "Portfolio", "Emerging"]
        delete_unwanted_files(folder_path1, keywords1)
    except Exception as e:
        print(f"Error: {e}")

    
    # Bordertocoast Delete
    try: 
        folder_path2 = "Data/raw_data/bordertocoast_data"
        keywords2 = ["Equities", "Portfolio", "Emerging", "Equity"]
        delete_unwanted_files(folder_path2, keywords2)
    except Exception as e:
        print(f"Error: {e}")


    # lgpscentral Delete
    try: 
        folder_path3 = "Data/raw_data/lgpscentral_data"
        keywords3 = ["Equities", "Portfolio", "Emerging", "Equity"]
        delete_unwanted_files(folder_path3, keywords3)
    except Exception as e:
        print(f"Error: {e}")



if __name__ == '__main__':
    run()  # run the function when the script is executed directly