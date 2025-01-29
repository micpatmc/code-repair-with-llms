import re

class PatternMatch():
    def __init__(self, model, fault_plan: str):
        self.model = model
        self.fault_plan = fault_plan
        self.patterns = []

    # return prompt
    def get_prompt(self, fault_index: int) -> str:
        return f"""
        Generate code implementation for the identified fault. Analyze its relationships with other identified faults 
        and provide a structured implementation. Always include the High-Level Overview.

        ### Implementation Plan:
        #### Code Changes:
        ```[language]
        // Provide the detailed code implementation here
        ```

        Make sure to keep the code changes format consistent, there should always be an opening ``` and closing ```.

        Fault ID: {fault_index}
        Fault Plan Details: {self.fault_plan}
        """

    def get_matches(self):
        return self.patterns

    def return_code_block(self, text: str) -> str:
        # regex pattern to match text between triple backticks
        pattern = r"```(?:[a-zA-Z]*)?\r?\n([\s\S]*?)```"

        # find first match and return only the code content (group 2)
        match = re.search(pattern, text)
        return match.group(1) if match else ""

    # based on prompt and number of faults, execute for each fault
    def execute_pattern_matching(self):
        # get the number of faults
        num_faults = len(re.findall(r'#### Fault \d+:', self.fault_plan))

        pre_patterns = []

        # there will be num_fault calls to the llm about pattern matching
        for fault_index in range(num_faults):
            # pass the fault_loc prompt but focus on specific fault
            prompt = self.get_prompt(fault_index + 1)
            response = self.model.generate_response(prompt)
            pre_patterns.append(response)

        for pattern in pre_patterns:
            self.patterns.append(self.return_code_block(pattern))