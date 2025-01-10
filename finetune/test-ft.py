
from finetune import FineTuner

input_dir = "./llama-3.2-1B"
output_dir = "./models/new_llama"

fine_tuner = FineTuner(input_dir)

tokenizer, tokenized_data = fine_tuner.tokenize_text("C:\\Users\\Vincent\\Desktop\\school\\senior design\\code-repair-with-llms\\test.txt")
tokenizer.save_pretrained(output_dir)

dataset = fine_tuner.prepare_dataset(tokenized_data)
fine_tuner.fine_tune_qlora(dataset, output_dir)
