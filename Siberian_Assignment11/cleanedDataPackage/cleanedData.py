# File Name: cleanData.py
# Names: Nogaye Gueye, Uruz Bidiwala
# email:  gueyene@mail.uc.edu  bidiwaur@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:  04/17/2025
# Course #/Section:   IS4010
# Semester/Year:   Spring 2025
# Brief Description of the assignment: Created classes and methods with code to clean data sets and create csv files. 
# Brief Description of what this module does: Contains code that cleans the data, edits addresses and removes repeated data rows, etc. 
# Citations: openai.com 
# Anything else that's relevant: N/A


import pandas as pd
import requests
import re
import time



class DataCleaner:
    def __init__(self, filepath):
        """Initialize DataCleaner with the input CSV and the ZipCodeAPI."""
        self.filepath = filepath
        self.df = pd.read_csv(filepath)
        self.api_key = "42b1bee0-162e-11f0-a524-53feafedb3a5"


    def _remove_duplicates(self):
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        after = len(self.df)
        print(f"🔁 Removed {before - after} duplicate rows.")

    def _format_gross_price(self):
        """Force 'Gross Price' to be strings with exactly 2 decimal places."""
        if "Gross Price" in self.df.columns:
            self.df["Gross Price"] = self.df["Gross Price"].apply(self._format_price)
            print("💵 Gross Price column formatted.")

    def _format_price(self, val):
        try:
            return "{:.2f}".format(float(val))
        except:
            return ""

    def _separate_anomalies(self):
        """Remove 'Pepsi' entries and save them to a separate anomalies CSV."""
        if "Fuel Type" in self.df.columns:
            anomalies = self.df[self.df["Fuel Type"].str.lower() == "pepsi"]
            anomalies.to_csv("Data/dataAnomalies.csv", index=False)
            self.df = self.df[self.df["Fuel Type"].str.lower() != "pepsi"]
            print("🧃 Anomalies (Pepsi) saved to Data/dataAnomalies.csv")\

    def _extract_city_state(self):
         #Extract city and state from various Full Address formats.
        self.df["City"] = None
        self.df["State"] = None

        for idx, address in self.df["Full Address"].items():
            if not isinstance(address, str):
                continue

            # Format 1: Street, City, ST
            match1 = re.search(r"^[^,]+,\s*([^,]+),\s*([A-Za-z]{2})$", address)

            # Format 2: ZIP ST, City, Street
            match2 = re.search(r"^\d{5}\s+([A-Za-z]{2}),\s*([^,]+),", address)

            # Format 3: Street, City, ST ZIP
            match3 = re.search(r"^[^,]+,\s*([^,]+),\s*([A-Za-z]{2})\s+\d{5}$", address)

            if match1:
                self.df.at[idx, "City"] = match1.group(1).strip()
                self.df.at[idx, "State"] = match1.group(2).strip().upper()
            elif match2:
                self.df.at[idx, "State"] = match2.group(1).strip().upper()
                self.df.at[idx, "City"] = match2.group(2).strip()
            elif match3:
                self.df.at[idx, "City"] = match3.group(1).strip()
                self.df.at[idx, "State"] = match3.group(2).strip().upper() 
    
        


    def _fill_missing_zip_codes(self):
        """Extract ZIP from Full Address or use API (max 5 times)."""
        api_calls = 0
        max_api_calls = 5
        filled_count = 0

        if "Zip Code" not in self.df.columns:
            self.df["Zip Code"] = None

        for idx, row in self.df.iterrows():
            if pd.notna(row.get("Zip Code")):
                continue

            address = row.get("Full Address", "")
            zip_match = re.search(r"\b\d{5}\b", address)
            if zip_match:
                self.df.at[idx, "Zip Code"] = zip_match.group()
                filled_count += 1
            elif api_calls < max_api_calls:
                match = re.search(r',\s*([^,]+),\s*([A-Za-z]{2})$', address)
                if match:
                    city = match.group(1).strip()
                    state = match.group(2).strip().upper()
                    zip_code = self.api.get_zip_code(city, state)
                    if zip_code:
                        self.df.at[idx, "Zip Code"] = zip_code
                        api_calls += 1
                        filled_count += 1

        print(f"📬 ZIP codes filled for {filled_count} rows (including {api_calls}5 via API).")
    def lookup_zip_code(self, city, country='US'):
        """

        """
        try:
            response = requests.get(
                "https://app.zipcodebase.com/api/v1/search",
                params={
                    "apikey": self.api_key,
                    "city": city,
                    "country": country
                }
            )
            data = response.json()
            results = data.get("results", {})
            if results:
                first_result = next(iter(results.values()))
                if first_result:
                    return first_result[0].get("postal_code")
        except Exception as e:
            print(f"Error fetching ZIP for city '{city}': {e}")
        
    
    def clean_and_save(self, output_path="Data/cleanedData.csv"):
        """Run all cleaning steps and save cleaned data to CSV."""
        self._remove_duplicates()
        self._format_gross_price()
        self._separate_anomalies()
        self._extract_city_state()  # must come BEFORE
        self._fill_missing_zip_codes()  # so this has city/state to work with
    # Save cleaned data using same style as anomalies
        self.df.to_csv("Data/cleanedData.csv", index=False)
        print("✅ Cleaned data saved to Data/cleanedData.csv")