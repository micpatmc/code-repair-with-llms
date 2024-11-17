
from huggingface_hub import InferenceClient
import os

"""
this stage will take the input from the user and pass it with the prompt to the LLM
and then the llm will provide explicit information on where the faults are in the code
and how to fix them
"""
class FaultLocalization():
    def __init__(self, data):
        self.data = data
        self.fault_localization = None # output created by the llm

    def get_sys_prompt(self) -> str:
        return f"""
        You job is to determine if there are any vulnerabilies or faults with the code.
        """

    def get_prompt(self, data) -> str:
        return f"""
        Given this code file, determine if there are any vulnerabilies or faults with the code
        and provide, as an explanation, what can be done to fix this problem. Also provide a high level overview
        of the file and what the file is doing explicitly.

        The code is: {data}
        """

    def get_fault_localization(self)-> str:
        return self.fault_localization

    def set_fault_localization(self, fault_localization):
        self.fault_localization = fault_localization

    def calculate_fault_localization(self):
        # pass prompt to LLM with precode to find faults
        sys_prompt = self.get_sys_prompt()
        prompt = self.get_prompt(self.data)

        # need to create a global class for initializing LLM being used at this stage but example for now
        client = InferenceClient(
            "meta-llama/Llama-3.2-3B-Instruct",
            token="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",
        )
        response = client.text_generation(
            prompt,
            max_new_tokens=2048,
            temperature=0.7,
            do_sample=True,
            top_k=50,
            top_p=0.95,
        )

        self.set_fault_localization(response)