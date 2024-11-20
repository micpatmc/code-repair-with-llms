import openai

# Set up your OpenAI API key
openai.api_key = ''

def get_fixed_code(file_path):
    # Read the vulnerable script
    with open(file_path, 'r') as file:
        input_code = file.read()
    
    # Send the code to ChatGPT, requesting a fix for vulnerabilities
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Please identify and fix any vulnerabilities in this code, make sure to give me back only the file and no additional text, don't talk about anything else in the output:\n\n{input_code}"}
        ]
    )
    
    # Get the modified code from ChatGPT's response
    fixed_code = response['choices'][0]['message']['content']
    
    # Write the fixed code to a new file
    output_file_path = "fixed_script.py"
    with open(output_file_path, 'w') as output_file:
        output_file.write(fixed_code)
    
    print(f"Fixed code saved to {output_file_path}")
    return output_file_path

# Example usage
file_path = "file.py"  # Replace with the path to your vulnerable script
get_fixed_code(file_path)
