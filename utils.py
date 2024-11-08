import os
import requests
import gradio as gr

API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Make sure API key is set in environment variables

def load_file(file_path):
    """Load C file content."""
    with open(file_path, 'r') as file:
        return file.read()

def call_huggingface_api(prompt):
    """Send the prompt to Hugging Face API and get a response."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": prompt
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        
        # Extract only the 'generated_text' from the response, stripping unnecessary parts
        if isinstance(result, list) and isinstance(result[0], dict) and 'generated_text' in result[0]:
            generated_text = result[0]['generated_text'].strip()
            return generated_text
        else:
            return "Error: Unexpected response format."
    else:
        return "Error: Unable to fetch results from Hugging Face API."

def identify_cve(code):
    """Identify vulnerabilities in the code."""
    prompt = f"Analyze the following C code and identify all security vulnerabilities. Focus on issues such as buffer overflows, use of unsafe functions like gets, and any other common security flaws.\n\n{code}\n"
    return call_huggingface_api(prompt)

def repair_code(code, vulnerabilities):
    """Repair the code based on the identified vulnerabilities."""
    prompt = f"Fix the following vulnerabilities for the code in the C programming language. The vulnerabilities are as follows: {vulnerabilities}\n\nCode to fix:\n\n{code}"
    return call_huggingface_api(prompt)

# Gradio interface function to call and display results
def analyze_and_repair_c_code(c_code):
    # Step 1: Identify vulnerabilities
    vulnerabilities = identify_cve(c_code)
    
    # Step 2: Repair the code based on the vulnerabilities
    repaired_code = repair_code(c_code, vulnerabilities)
    
    # Return the results
    return vulnerabilities, repaired_code

# Gradio Interface Setup
iface = gr.Interface(
    fn=analyze_and_repair_c_code,  # Function that will process the inputs
    inputs=gr.Textbox(label="Enter C Code", placeholder="Paste your C code here..."),  # Input widget
    outputs=[gr.Textbox(label="Identified Vulnerabilities"), gr.Textbox(label="Repaired Code")],  # Outputs
    title="C Code Vulnerability Analysis and Repair",  # Title of the interface
    description="This tool analyzes C code for vulnerabilities, identifies security flaws, and provides a repaired version with fixes applied."  # Description
)

# Launch the Gradio interface
iface.launch()


# Launch the Gradio interface
if __name__ == "__main__":
    iface.launch()