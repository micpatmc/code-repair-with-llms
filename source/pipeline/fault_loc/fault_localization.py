
from huggingface_hub import InferenceClient
import os

"""
this stage will take the input from the user and pass it with the prompt to the LLM
and then the llm will provide explicit information on where the faults are in the code
and how to fix them
"""
class FaultLocalization():
    def __init__(self, model, data):
        self.model = model # model object
        self.data = data
        self.fault_localization = None # output created by the llm

    def get_sys_prompt(self) -> str:
        return f"""
        You job is to determine if there are any vulnerabilies or faults with the code.
        """

    def get_prompt(self) -> str:
        return f"""
        Analyze the following code file to identify any vulnerabilities or faults. For each identified issue, provide 
        the analysis using the following structured format:

        ### High-Level Overview:
        - Provide a clear, explicit summary of what the file is doing, including its purpose and functionality.

        ### Detected Faults:
        For each fault or vulnerability, use this consistent structure:
        
        #### Fault 1:
        - **Fault Detected**: [Brief description of the issue]
        - **Cause**: [Explain what part of the code is causing the issue and why]
        - **Impact**: [Outline the potential consequences of this fault on the program’s functionality or security]
        - **Solution**: [Provide a detailed suggestion or fix to resolve the issue]

        Repeat the above format (Fault 2, Fault 3, etc.) for additional issues if applicable. If no faults are detected, 
        explicitly state that the code appears to be fault-free.

        ### Output Requirements:
        - Use bullet points and section headers for clarity.
        - Ensure all explanations are concise, actionable, and easy to understand.

        The code is: {self.data}
        """


    def get_fault_localization(self)-> str:
        return self.fault_localization

    def set_fault_localization(self, fault_localization):
        self.fault_localization = fault_localization

    def calculate_fault_localization(self):
        # pass prompt to LLM with precode to find faults
        sys_prompt = self.get_sys_prompt()
        prompt = self.get_prompt()

        response = self.model.generate_response(prompt)

        self.set_fault_localization(response)