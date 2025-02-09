import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import nvdlib
import re
from tqdm import tqdm

class CVEDatasetGenerator:

    
    
    def __init__(self, start_year=2015):
        self.languages = {
            'python': ['python'],
            'java': ['java'],
            'c_cpp': ['cpp', 'c'],
            # Add more languages and keywords here
        }
        self.start_year = start_year
    
    def fetch_cves(self, start_year=self.start_year):
        """Fetches CVEs from NVD for specified programming languages"""
        all_cves = []
        current_year = datetime.now().year
        
        for year in range(start_year, current_year + 1):
            # Format dates properly for NVD API
            start_date = f"{year}-01-01 00:00"
            end_date = f"{year+1}-01-01 00:00"
            
            for language, keywords in self.languages.items():
                for keyword in keywords:
                    try:
                        # Using nvdlib to fetch CVEs with proper date format
                        cves = nvdlib.searchCVE(
                            keywordSearch=keyword,
                            pubStartDate=start_date,
                            pubEndDate=end_date,
                            key='4073cef3-2a1f-4283-bb46-e6f04145f38c'
                        )
                        
                        for cve in cves:
                            # Initialize default values
                            description = None
                            cwe_id = None
                            severity = None
                            
                            # Safely handle descriptions
                            if cve.descriptions and hasattr(cve.descriptions[0], 'value'):
                                description = cve.descriptions[0].value
                            
                            # Safely handle weaknesses (CWE)
                            if hasattr(cve, 'weaknesses') and cve.weaknesses:
                                cwe_id = cve.weaknesses[0].value if hasattr(cve.weaknesses[0], 'value') else None
                            
                            # Safely handle severity score
                            if hasattr(cve, 'score') and cve.score:
                                severity = cve.score[0].score if hasattr(cve.score[0], 'score') else None
                            
                            # Build the CVE data
                            cve_data = {
                                'cve_id': cve.id,
                                'language': language,
                                'description': description,
                                'severity': severity,
                                'cwe_id': cwe_id,
                                'published_date': cve.published,
                                'references': [ref.url for ref in cve.references],
                                'vulnerable_code': None,
                                'fixed_code': None
                            }
                            
                            all_cves.append(cve_data)
                    except Exception as e:
                        print(f"Error fetching CVEs for {language} - {keyword} in {year}: {str(e)}")
                        continue
        
        return pd.DataFrame(all_cves)

    def extract_code_snippets(self, df):
        """Attempts to extract vulnerable and fixed code snippets from references"""
        def find_code_blocks(text):
            # Common code block patterns in GitHub issues, commits, etc.
            patterns = [
                r'```[a-z]*\n(.*?)```',  # Markdown code blocks
                r'(?s)(?<=diff\s--git).*?(?=diff\s--git|\Z)',  # Git diff blocks
                r'(?s)@@ .*? @@.*?(?=@@|$)'  # Unified diff chunks
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL)
                for match in matches:
                    yield match.group(1).strip()
        
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            code_pairs = []
            
            for ref in row['references']:
                if 'github.com' in ref:
                    try:
                        # Get raw content if it's a GitHub link
                        response = requests.get(ref.replace('github.com', 'raw.githubusercontent.com'))
                        content = response.text
                        
                        code_blocks = list(find_code_blocks(content))
                        if len(code_blocks) >= 2:
                            # Assume first block is vulnerable code, second is fixed
                            code_pairs.append({
                                'vulnerable': code_blocks[0],
                                'fixed': code_blocks[1]
                            })
                    except Exception as e:
                        print(f"Error processing reference {ref}: {str(e)}")
                        continue
            
            if code_pairs:
                df.at[idx, 'vulnerable_code'] = code_pairs[0]['vulnerable']
                df.at[idx, 'fixed_code'] = code_pairs[0]['fixed']
        
        return df

    def prepare_training_data(self, df):
        """Prepares the final dataset for LLM training"""
        # Filter out entries without code pairs
        df_clean = df.dropna(subset=['vulnerable_code', 'fixed_code'])
        
        # Create structured training examples
        training_data = []
        for _, row in df_clean.iterrows():
            example = {
                'input': {
                    'code': row['vulnerable_code'],
                    'vulnerability_type': row['cwe_id'],
                    'description': row['description'],
                    'language': row['language']
                },
                'output': {
                    'fixed_code': row['fixed_code']
                },
                'metadata': {
                    'cve_id': row['cve_id'],
                    'severity': row['severity'],
                    'published_date': str(row['published_date'])  # Convert datetime to string
                }
            }
            training_data.append(example)
        
        return training_data

    def save_dataset(self, training_data, output_file='cve_training_data.json'):
        """Saves the training dataset to a JSON file"""
        with open(output_file, 'w') as f:
            json.dump(training_data, f, indent=2)

def main():
    # Initialize the generator
    generator = CVEDatasetGenerator()
    
    print("Fetching CVEs...")
    try:
        cve_df = generator.fetch_cves()
        print(f"Found {len(cve_df)} CVE entries")
        
        print("Extracting code snippets...")
        cve_df = generator.extract_code_snippets(cve_df)
        
        print("Preparing training data...")
        training_data = generator.prepare_training_data(cve_df)
        
        generator.save_dataset(training_data)
        print(f"Dataset saved with {len(training_data)} examples")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()