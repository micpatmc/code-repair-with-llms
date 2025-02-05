from rag_db import RAG
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from source.model.model import Model
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "meta-llama/Llama-3.2-1B"

from langchain.prompts import PromptTemplate

def format_prompt_for_llama(prompt: str, variables: dict = None) -> str:
    # Define a prompt template
    template = PromptTemplate(
        input_variables=list(variables.keys()) if variables else [],
        template=prompt
    )
    
    # LLaMA-specific formatting
    formatted_prompt = f"<s>[INST] {template.format(**variables) if variables else prompt} [/INST]</s>"
    
    return formatted_prompt

def format_prompt(query, context):
    # Include only the top 3 most relevant context sections based on similarity score
    sorted_context = sorted(context, key=lambda x: x['similarity_score'], reverse=True)[:3]
    
    # Build the context string with only essential details
    context_str = ""
    for i, result in enumerate(sorted_context, 1):
        context_str += f"\nSection {i}:\n"
        context_str += f"Code:\n{result['code']}\n"  # Exclude metadata and similarity score
        context_str += "-" * 40 + "\n"

    # Concise prompt with minimal instructions
    prompt = f"""Provide only the shortest and most direct answer to the question. Do not elaborate or provide additional information.
    
    Context:{context_str}

    Question: {query}

    Answer:"""

    return prompt


def main():
    # create vector db and load model and tokenizer
    rag = RAG()
    model = Model("meta-llama/Meta-Llama-3-8B-Instruct")

    """tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="cuda"
    )"""

    # embed contents of the file
    rag.embed_code(["C:\\Users\\Gavin Cruz\\Documents\\SD1\\finalspace\\code-repair-with-llms\\source\\pipeline\\rag\\example1.py"])

    # query
    query = ""

    # retrieve context
    context = rag.retrieve_context(query, k=3)

    # format and obtain prompt
    prompt = format_prompt(query, context)

    response = model.generate_response(prompt)
    

    with open("response.txt", "w") as f:
        f.write(response)

    rag.clear_index()

if __name__ == "__main__":
    main()