# main script to run 

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import torch_directml


device = torch_directml.device()

# Load the tokenizer and model
model_name = "EleutherAI/gpt-neo-125M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set pad_token if it's not defined
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token  # Set pad_token to eos_token

# Move the model to GPU if available
# model = model.half().to(device)
model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)

prompt = f"what is the color of the sun"


# Define the input prompt
inputs = tokenizer(prompt, return_tensors="pt", padding=True)
input_ids = inputs["input_ids"].to(device)
attention_mask = inputs["attention_mask"].to(device)

# Generate text
output_ids = model.generate(input_ids, attention_mask=attention_mask, max_new_tokens=50, num_return_sequences=1)

# Decode and print the generated text
generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print(generated_text)
print('baiiii :3')
