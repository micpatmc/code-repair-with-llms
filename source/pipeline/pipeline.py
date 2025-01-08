import json
import sys
import os

from fault_loc.fault_localization import FaultLocalization
from pattern_match.pattern_matching import PatternMatch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from source.model.model import Model

"""
this pipeline will be the main process for the pipeline that is being integrated
"""
class Pipeline():
    def __init__(self):
        self.model = None
        self.stage1 = False
        self.stage2 = False
        self.stage3 = False
        self.stage4 = False

    # define the model being used throughout the pipeline
    def set_model(self, model_selection: str):
        try:
            self.model = Model(model_selection)
        except Exception as e:
            print(f"Error setting model: {e}")

    # first stage which determines where the fault/vulnerability is
    def fault_localization(self, precode_content):
        fl = FaultLocalization(self.model, precode_content)
        fl.calculate_fault_localization()
        return fl.get_fault_localization()

    # second stage determines the type of fault/vulnerability
    def pattern_matching(self, localization: str):
        pm = PatternMatch(self.model, localization)
        pm.execute_pattern_matching()
        return pm.get_matches()

    # third stage creates the patches and places them in the code
    def patch_generation(self):
        pass

    # last stage determines if the fixes are corrected
    def patch_validation(self):
        pass

def create_code_dict(file_path):
    # Initialize the list to store dictionaries for each entry
    code_dicts = []
    
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Process each entry in the JSON file
    for entry in data:
        # Initialize a dictionary for this entry
        code_dict = {}
        
        # Extract the pre_code
        if 'pre_code' in entry:
            code_dict['precode'] = entry['pre_code']
        else:
            code_dict['precode'] = "No pre code available"
        
        # Extract the post_code (if it exists)
        if 'post_code' in entry:
            code_dict['postcode'] = entry['post_code']
        else:
            code_dict['postcode'] = "No post code available"
        
        # Add additional information if available
        if 'id' in entry:
            code_dict['id'] = entry['id']
        if 'sub_id' in entry:
            code_dict['sub_id'] = entry['sub_id']
        if 'human_patch' in entry:
            code_dict['human_patch'] = entry['human_patch']
        if 'cve_id' in entry:
            code_dict['cve_id'] = entry['cve_id']
        if 'cwe_id' in entry:
            code_dict['cwe_id'] = entry['cwe_id']
        
        # Append this entry's dictionary to the list
        code_dicts.append(code_dict)
    
    return code_dicts

def write_to_file(content):
    # Open the file in write mode
    with open("output.txt", 'a') as file:
        # Write the content to the file
        file.write(content + "\n")
        # Close the file
        file.close()

def main():
    # create pipeline
    pipeline = Pipeline()
    
    # process file input
    code_dict = create_code_dict('testSD1/source/pipeline/00_initial_java.json')

    # set the model to whatever the selection is
    pipeline.set_model("meta-llama/Meta-Llama-3-8B-Instruct")

    # fault localization
    # localize and plan the faults in the source code
    write_to_file("#### Fault Localization ####\n")
    localization = pipeline.fault_localization(code_dict[0]['precode'])
    write_to_file(localization)

    # pattern matching
    # take the localization and use it to create code snippets for code fixes for the code
    write_to_file("\n#### Pattern Matching ####\n")
    patterns = pipeline.pattern_matching(localization)
    for pattern in patterns:
        write_to_file(pattern)

    # patch generation
    # take the code snippets and create multiple files with potential fixes (patch candidates)

    # patch validation
    # test the candidates and use the optimal one (passes the test suite)

    # write new file
    # write the candidate to the file and return the file to download


if __name__ == "__main__":
    main()