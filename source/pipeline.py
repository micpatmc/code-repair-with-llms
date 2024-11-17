import json

from fault_loc.fault_localization import FaultLocalization

"""
this pipeline will be the main process for the pipeline that is being integrated
"""
class Pipeline():
    def __init__(self):
        self.stage1 = False
        self.stage2 = False
        self.stage3 = False
        self.stage4 = False

    # first stage which determines where the fault/vulnerability is
    def fault_localization(self, precode_content):
        fl = FaultLocalization(precode_content)
        fl.calculate_fault_localization()
        return fl.get_fault_localization()

    # second stage determines the type of fault/vulnerability
    def pattern_matching(self):
        pass

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

def main():
    # create pipeline
    pipeline = Pipeline()
    
    # process file input
    code_dict = create_code_dict('testSD1/source/00_initial_java.json')

    #print(code_dict[0]['precode'])

    # run pipeline on first json data entry
    localization = pipeline.fault_localization(code_dict[0]['precode'])
    #print(localization)


if __name__ == "__main__":
    main()