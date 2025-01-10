import torch
import torch_directml
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, BitsAndBytesConfig
from datasets import Dataset
from peft import PeftModel, LoraConfig, get_peft_model
from bitsandbytes.functional import QuantState


device = None

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch_directml.device()

class FineTuner:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None
        self.qt_model = None
        self.model_path = "C:\\Users\\Vincent\\Desktop\\school\\senior design\\code-repair-with-llms\\llama-3.2-1B"

    def tokenize_text(self, file_path):
        tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        with open(file_path, "r", encoding="utf-8") as f:
            text_data = f.read()
        
        tokenized_data = tokenizer(text_data, return_tensors="pt", truncation=True, padding="max_length", max_length=1024)
        return tokenizer, tokenized_data

    def prepare_dataset(self, tokenized_data):
        labels = tokenized_data["input_ids"].clone()
        dataset = Dataset.from_dict({
            "input_ids": tokenized_data["input_ids"],
            "attention_mask": tokenized_data["attention_mask"],
            "labels": labels
        })
        return dataset

    @staticmethod
    def requires_peft_loading(model_dir):
        peft_files = ['adapter_model.bin', 'adapter_config.json']
        return any(file in os.listdir(model_dir) for file in peft_files)

    def fine_tune_qlora(self, dataset, output_dir):
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )
                
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path, quantization_config=bnb_config).to(device)
        
        lora_config = LoraConfig(
            r=8,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.1,
            bias="none"
        )
        
        self.qt_model = get_peft_model(self.model, lora_config)
        self.model = None
        
        training_args = TrainingArguments(
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            num_train_epochs=3,
            learning_rate=2e-4,
            logging_steps=10,
            output_dir=output_dir,
            save_steps=1000,
            save_total_limit=2,
            fp16=True,
            report_to="none"
        )
        
        trainer = Trainer(
            model=self.qt_model,
            args=training_args,
            train_dataset=dataset
        )
        trainer.train()
        
        self.qt_model.save_pretrained(output_dir)

        self.qt_model = None

    def __del__(self):
        if hasattr(self, 'qt_model'):
            self.qt_model = None
        if hasattr(self, 'model'):
            self.model = None