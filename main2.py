import requests
import nvdlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import time

# def search_cves_by_keyword(
#     keyword: str,
#     api_key: str,
#     days_back: int = 30
# ) -> Optional[Dict[str, Any]]:
#     """
#     Search for CVEs using the NVD REST API and get details using nvdlib.
    
#     Args:
#         keyword (str): The keyword to search for (e.g., 'python')
#         api_key (str): Your NVD API key
#         days_back (int): Number of days to look back (default: 30)
    
#     Returns:
#         Optional[Dict[str, Any]]: Dictionary containing CVE information or None if not found
#     """
#     try:
#         # Calculate the start date
#         start_date = datetime.now() - timedelta(days=days_back)
#         start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%S.000")
        
#         # NVD API endpoint
#         url = "https://services.nvd.nist.gov/rest/json/cves/2.0/"
        
#         # Parameters for the API request
#         params = {
#             "keywordSearch": keyword,
#             "resultsPerPage": 1,  # We only need the most recent one
#         }
        
#         # Headers including the API key
#         headers = {
#             "apiKey": api_key
#         }
        
#         # Make the request to NVD API
#         response = requests.get(url, params=params, headers=headers)
        
#         if response.status_code == 200:
#             data = response.json()
#             print(data)
#             # Check if we found any vulnerabilities
#             if data['totalResults'] > 0:
#                 # Get the most recent CVE ID

#                 if 'cveChanges' in data:
#                 # Extract CVE ID from 'cveChanges' list
#                     cve_id = data['cveChanges'][0]['change']['cveId']
                    
#                 # Check if the data has 'vulnerabilities' field (second format)
#                 elif 'vulnerabilities' in data:
#                 # Extract CVE ID from 'vulnerabilities' list
#                     cve_id = data['vulnerabilities'][0]['cve']['id']
                
#                 # Use nvdlib to get detailed information about this specific CVE
#                 time.sleep(0.6)  # Rate limiting as per NVD API requirements
#                 cve_item = nvdlib.searchCVE(id=cve_id, key=api_key)[0]
                
#                 # Extract severity metrics if available
#                 severity = None
#                 if hasattr(cve_item, 'metrics') and cve_item.metrics:
#                     severity = {
#                         'cvss_v3': getattr(cve_item.metrics, 'cvssMetricV3', [{}])[0].get('cvssData', {}).get('baseScore'),
#                         'cvss_v2': getattr(cve_item.metrics, 'cvssMetricV2', [{}])[0].get('cvssData', {}).get('baseScore')
#                     }
                
#                 # Build response dictionary
#                 result = {
#                     "cve_id": cve_item.cve_id,
#                     "published_date": cve_item.published_date,
#                     "last_modified_date": cve_item.last_modified_date,
#                     "description": cve_item.description,
#                     "severity": severity,
#                     "references": [ref.url for ref in cve_item.references] if hasattr(cve_item, 'references') else [],
#                     "vulnerable_configuration": [conf.cpe23Uri for conf in cve_item.configurations] if hasattr(cve_item, 'configurations') else []
#                 }
                
#                 return result
#             else:
#                 print(f"No CVEs found for the keyword '{keyword}' in the last {days_back} days")
#                 return None
                
#         else:
#             print(f"Error: API request failed with status code {response.status_code}")
#             return None
            
#     except Exception as e:
#         print(f"Error fetching CVE data: {str(e)}")
#         return None

# # Example usage:
# if __name__ == "__main__":
#     API_KEY = "4073cef3-2a1f-4283-bb46-e6f04145f38c"
#     keyword = "python"
    
#     result = search_cves_by_keyword(
#         keyword=keyword,
#         api_key=API_KEY,
#         days_back=30
#     )
    
#     if result:
#         print("\nMost recent CVE details:")
#         print(f"CVE ID: {result['cve_id']}")
#         print(f"Published: {result['published_date']}")
#         print(f"Description: {result['description']}")
#         if result['severity']:
#             print(f"CVSS v3 Score: {result['severity']['cvss_v3']}")
#         print("\nReferences:")
#         for ref in result['references']:
#             print(f"- {ref}")

# r = nvdlib.searchCVE_V2(keywordSearch='Python', limit=10)
# for cve in r:
#     print("\n")
#     print(cve)
#     print("\n")


import nvdlib

'''
    Need to develop a wrapper with a start date and end date.

    Will loop through and modify the pubStartDate and pubEndDate to loop over longer ranges.

    Their range is only within 120 days so we will make it exact.

    Will allow for many keywords/Programming languages to be looped through

    Check for 

'''

def fetch_cve_details(keyword_search: str, limit: int = 10, apiKey: str = ""):
    """
    Fetch CVE details from the NVD database based on a keyword search.

    Args:
        keyword_search (str): The keyword to search for (e.g., 'Python').
        limit (int): The number of CVEs to fetch (default: 10).
    """
    # Search for CVEs matching the keyword
    r = nvdlib.searchCVE_V2(pubStartDate = '2019-06-08 00:00', pubEndDate = '2019-09-08 00:00', keywordSearch=keyword_search, limit=limit, key=apiKey)
    
    for cve in r:
        # Check if there are any code-related references
    
        if cve.contains("git")
        if cve.references:
            print("\n")
            print(f"CVE ID: {cve.id}")
        #print(f"Published Date: {cve.published_date}")
            print(f"Description: {cve.descriptions}")
            
            print("References to code fixes or advisories:")
            for ref in cve.references:
                print(f"- {ref.url}")
            
            # Check if there are descriptions related to code
            if cve.descriptions:
                print("Full Description(s):")
                for desc in cve.descriptions:
                    print(f"  - {desc.value}")
            
            # Check configurations if available
            # if cve.configurations:
            #     print("Vulnerable Configurations:")
            #     for conf in cve.configurations:
            #         print(f"- {conf.cpe23Uri}")
            
            print("\n")

# Example usage
API_KEY = "4073cef3-2a1f-4283-bb46-e6f04145f38c"
fetch_cve_details("python", limit=100, apiKey=API_KEY)
