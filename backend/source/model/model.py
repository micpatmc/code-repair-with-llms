from transformers import AutoTokenizer
from huggingface_hub import InferenceClient
from typing import Dict, Any, Optional
import json
import os
from pathlib import Path

HF_TOKEN = "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"

class Model:
    def __init__(self, model: str = ""):
        # retrieves the config path and creates list of model configs
        self.config_path = self._get_config_path()
        self.model_configs = self._load_model_configs()
        
        # sets all attributes for the model
        self.model = model
        self.current_config = self._get_model_config(model)
        self.tokenizer = self.get_tokenizer()
        self.client = self.initialize_client()
        self.max_context = self.current_config.get("max_context", 0)
        self.max_response = self.current_config.get("max_response", 0)


    """
    Loading configurations for all potential/supported models
    """
    # finds config path
    def _get_config_path(self) -> Path:
        return Path(__file__).parent / "model_configs.json"

    # loads the configs
    def _load_model_configs(self) -> Any:
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at {self.config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid configuration file: {str(e)}")

    # based on model passed from selection, loads specific model configs
    def _get_model_config(self, model: str) -> Any:
        if model not in self.model_configs["models"]:
            raise ValueError(f"Unsupported model: {model}")
        return self.model_configs["models"][model]

    """
    methods for model specific functions
    """
    # get tokenizer for specific model
    def get_tokenizer(self) -> AutoTokenizer:
        try:
            return AutoTokenizer.from_pretrained(self.model)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize tokenizer: {str(e)}")

    # This class will be used to connect to UCF ARCC and also use the models under the inference client
    def initialize_client(self) -> InferenceClient:
        # add a check to see if the ARCC model is being used or online models
        # -->
        try:
            return InferenceClient(
                self.model,
                token=HF_TOKEN,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize model client: {str(e)}")

    # sets the max contraints for the windows for specific models
    def set_constraints(self, max_context: int) -> None:
        pass

    # returns the number of tokens in given text
    def get_token_count(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    # returns if the prompt can fit in the context window
    def is_within_context_window(self, text: str) -> Any:
        return self.get_token_count(text) <= self.max_context

    # returns if the model can return full file in the response window
    def is_within_response_window(self, text: str) -> Any:
        return self.get_token_count(text) <= self.max_response

    # generate the response based on model and config
    def generate_response(self, prompt: str, **kwargs: Dict[str, Any]) -> Any:
        if not self.is_within_context_window(prompt):
            # need to chunk the input
            pass

        if not self.is_within_response_window(prompt):
            # need to chunk the input of the source file to fit the response window equally
            pass

        try:
            # Merge default configs with any provided kwargs
            generation_config = {
                "max_new_tokens": self.max_response,
                "temperature": self.current_config["temperature"],
                "top_k": self.current_config["top_k"],
                "top_p": self.current_config["top_p"],
                "do_sample": False,
            }
            generation_config.update(kwargs)

            return self.client.text_generation(
                prompt,
                **generation_config
            )
        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {str(e)}")

    # update settings for model, example top_p or temp
    def update_model_config(self, model_name: str, config_updates: Dict[str, Any]) -> None:
        pass
