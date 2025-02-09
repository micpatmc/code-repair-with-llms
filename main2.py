import nvdlib
from datetime import datetime, timedelta

API_KEY = "4073cef3-2a1f-4283-bb46-e6f04145f38c"
MAX_DATE_RANGE = 120

class Fetch_Training_Data:
    def __init__(self, start_year=2015):
        self.languages = {
            'python': ['python'],
            'java': ['java'],
            'c_cpp': ['cpp', 'c'],
            # Add more languages and keywords here
        }
        self.start_year = start_year
        self.start_date = f'{start_year}-01-01 00:00'
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
        # Function to add days to a given date
        add_max_date = lambda date_obj, days: date_obj + timedelta(days=days)
        
        start_date_obj = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M")
        
        # Loop through the iterations
        for i in range(self.iterations):
            # Calculate end_date based on the MAX_DATE_RANGE
            end_date_obj = add_max_date(start_date_obj, MAX_DATE_RANGE)
            
            # Fetch CVE details
            self.fetch_cve_details(
                limit=1000,
                apiKey=self.apiKey,
                pubStartDate=start_date_obj.strftime("%Y-%m-%d %H:%M"),
                pubEndDate=end_date_obj.strftime("%Y-%m-%d %H:%M"),
                keyword_search="python"
            )
            
            # Set new start date for the next iteration
            start_date_obj = add_max_date(end_date_obj, 1)

    def fetch_cve_details(self, keyword_search: str, apiKey, pubStartDate, pubEndDate, limit: int = 10):
        """
        Fetch CVE details from the NVD database based on a keyword search.

        Args:
            keyword_search (str): The keyword to search for (e.g., 'Python').
            limit (int): The number of CVEs to fetch (default: 10).
        """
        # Search for CVEs matching the keyword
        r = nvdlib.searchCVE_V2(pubStartDate=pubStartDate, pubEndDate=pubEndDate, keywordSearch=keyword_search, limit=limit, key=apiKey)

        for cve in r:
            # Check if there are any code-related references
            # if "git" in cve.descriptions:  # Use 'in' instead of contains()
            #     if cve.references:
            print("\n")
            print(f"CVE ID: {cve.id}")
            print(f"Description: {cve.descriptions}")
        
            print("References to code fixes or advisories:")
            for ref in cve.references:
                print(f"- {ref.url}")
                
            # Check if there are descriptions related to code
            if cve.descriptions:
                print("Full Description(s):")
                for desc in cve.descriptions:
                    print(f"  - {desc.value}")
            
            print("\n")

def main():
    gen_training_date = Fetch_Training_Data(start_year=2024)

    print("Getting CVE's:")
    gen_training_date.iterate_cves()

if __name__ == "__main__":
    main()
