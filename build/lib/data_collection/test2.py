from Data_Analyzer.Brunel_LGPS_data_analysis import DataAnalyzer
from data_collection.brunel_data_collection_gen import FileDataExtractor

# Extract the data
extractor = FileDataExtractor()
data_dictionary_list = extractor.extract_excel_data()

# Analyze and visualize the data
analyzer = DataAnalyzer(data_dictionary_list)
analyzer.clean_data()

analyzer.analyze_total_assets()
analyzer.analyze_uk_investments()
analyzer.analyze_asset_class_breakdown()

analyzer.visualize_asset_class_breakdown()
analyzer.visualize_uk_vs_nonuk_investments()
analyzer.visualize_sector_breakdown()
