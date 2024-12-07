from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Dict, Any, List

class DeepSeekWrapper:
    def __init__(self, model_name="deepseek-ai/deepseek-coder-33b-instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True
        )
        self.model.eval()

    def generate(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to DeepSeek format and generate response"""
        prompt = self._format_messages(messages)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        outputs = self.model.generate(
            inputs.input_ids,
            max_new_tokens=2048,
            temperature=0.7,
            top_p=0.95,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self._extract_response(response)

    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Format messages for DeepSeek-Coder"""
        formatted = ""
        for msg in messages:
            if msg["role"] == "system":
                formatted += f"System: {msg['content']}\n\n"
            elif msg["role"] == "user":
                formatted += f"Human: {msg['content']}\n"
            elif msg["role"] == "assistant":
                formatted += f"Assistant: {msg['content']}\n"
        formatted += "Assistant: "
        return formatted

    def _extract_response(self, text: str) -> str:
        """Extract the model's response from the generated text"""
        if "Assistant: " in text:
            return text.split("Assistant: ")[-1].strip()
        return text.strip()