import nvdlib
import json
import pandas as pd  # Import pandas for CSV conversion
from datetime import datetime, timedelta

API_KEY = "4073cef3-2a1f-4283-bb46-e6f04145f38c"
MAX_DATE_RANGE = 120

class Fetch_Training_Data:
    def __init__(self, start_year=2015, keywords=[]):
        self.cves = []
        self.start_year = start_year
        self.start_date = f'{start_year}-01-01 00:00'
        self.keywords = keywords
        self.apiKey = API_KEY

        # Calculate the number of iterations and remainder
        self.iterations, self.remainder = self.calculate_iterations(self.start_date)

    def calculate_iterations(self, start_date):
        start_obj = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
        current_obj = datetime.now()

        diff = current_obj - start_obj
        total_days = diff.days

        iterations = total_days // MAX_DATE_RANGE
        remainder = total_days % MAX_DATE_RANGE

        return iterations, remainder

    def iterate_cves(self):
        add_max_date = lambda date_obj, days: date_obj + timedelta(days=days)
        
        start_date_obj = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M")
        
        for i in range(self.iterations):
            for j in range(len(self.keywords)):
                end_date_obj = add_max_date(start_date_obj, MAX_DATE_RANGE)
                
                self.fetch_cve_details(
                    limit=1000,
                    apiKey=self.apiKey,
                    pubStartDate=start_date_obj.strftime("%Y-%m-%d %H:%M"),
                    pubEndDate=end_date_obj.strftime("%Y-%m-%d %H:%M"),
                    keyword_search="java"
                )
                
                start_date_obj = add_max_date(end_date_obj, 1)

        self.save_dataset()

    def fetch_cve_details(self, keyword_search: str, apiKey, pubStartDate, pubEndDate, limit: int = 10):
        """
        Fetch CVE details from the NVD database based on a keyword search.

        Args:
            keyword_search (str): The keyword to search for (e.g., 'Python').
            limit (int): The number of CVEs to fetch (default: 10).
        """
        r = nvdlib.searchCVE_V2(
            pubStartDate=pubStartDate, 
            pubEndDate=pubEndDate, 
            keywordSearch=keyword_search, 
            delay=1,
            limit=limit, 
            key=apiKey
        )

        cve_list = list(r)  # Convert generator to a list
        self.cves.extend(cve_list)  # Store the CVE objects in the dataset

        for cve in cve_list:
            print("\n")
            print(f"CVE ID: {cve.id}")
            print(f"Description: {cve.descriptions}")
        
            print("References to code fixes or advisories:")
            for ref in cve.references:
                print(f"- {ref.url}")
                
            if cve.descriptions:
                print("Full Description(s):")
                for desc in cve.descriptions:
                    print(f"  - {desc.value}")

    def save_dataset(self, output_json='cve_training_data.json', output_csv='cve_training_data.csv'):
        """Saves the training dataset to both JSON and CSV files"""

        # Convert CVE objects to dictionaries
        data = [self.serialize_cve(cve) for cve in self.cves]

        # Save as JSON
        with open(output_json, 'w') as f:
            json.dump(data, f, indent=2)

        # Convert to Pandas DataFrame and save as CSV
        df = pd.DataFrame(data)
        df.to_csv(output_csv, index=False)

        print(f"Data saved successfully to {output_json} and {output_csv}")

    def serialize_cve(self, cve):
        """Convert a CVE object to a dictionary for JSON serialization"""
        return {
            "id": cve.id,
            "published": cve.published,
            "lastModified": cve.lastModified,
            "vulnStatus": cve.vulnStatus,
            "descriptions": " | ".join([desc.value for desc in cve.descriptions]) if cve.descriptions else "",
            "references": " | ".join([ref.url for ref in cve.references]) if cve.references else ""
        }

def main():

    keywords = {
            'python': ['python'],
            'java': ['java'],
            'c_cpp': ['cpp', 'c'],
            # Add more languages and keywords here
        }
    
    gen_training_date = Fetch_Training_Data(start_year=2020, keywords=keywords)

    print("Getting CVE's:")
    gen_training_date.iterate_cves()

if __name__ == "__main__":
    main()
