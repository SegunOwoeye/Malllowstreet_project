import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalyzer:
    """
    A class to analyze and visualize investment data from LGPS pools.
    """

    def __init__(self, data_dictionary_list):
        """
        Initialize the DataAnalyzer with a list of data dictionaries.

        Args:
            data_dictionary_list (list): A list of dictionaries containing file names and associated data.
        """
        self.data = self._combine_data(data_dictionary_list)

    def _combine_data(self, data_dictionary_list):
        """
        Combine data from all data dictionaries into a single DataFrame.

        Args:
            data_dictionary_list (list): A list of dictionaries with file names and data.

        Returns:
            pd.DataFrame: Combined DataFrame with standardized columns.
        """
        combined_data = []
        for item in data_dictionary_list:
            file_name = item['file_name']
            data_frames = item['data']
            for sheet_name, df in data_frames.items():
                df['source_file'] = file_name
                df['sheet_name'] = sheet_name
                combined_data.append(df)

        combined_df = pd.concat(combined_data, ignore_index=True)

        # Standardize column names
        combined_df.columns = combined_df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')

        return combined_df

    def clean_data(self):
        """
        Clean and preprocess the data for analysis.

        Returns:
            pd.DataFrame: Cleaned data.
        """
        # Display current column names for debugging
        print("Current columns:", self.data.columns.tolist())

        # Attempt to standardize column names for 'market_value' and 'asset_class'
        expected_columns = ['market_value', 'asset_class']
        standardized_columns = {col: col.lower().replace(' ', '_') for col in self.data.columns}
        self.data.rename(columns=standardized_columns, inplace=True)

        # Check if required columns are present after renaming
        missing_columns = [col for col in expected_columns if col not in self.data.columns]
        if missing_columns:
            raise KeyError(f"Missing columns in data: {missing_columns}")

        # Drop rows with missing critical information
        self.data = self.data.dropna(subset=['market_value', 'asset_class'])

        # Convert market_value to numeric, handling errors
        self.data['market_value'] = pd.to_numeric(self.data['market_value'], errors='coerce')

        # Fill or drop remaining NaN values
        self.data = self.data.dropna(subset=['market_value'])

        return self.data


    def analyze_total_assets(self):
        """
        Calculate the total market value of all assets.

        Returns:
            float: Total market value of assets.
        """
        total_assets = self.data['market_value'].sum()
        print(f"Total Assets: £{total_assets:,.2f}")
        return total_assets

    def analyze_uk_investments(self):
        """
        Calculate the total market value of UK investments.

        Returns:
            float: Total market value of UK investments.
        """
        uk_investments = self.data[self.data['country'] == 'United Kingdom']['market_value'].sum()
        print(f"Total UK Investments: £{uk_investments:,.2f}")
        return uk_investments

    def analyze_asset_class_breakdown(self):
        """
        Provide a breakdown of the market value by asset class.

        Returns:
            pd.Series: Market value breakdown by asset class.
        """
        asset_class_breakdown = self.data.groupby('asset_class')['market_value'].sum()
        print(asset_class_breakdown)
        return asset_class_breakdown

    def visualize_asset_class_breakdown(self):
        """
        Generate a bar chart of the asset class breakdown.
        """
        asset_class_breakdown = self.analyze_asset_class_breakdown()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=asset_class_breakdown.index, y=asset_class_breakdown.values, palette='viridis')
        plt.xticks(rotation=45, ha='right')
        plt.title('Asset Class Breakdown by Market Value')
        plt.xlabel('Asset Class')
        plt.ylabel('Market Value (£)')
        plt.tight_layout()
        plt.show()

    def visualize_uk_vs_nonuk_investments(self):
        """
        Generate a pie chart of UK vs. Non-UK investments.
        """
        total_assets = self.analyze_total_assets()
        uk_investments = self.analyze_uk_investments()

        plt.figure(figsize=(6, 4))
        uk_vs_nonuk = pd.Series({'UK Investments': uk_investments, 'Non-UK Investments': total_assets - uk_investments})
        uk_vs_nonuk.plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
        plt.title('UK vs. Non-UK Investments')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()

    def visualize_sector_breakdown(self):
        """
        Generate a bar chart showing the breakdown by sector if available.
        """
        if 'sector' in self.data.columns:
            sector_breakdown = self.data.groupby('sector')['market_value'].sum()

            plt.figure(figsize=(10, 6))
            sns.barplot(x=sector_breakdown.index, y=sector_breakdown.values, palette='cubehelix')
            plt.xticks(rotation=45, ha='right')
            plt.title('Sector Breakdown by Market Value')
            plt.xlabel('Sector')
            plt.ylabel('Market Value (£)')
            plt.tight_layout()
            plt.show()
        else:
            print("Sector data not available for visualization.")

