from rag_db import RAG
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "meta-llama/Llama-3.2-1B"

def format_prompt(query, context):
    context_str = ""
    for i, result in enumerate(context, 1):
        context_str += f"\nSection {i}:\n"
        context_str += f"File: {result['metadata']}\n"
        context_str += f"Code:\n{result['code']}\n"
        context_str += f"Similarity Score: {result['similarity_score']:.2f}\n"
        context_str += "-" * 40 + "\n"

    prompt = f"""Below is a section of Python code and a question about it.
    Please analyze the code and answer the question based on the provided context.
    Just respond with the answer without providing additional information.

    Context:
    {context_str}

    Question: {query}

    Answer:"""

    return prompt

def main():
    # create vector db and load model and tokenizer
    rag = RAG()
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="cuda"
    )

    # embed contents of the file
    rag.embed_code(["C:\\Users\\Gavin Cruz\\Documents\\SD1\\finalspace\\code-repair-with-llms\\source\\pipeline\\rag\\example1.py"])

    # query
    query = "What is the main purpose of this code?"

    # retrieve context
    context = rag.retrieve_context(query, k=3)

    # format and obtain prompt
    prompt = format_prompt(query, context)

    # tokenize and generate
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate response
    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            max_length=1024,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # decode response from llm
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = response.replace(prompt, "").strip()

    with open("response.txt", "w") as f:
        f.write(response)

    rag.clear_index()

if __name__ == "__main__":
    main()